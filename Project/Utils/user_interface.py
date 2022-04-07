from typing import Dict, List


class UserInterface:
    """ Parent class for dynamic input """

    def __init__(self):
        self.running = True  # Control of main loop
        # Mapping name of commands to List
        self.functions: Dict[str, List[callable, int, int]] = {
            # Command name : [function, min_args, max_args]
            "exit": [self.exit_command, 0, 0],
            "help": [self.help_command, 0, 0],
        }

    def dynamic_input(self) -> None:
        """
        Handles input dynamically passed during runtime,
        always has while(self.running) loop.

        :return: None
        """
        raise NotImplementedError("Error, this functions has to be implemented by children classes!")

    # ----------------------------------------- Commands -----------------------------------------

    def help_command(self, args: List[str]) -> None:
        """
        Prints all function names with their description and how tu use them.

        :param args: arguments of help command (expecting none)
        :return: None
        """
        raise NotImplementedError("Error, this functions has to be implemented by children classes!")

    def exit_command(self, args: List[str]) -> None:
        """
        Quits the program

        :param args: arguments of exit command (expecting none)
        :return: None
        """
        self.running = False

    # ----------------------------------------- Utils -----------------------------------------

    def check_function_args(self, command_name: str, args: List[str]) -> bool:
        """
        Check command name and number of arguments.

        :param command_name: name of command
        :param args: inputted by user
        :return: True if arguments are correct, false otherwise
        """
        if command_name not in self.functions:
            print(f"Unknown command name: {command_name}")
            return False
        command: List = self.functions[command_name]
        arg_count: int = len(args)
        if arg_count < command[1]:
            print(f"Command: {command_name} expects at least {command[1]} arguments, got {arg_count}!")
            return False
        elif arg_count > command[2]:
            print(f"Command: {command_name} expects at maximum {command[2]} arguments, got {arg_count}!")
            return False
        return True

    def get_function_name(self, command_name: str) -> str:
        """
        :param command_name: name of command from command line
        :return: command name in commands dictionary, empty string if it does not exist
        """
        command_name = command_name.lower()
        if command_name in self.functions:
            return command_name
        return ""
