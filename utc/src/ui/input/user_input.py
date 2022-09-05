from utc.src.ui.command import Command
from utc.src.ui.input.input_utils import InputUtils, ArgumentValidator, InMemoryHistory, WordCompleter, Validator
from typing import Tuple, List, Dict, Optional, Union
from os import fstat
from sys import stdin, argv
from stat import S_ISREG
from prompt_toolkit import prompt


class UserInput(InputUtils):
    """

    """
    def __init__(self):
        super().__init__()
        self._input_from_file: bool = self.is_redirected()
        # Mapping name of commands to their respective classes
        self.commands: Dict[str, Command] = {
            # command_name : Command
        }

    def initialize_input(self) -> None:
        """
        Initializes additional utility classes for input

        :return: None
        """
        self.argument_validator = ArgumentValidator()
        # Input from file needs only argument validator
        if self._input_from_file:
            return
        # Dynamic input
        self.command_history = InMemoryHistory()
        self.command_completer = WordCompleter(list(self.commands.keys()), ignore_case=True, WORD=True)
        self.command_validator = Validator.from_callable(
            self.command_exists,
            error_message="This is command does not exist, for list of commands type 'help'!",
        )

    # --------------------------------------------- Input ---------------------------------------------

    def get_input(self) -> Optional[Tuple[str, str]]:
        """
        :return: tuple containing (command name, list of command args as string)
        given by user or read from file, 'None' if an error occurred
        """
        # Return input from stdin
        if self._input_from_file:
            return self.read_file_input()
        # Get input from user
        command_name: Optional[str] = self.ask_command_name()
        return command_name, self.ask_command_args(command_name)

    def ask_command_name(self) -> Optional[str]:
        """
        :return: name of user-inputted (or read from file) command name (with
        the usage of 'command_validator', the name must exist
        """
        command_name: str = prompt(
            "Input command: ", completer=self.command_completer, history=self.command_history,
            validator=self.command_validator
        ).lower()
        return command_name

    def ask_command_args(self, command: Union[Command, str]) -> str:
        """

        :param command: either name of command name or Command class
        from which arguments will get pulled
        :return: string of arguments converted to appropriate type
        (simple ones e.g. int, str, bool, ..) of given command,
        empty string if command is of type 'None' or command does not have arguments
        """
        # Convert to appropriate type
        if isinstance(command, str):
            command = self.commands.get(command, None)
        # Checks
        if command is None:
            print(f"Cannot ask for arguments of command type: 'None' !")
            return ""
        elif len(command.args.keys()) == 0:  # No arguments to fill
            return ""
        self.argument_validator.set_command(command)
        inputted_args = prompt(
            f"Fill '{command.name}' arguments: ", default=command.get_args_text(),
            history=InMemoryHistory(command.stored_arguments),
            validator=self.argument_validator
        )
        return inputted_args

    def read_file_input(self) -> Optional[Tuple[str, str]]:
        """
        Reads input from redirected file (stdin) to this program

        :return: tuple containing (command name, list of command args as string)
        given by user or read from file, 'None' if an error occurred
        """
        if not self._input_from_file:
            print(f"Cannot read input from stdin, no file was redirected!")
            return None
        file_line: str = next(stdin, "").strip()
        split_input: List[str] = file_line.split()
        # End of input
        if not split_input:
            command_name = "exit"
            print("Reached end of file, returning command: 'exit'")
        else:
            print(f"Reading line: {file_line}")
            command_name = split_input.pop(0)
        self.argument_validator.set_command(self.commands.get(command_name, None))
        return command_name, " ".join(split_input)

    # noinspection PyMethodMayBeStatic
    def get_argv(self) -> List[str]:
        """
        :return: argv arguments given to program
        """
        return argv

    # --------------------------------------------- Command Utils ---------------------------------------------

    def add_command(self, commands: List[Tuple[str, Command]], message: bool = False) -> None:
        """
        Adds command (or multiple) to data structure, fails if command name
        already exists

        :param commands: list of pairs (command_name, Command Class) to be added
        :param message: if message about command already existing should be printed (default false)
        :return: None
        """
        for command_pair in commands:
            # Check for existence
            if self.command_exists(command_pair[0]):
                if message:
                    print(f"Command name with name: '{command_pair[0]}' already exists, failed to add!")
                continue
            self.commands[command_pair[0]] = command_pair[1]
            print(f"Enabling new command: '{command_pair[0]}'")
        # Update command completer
        if self.command_completer is not None:
            self.command_completer.words = list(self.commands.keys())

    def remove_command(self, command_names: List[str], message: bool = False) -> None:
        """
        Adds command to data structure, fails if command name
        already exists

        :param command_names: list of command names to be removed
        :param message: if message about command not existing should be printed (default false)
        :return: None
        """
        for command_name in command_names:
            # Check for existence
            if not self.command_exists(command_name):
                if message:
                    print(f"Command name with name: '{command_name}' does not exists, failed to remove!")
                continue
            del self.commands[command_name]
            print(f"Removing command: '{command_name}'")
        # Update command completer
        if self.command_completer is not None:
            self.command_completer.words = list(self.commands.keys())

    def command_exists(self, command_name: str) -> bool:
        """
        :param command_name: to be checked for existence
        :return: true if command name is already in use, false otherwise
        """
        return command_name in self.commands

    # --------------------------------------------- Input Utils ---------------------------------------------

    # noinspection PyMethodMayBeStatic
    def is_redirected(self) -> bool:
        """
        :return: true if input is redirected from file, false otherwise
        """
        mode: int = fstat(stdin.fileno()).st_mode
        return S_ISREG(mode)

    def is_initialized(self) -> bool:
        if self._input_from_file:
            return self.argument_validator is not None
        return super().is_initialized()

