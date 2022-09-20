from utc.src.file_system import InfoFile
from utc.src.ui.input import UserInput
from utc.src.ui.command import Command
from typing import Dict, Tuple, Any
from prompt_toolkit.validation import ValidationError
from prompt_toolkit.document import Document
import subprocess


class UserInterface:
    """ Parent class for static/dynamic input """

    def __init__(self, class_name: str):
        print(f"Launching UserInterface for '{class_name}', initializing objects..")
        self.running = False  # Control of main loop
        self.name = class_name  # Name of subclass
        self.current_ret_val: Any = None
        # Info file
        self.info_file: InfoFile = None
        self.user_input: UserInput = None

    # ----------------------------------------- Input -----------------------------------------

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
        print("Starting program, for help type: 'help'")
        print(
            "Input command arguments between \"quotes\", "
            "separated by space (arguments with values are optional)"
        )
        self.initialize_input()
        # Main loop
        self.running = True
        while self.running:
            command_name, command_args = self.user_input.get_input()
            if not self.process_input(command_name, command_args):
                break
        print("Exiting ...")

    def process_input(self, command_name: str, command_args: str) -> bool:
        """
        :param command_name: name of command
        :param command_args: arguments of command
        :return: True on success (command execution is not checked),
        false otherwise
        """
        if self.user_input is None or not self.user_input.is_initialized():
            print(f"Cannot process input, call 'initialize_input' first !")
            return False
        elif not self.user_input.command_exists(command_name):
            return False
        converted_args: list = []
        # Convert argument to their correct type (add default values if missing)
        if command_args:
            doc: Document = Document(command_args)
            try:
                self.user_input.argument_validator.set_command(
                    self.user_input.commands[command_name]
                )
                converted_args = self.user_input.argument_validator.convert_args(
                    self.user_input.argument_validator.parse_input(doc), doc
                )
            except ValidationError as e:
                print(f"Error: {e.message}")
                return False
        # Update info file
        self.record(command_name, command_args)
        # Execute
        self.current_ret_val = self.user_input.commands[command_name].exec(converted_args, command_args)
        return True

    def initialize_input(self) -> None:
        """
        Initializes UserInput class, calls "initialize_commands"

        :return: Non
        """
        # Already initialized
        if self.user_input is not None and self.user_input.is_initialized():
            return
        # Initialize UserInput
        self.user_input = UserInput()
        self.user_input.initialize_input()
        self.initialize_commands()

    # ----------------------------------------- Commands -----------------------------------------

    def initialize_commands(self) -> None:
        """
        Method for adding initial commands to UserInput, gets called
        after initialize_input, should be overridden by subclasses of
        UserInterface

        :return: None
        """
        if self.user_input is None or not self.user_input.is_initialized():
            print(f"Cannot add commands to UserInput, is not initialized!")
            return
        # Add commands
        self.user_input.add_command([
            ("help", Command("help", self.help_command)),
            ("exit", Command("exit", self.exit_command))
        ])

    def help_command(self, command_name: str = "all") -> None:
        """
        :param command_name: name of command to be printed (default all)
        :return: None
        """
        to_print: Dict[str, Command] = {}
        # Print help description of specific command
        if command_name != "all":
            if self.user_input.command_exists(command_name):
                to_print[command_name] = self.user_input.commands[command_name]
            else:  # Unknown command
                print(f"Command: '{command_name}' does not exist, for list of commands type 'help'!")
                return
        else:  # All commands
            to_print = self.user_input.commands
        # Print help description of command\s
        for function_name, command in to_print.items():
            print(command.help())

    def exit_command(self) -> None:
        """
        Quits the program

        :return: None
        """
        self.running = False

    # ----------------------------------------- Utils -----------------------------------------

    def record(self, command_name: str, command_args: str) -> None:
        """
        :param command_name: name of command
        :param command_args: arguments of command (in format: arg_name1="value1")
        :return: None
        """
        # Record command to info file
        if self.info_file is not None:
            self.info_file.record_command(command_name, command_args)

    def merge(self, other: 'UserInterface') -> None:
        """
        Merges other UserInterface subclasses to current one,
        taking their UserInput class and changing it for this one

        :param other: different UserInterface subclass
        :return: None
        """
        # Checks
        if not isinstance(other, UserInterface):
            print(f"Unable to merge UserInterface with different type then UserInterface, got: {type(other)} !")
            return
        elif self.user_input is None or not self.user_input.is_initialized():
            print(f"Cannot merge with other UserInterface, UserInput is not initialized!")
            return
        # Change pointer and add commands
        other.user_input = self.user_input
        other.initialize_commands()

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
