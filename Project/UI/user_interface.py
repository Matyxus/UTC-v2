from typing import Dict, Tuple, List
from Project.UI.argument_validator import ArgumentValidator, ValidationError
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

    def __init__(self):
        print(f"Launching UI for input, initializing objects..")
        self.running = True  # Control of main loop
        # Mapping name of commands to their respective functions
        self.commands: Dict[str, callable] = {
            # command_name : function_pointer
            "exit": self.exit_command,
            "help": self.help_command
        }
        # History of used commands (mapping command name to their previous arguments)
        self.stored_arguments: Dict[str, List[str]] = {}
        # Commands Utils
        self.command_history: InMemoryHistory = None
        self.command_completer: WordCompleter = None
        self.command_validator: Validator = None
        self.argument_validator: ArgumentValidator = None

    def run(self) -> None:
        """
        :return:
        """
        # Check if input is directed from file
        if self.is_redirected():
            print("Launching static input, reading commands from file")
            self.static_input()
        else:
            print("Launching dynamic input, reading commands entered by user")
            self.dynamic_input()
        print("Exiting...")

    # ----------------------------------------- Input -----------------------------------------

    def dynamic_input(self) -> None:
        """
        Handles input dynamically passed during runtime, always has while(self.running) loop

        :return: None
        """
        print("Starting program, for help type: 'help'")
        print(
            "Input command arguments between \"quotes\", "
            "separated by space (arguments with values are optional)"
        )
        # ------------------ Init ------------------
        self.command_history = InMemoryHistory()
        self.command_completer = WordCompleter(list(self.commands.keys()), ignore_case=True)
        self.command_validator = Validator.from_callable(
            self.is_command,
            error_message="This is not valid command, for list of commands type 'help'!",
        )
        self.argument_validator = ArgumentValidator()
        # ------------------ Main loop ------------------
        while self.running:
            # Command name
            command_name: str = prompt(
                "Input command: ", completer=self.command_completer, history=self.command_history,
                validator=self.command_validator
            ).lower()
            # Prepare for argument input
            self.argument_validator.set_command(self.commands[command_name])
            inputted_args: list = []
            inputted_args_text: str = ""
            # Check for no argument commands
            if len(self.argument_validator.args) != 0:
                inputted_args_text: str = prompt(
                    "Fill arguments: ", default=self.argument_validator.get_command_args(),
                    history=InMemoryHistory(self.stored_arguments.get(command_name, None)),
                    validator=self.argument_validator
                )
                # Convert argument to their correct type (add default values if missing)
                doc: Document = Document(inputted_args_text)
                inputted_args = self.argument_validator.convert_args(
                    self.argument_validator.parse_input(doc), doc
                )
                assert (type(inputted_args) == list)
                # Memorize inputted args for history
                if command_name not in self.stored_arguments:
                    self.stored_arguments[command_name] = []
                self.stored_arguments[command_name].append(inputted_args_text)
            print(f"Executing command {command_name}({inputted_args_text}) ...")
            self.commands[command_name](*inputted_args)

    def static_input(self) -> None:
        """
        Handles statically passed input from redirected file (e.g. file.py < file),
        expecting each command to be written on its own line, space separated,
        in format: command_name arg_name1="arg_value", ....

        :return: None
        """
        self.argument_validator = ArgumentValidator()
        for index, line in enumerate(stdin):
            print(f"Reading line: {index} -> {line}")
            stripped = line.strip()
            # In case file does not end with new line
            if not stripped:
                break
            split_input: List[str] = line.split()
            if not split_input:
                print(f"Invalid input: {split_input}")
                continue
            # Command name
            command_name: str = split_input.pop(0)
            if not self.is_command(command_name):
                print(f"Received invalid command: {command_name} for list of commands use command 'help'!")
                continue
            # Prepare for argument input
            self.argument_validator.set_command(self.commands[command_name])
            inputted_args: list = []
            inputted_args_text: str = ""
            # Check for no argument commands
            if len(self.argument_validator.args) != 0:
                inputted_args_text: str = " ".join(split_input)
                doc: Document = Document(inputted_args_text)
                try:
                    self.argument_validator.validate(doc)
                except ValidationError as e:
                    print(f"Error {e}")
                    continue
                inputted_args = self.argument_validator.convert_args(
                    self.argument_validator.parse_input(doc), doc
                )
                assert (type(inputted_args) == list)
            print(f"Executing command {command_name}({inputted_args_text}) ...")
            self.commands[command_name](*inputted_args)

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
        :param commands:
        :return: None
        """
        for command_name, function_pointer in commands.items():
            self.commands[command_name] = function_pointer
        self.command_completer.words = list(self.commands.keys())
        print(f"Enabling new commands: {list(commands.keys())} ...")

    def remove_commands(self, command_names: List[str]) -> None:
        """
        :param command_names:
        :return: None
        """
        for command_name in command_names:
            self.commands.pop(command_name, None)
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

    def run_command(self, command: str, timeout: int = None, encoding: str = "utf-8") -> Tuple[bool, str]:
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
                print(f"Error {str(callProcessErr)}\n\n")
            else:
                success = True
        print(f"Success: {success}")
        return success, console_output
