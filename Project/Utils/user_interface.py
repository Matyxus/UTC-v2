from typing import Dict, List, Tuple
import subprocess
import inspect


class UserInterface:
    """ Parent class for static/dynamic input """

    def __init__(self):
        print(f"Launching UI for input, initializing objects..")
        self.running = True  # Control of main loop
        # Mapping name of commands to List
        self.functions: Dict[str, List[callable, int, int]] = {
            # function_name : [function_pointer, {arg_name: [[arg_type,..], optional], ...}]
            "exit": [self.exit_command, 0, 0],
            "help": [self.help_command, 0, 0]
        }

    # ----------------------------------------- Input -----------------------------------------

    def dynamic_input(self) -> None:
        """
        Handles input dynamically passed during runtime, always has while(self.running) loop.

        :return: None
        """
        raise NotImplementedError("Error, this functions has to be implemented by children classes!")

    def static_input(self) -> None:
        """
        Handles statically passed input (e.g. from command line, file, ..), uses sys.argv

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

    def run_commmand(self, command: str, timeout: int = None, encoding: str = "utf-8") -> Tuple[bool, str]:
        """
        https://stackoverflow.com/questions/41094707/setting-timeout-when-using-os-system-function

        :param command: console/terminal command string
        :param timeout: wait max timeout (seconds) for run console command (default None)
        :param encoding: console output encoding, default is utf-8
        :return: True/False on success/failure, console output as string
        """
        success: bool = False
        console_output: str = ""
        try:
            console_output_byte = subprocess.check_output(command, shell=True, timeout=timeout)
            console_output = console_output_byte.decode(encoding)  # '640x360\n'
            console_output = console_output.strip()  # '640x360'
            success = True
        except subprocess.CalledProcessError as callProcessErr:
            print(f"Error {str(callProcessErr)} for command {command}\n\n")
        return success, console_output

# For testing purposes
if __name__ == "__main__":
    pass
    # temp = UserInterface()
    # print(temp.functions["exit"].__doc__)
    # print(inspect.signature(temp.functions["exit"]))

