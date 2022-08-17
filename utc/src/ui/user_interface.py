from utc.src.file_system import InfoFile
from utc.src.ui.argument_validator import ArgumentValidator, ValidationError
from typing import Dict, Tuple, List
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
from prompt_toolkit.document import Document
from prompt_toolkit import prompt
from inspect import signature, getdoc
from os import fstat
from sys import stdin
from stat import S_ISREG
import subprocess


class UserInterface:
    """ Parent class for static/dynamic input """

    def __init__(self, class_name: str):
        print(f"Launching UserInterface for {class_name}, initializing objects..")
        self.running = True  # Control of main loop
        self.name = class_name  # Name of subclass
        # Mapping name of commands to their respective functions
        self.commands: Dict[str, callable] = {
            # command_name : function_pointer
            "exit": self.exit_command,
            "help": self.help_command
        }
        # Info file
        self.info_file: InfoFile = None
        # History of used commands (mapping command name to their previous arguments)
        self.stored_arguments: Dict[str, List[str]] = {}
        # Commands Utils
        self.command_history: InMemoryHistory = None
        self.command_completer: WordCompleter = None
        self.command_validator: Validator = None
        self.argument_validator: ArgumentValidator = None
        self._input_from_file: bool = False  # If input was passed from file

    def run(self) -> None:
        """
        Handles input passed from user using prompt_toolkit to ask for
        command name, then (if there are any) asks for arguments of
        chosen command name.
        The same way is handled input passed from redirected file,
        expecting format each line to be: command_name arg1="value" arg2="value2", ...,
        there must be exactly 1 blank space between command names and its parameters

        :return: None
        """
        # Initialize
        self._input_from_file = self.is_redirected()
        if not self._input_from_file:
            print("Starting program, for help type: 'help'")
            print(
                "Input command arguments between \"quotes\", "
                "separated by space (arguments with values are optional)"
            )
        self.initialize_input()
        # Main loop
        while self.running:
            command_name, command_args = self.get_input()
            converted_args: list = []
            if command_args:
                # Convert argument to their correct type (add default values if missing)
                doc: Document = Document(command_args)
                try:
                    converted_args = self.argument_validator.convert_args(
                        self.argument_validator.parse_input(doc), doc
                    )
                except ValidationError as e:
                    print(f"Error: {e.message}")
                    break
            self.record(command_name, command_args)
            print(f"Executing command {command_name}({command_args}) ...")
            # Execute
            self.commands[command_name](*converted_args)
        print("Exiting ...")

    # ----------------------------------------- Input -----------------------------------------

    def initialize_input(self) -> None:
        """
        :return:
        """
        self.argument_validator = ArgumentValidator()
        # Input from file needs only argument validator
        if self._input_from_file:
            return
        # Dynamic input
        self.command_history = InMemoryHistory()
        self.command_completer = WordCompleter(list(self.commands.keys()), ignore_case=True, WORD=True)
        self.command_validator = Validator.from_callable(
            self.is_command,
            error_message="This is not valid command, for list of commands type 'help'!",
        )

    def get_input(self) -> Tuple[str, str]:
        """
        :return: reads and returns command name and its arguments from stdin
        """
        command_name: str = ""
        inputted_args: str = ""
        if self._input_from_file:  # Static input
            file_line: str = next(stdin, "").strip()
            split_input: List[str] = file_line.split()
            # End of input
            if not split_input:
                command_name = "exit"
                print("Reached end of file, exiting ...")
            else:
                print(f"Reading line: {file_line}")
                command_name = split_input.pop(0)
            inputted_args = " ".join(split_input)
            # Prepare for argument input
            self.argument_validator.set_command(self.commands[command_name])
        else:  # Dynamic input
            command_name = prompt(
                "Input command: ", completer=self.command_completer, history=self.command_history,
                validator=self.command_validator
            ).lower()
            # Prepare for argument input
            self.argument_validator.set_command(self.commands[command_name])
            # Check for no argument commands
            if len(self.argument_validator.args) != 0:
                inputted_args = prompt(
                    "Fill arguments: ", default=self.argument_validator.get_command_args(),
                    history=InMemoryHistory(self.stored_arguments.get(command_name, None)),
                    validator=self.argument_validator
                )
        return command_name, inputted_args

    # ----------------------------------------- Commands -----------------------------------------

    def help_command(self, command_name: str = "all") -> None:
        """
        :param command_name: description of command to be printed (default all)
        :return: None
        """
        function_to_print: Dict[str, callable] = self.commands
        if command_name != "all" and command_name in self.commands:
            function_to_print = {command_name: self.commands[command_name]}
        for function_name, function in function_to_print.items():
            print(f"Description of command {function_name}:{signature(function)}")
            if getdoc(function) is not None:
                print("\t" + getdoc(function).replace("\n", "\n\t") + "\n")
            else:  # Handle missing documentation
                print(f"\t No documentation\n")

    def exit_command(self) -> None:
        """
        Quits the program

        :return: None
        """
        self.running = False

    # ----------------------------------------- Utils -----------------------------------------

    def add_commands(self, commands: Dict[str, callable]) -> None:
        """
        :param commands: dictionary mapping command name to method to be added
        :return: None
        """
        for command_name in commands.copy():  # Iterate over copy, so we can change size
            # Command with this name is present, add suffix of class name
            if command_name in self.commands:
                # Extract previous
                function_pointer: callable = commands.pop(command_name)
                # Change name to class specific
                command_name = f"{command_name}-{self.name}"
                commands[command_name] = function_pointer
            self.commands[command_name] = commands[command_name]
        if self.command_completer is not None:
            self.command_completer.words = list(self.commands.keys())
        print(f"Enabling new commands: {list(commands.keys())}")

    def remove_commands(self, command_names: List[str]) -> None:
        """
        :param command_names: list of command names to be removed
        :return: None
        """
        for command_name in command_names:
            self.commands.pop(command_name, None)
        if self.command_completer is not None:
            self.command_completer.words = list(self.commands.keys())
        print(f"Disabling commands: {command_names} ...")

    def is_command(self, text: str) -> bool:
        """
        :param text: string
        :return: True if string is valid command name, false otherwise
        """
        return text in self.commands

    def is_redirected(self) -> bool:
        """
        :return: True if input is redirected from file
        """
        mode: int = fstat(stdin.fileno()).st_mode
        return S_ISREG(mode)

    def record(self, command_name: str, command_args: str) -> None:
        """
        :param command_name: name of command
        :param command_args: arguments of command (in format: arg_name1="value1")
        :return: None
        """
        # Memorize inputted args for history
        if not self._input_from_file and command_args:
            if command_name not in self.stored_arguments:
                self.stored_arguments[command_name] = []
            self.stored_arguments[command_name].append(command_args)
        # Record command to info file
        if self.info_file is not None:
            self.info_file.record_command(command_name, command_args)

    def merge(self, other: 'UserInterface') -> None:
        """
        Merges other UserInterface subclasses to current one,
        taking their commands and redirecting any newly added/removed
        commands to this instance

        :param other: different UserInterface subclass
        :return: None
        """
        if not isinstance(other, UserInterface):
            print(f"Unable to merge UserInterface with different type then UserInterface, got: {type(other)}")
            return
        # Remove "exit" and "help" from other classes, so that they are for this instance
        other.commands.pop("exit", None)
        other.commands.pop("help", None)
        # Copy other commands
        temp_commands: Dict[str, callable] = {
            command_name: function_ptr for command_name, function_ptr in other.commands.items()
        }
        # Change commands pointer
        other.commands = self.commands
        other.command_completer = self.command_completer
        # Add commands using other class to changed pointer
        # (this is mainly for "other" to add suffix of its own name to command names in case of collision)
        other.add_commands(temp_commands)

    @staticmethod
    def run_command(command: str, timeout: int = None, encoding: str = "utf-8") -> Tuple[bool, str]:
        """
        https://stackoverflow.com/questions/41094707/setting-timeout-when-using-os-system-function

        :param command: console/terminal command string
        :param timeout: wait max timeout (seconds) for run console command (default None)
        :param encoding: console output encoding, default is utf-8
        :return: True/False on success/failure, console output as string
        """
        success: bool = False
        console_output: str = ""
        print(f"Calling command: {command} with timeout: {timeout}")
        try:
            console_output_byte = subprocess.check_output(command, shell=True, timeout=timeout)
            console_output = console_output_byte.decode(encoding)  # '640x360\n'
            console_output = console_output.strip()  # '640x360'
            success = True
        except subprocess.SubprocessError as callProcessErr:
            # Catch other errors, apart from timeout ...
            if not isinstance(callProcessErr, subprocess.TimeoutExpired):
                print(f"Error {str(callProcessErr)}")
            else:
                success = True
        print(f"Success: {success}")
        return success, console_output
