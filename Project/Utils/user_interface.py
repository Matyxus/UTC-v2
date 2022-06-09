from typing import Dict, List, Tuple, Mapping
import prompt_toolkit
import subprocess
import inspect


class UserInterface:
    """ Parent class for static/dynamic input """

    def __init__(self):
        print(f"Launching UI for input, initializing objects..")
        self.running = True  # Control of main loop
        # Mapping name of commands to their respective functions
        self.functions: Dict[str, callable] = {
            # function_name : function_pointer
            "exit": self.exit_command,
            "help": self.help_command
        }

    # ----------------------------------------- Input -----------------------------------------

    def dynamic_input(self) -> None:
        """
        Handles input dynamically passed during runtime, always has while(self.running) loop.

        :return: None
        """
        print("Starting program, for help type: 'help'")
        while self.running:
            # Command name
            command_name: str = input("Input command: ").lower()
            if not command_name or command_name not in self.functions:
                print(f"Unknown command name: {command_name}, for list of commands type: 'help'")
                continue
            # Command args
            command_args: List[inspect.Parameter] = list(
                inspect.signature(self.functions[command_name]).parameters.values()
            )
            print("Input command arguments separated by space (arguments with values are optional)")
            inputted_args: Dict[str, str] = {}
            # Check for no argument commands
            if len(command_args) != 0:
                inputted_args: Dict[str, str] = {
                    arg.name: '' if arg.default == inspect.Parameter.empty else str(arg.default)
                    for arg in command_args
                }
                for arg_name, arg_default in inputted_args.items():
                    user_input: str = ""
                    if arg_default:
                        user_input = input(f"Enter argument {arg_name}(default {arg_default}): ")
                        if not user_input:
                            user_input = arg_default
                    else:
                        user_input = input(f"Enter argument {arg_name}: ")
                    inputted_args[arg_name] = user_input.lower()

            print(f"Interpreting... {command_name}:{inputted_args}")
            # Check and process command args
            processed_args: list = self.process_command_args(command_args, inputted_args)
            # Check if command has any required arguments in case processed_args is empty
            if len(processed_args) < sum(1 for arg in command_args if arg.default == inspect.Parameter.empty):
                continue  # Error occurred
            # Execute function
            print(f"Executing command: {command_name} with arguments: {processed_args}")
            self.functions[command_name](*processed_args)
        print("Exiting...")

    def static_input(self) -> None:
        """
        Handles statically passed input (e.g. from command line, file, ..), uses sys.argv

        :return: None
        """
        raise NotImplementedError("Error, this functions has to be implemented by children classes!")

    # ----------------------------------------- Commands -----------------------------------------

    def help_command(self, command_name: str = "all") -> None:
        """
        :param command_name: description of command to be printed (default all)
        :return: None
        """
        function_to_print: Dict[str, callable] = self.functions
        if command_name != "all" and command_name in self.functions:
            function_to_print = {command_name: self.functions[command_name]}
        for function_name, function in function_to_print:
            print(f"Description of command: {function_name}\n")
            print("\t" + inspect.getdoc(function) + "\n")

    def exit_command(self) -> None:
        """
        Quits the program

        :return: None
        """
        self.running = False

    # ----------------------------------------- Utils -----------------------------------------

    def process_command_args(self, command_args: List[inspect.Parameter], inputted_args: Dict[str, str]) -> list:
        """
        :param command_args: List of command arguments in form of class Parameter
        :param inputted_args: arguments of command inputted by user (dictionary mapping command name to value)
        :return: list of command arguments in correct type (in order)
        """
        ret_val: list = []
        # Check command arguments
        if not self.check_command_args(command_args, inputted_args):
            return ret_val
        # Check types of command arguments and convert them to their correct type, if possible
        for arg in command_args:
            # If argument is not in args, expecting default value (checked by check_command_args function)
            if arg.name not in inputted_args:
                assert (arg.default != inspect.Parameter.empty)
                ret_val.append(arg.default)
            # Argument is present, convert inputted string to correct type
            elif arg.annotation == inspect.Parameter.empty:  # Unknown type, leave it as string
                print(f"Found unknown type of parameter: {arg.name}, defaulting to string")
                ret_val.append(inputted_args[arg.name])
            elif arg.annotation == bool:  # Check for bool
                ret_val.append(inputted_args[arg.name] in ["true", "t"])
            # Default value
            elif arg.default != inspect.Parameter.empty and str(arg.default) == inputted_args[arg.name]:
                ret_val.append(arg.default)
            else:
                try:
                    ret_val.append(arg.annotation(inputted_args[arg.name]))
                except ValueError as e:
                    print(f"Unable to convert argument: {arg.name} to type: {arg.annotation}, defaulting to string")
                    ret_val.append(inputted_args[arg.name])
        return ret_val

    def check_command_args(self, command_args: List[inspect.Parameter], inputted_args: Dict[str, str]) -> bool:
        """
        Check command name and number of arguments.

        :param command_args: List of command arguments in form of class Parameter
        :param inputted_args: arguments of command inputted by user in string (mapped name to value)
        :return: True if arguments are correct, false otherwise
        """
        # Check for incorrectly entered arguments (evaluated by format_command_args function)
        if not len(inputted_args):
            return False
        # ------------------------- Check number of arguments -------------------------
        arg_count: int = len(inputted_args)
        maximum_args: int = len(command_args)  # Maximum number of arguments function can take
        # Count number of arguments with non default value (aka required arguments)
        minimum_args: int = sum(1 for arg in command_args if arg.default == inspect.Parameter.empty)
        if arg_count < minimum_args:
            print(f"Command expects at least {minimum_args} arguments, got {arg_count}!")
            return False
        elif arg_count > maximum_args:
            print(f"Command expects at maximum {maximum_args} arguments, got {arg_count}!")
            return False
        # ------------------------- Check if arguments correspond to function args -------------------------
        for arg in command_args:
            if arg.default != inspect.Parameter.empty:
                if arg.name not in inputted_args:
                    print(f"Missing required argument: {arg.name}, please check your input!")
                    return False
        return True

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
            if callProcessErr != subprocess.TimeoutExpired:
                print(f"Error {str(callProcessErr)} for command {command}\n\n")
        return success, console_output



# For testing purposes
#if __name__ == "__main__":
#    default_str: str = "number='' count='' from='' to='' where='default'"
#    text: str = prompt_toolkit.prompt('What is your name: ', default=default_str)
#    print(type(text))
    # temp = UserInterface()
    # temp.dynamic_input()




