from utc.src.ui.command.command_parser import CommandParser
from utc.src.file_system import InfoFile
from functools import wraps
from typing import List, Dict, Tuple, Set, Optional, Any


class CommandLogger:
    """
    Class responsible for logging commands and their arguments
    """
    def __init__(self, log_commands: bool = False):
        self.logging_enabled: bool = log_commands
        self.commands: Dict[str, List[str]] = {
            # command_name: [arg1, ...]
        }
        self.commands_order: List[str] = []  # List of commands names (in which order they were used)

    def add_logg(self, command_name: str, command_args: str, message: bool = True) -> None:
        """
        :param command_name: name of command
        :param command_args: arguments of command
        :param message: if message about logging should be printed
        :return: None
        """
        if not self.logging_enabled:
            print(f"Logging is not enabled, cannot log: '{command_name}' -> '{command_args}' !")
            return
        if message:
            print(f"LOGGING: '{command_name}' -> '{command_args}'")
        if command_name not in self.commands:
            self.commands[command_name] = []
        self.commands[command_name].append(command_args)
        self.commands_order.append(command_name)

    def add_comment(self, comment: str) -> None:
        """
        :param comment: adds comment to file (starts with ';')
        :return: None
        """
        if ";" not in self.commands:
            self.commands[";"] = []
        self.commands[";"].append(comment)
        self.commands_order.append(";")

    def clear_log(self) -> None:
        """
        Clears all entries of saved commands and their arguments

        :return: None
        """
        self.commands.clear()
        self.commands_order.clear()

    def get_ordered_commands(self) -> List[Tuple[str, str]]:
        """
        :return: list of tuples (command name, arguments),
        sorted by their recorded time (order of use)
        """
        ret_val: List[Tuple[str, str]] = []
        if not self.commands_order:
            return ret_val
        # Mapping of command name to index (of current argument)
        indexes: Dict[str, int] = {command_name: 0 for command_name in self.commands.keys()}
        for command_name in self.commands_order:
            ret_val.append((command_name, self.commands[command_name][indexes[command_name]]))
            indexes[command_name] += 1
        return ret_val

    def save_log(self, file_path: str) -> bool:
        """
        Creates ".info" file at given file_path containing
        ordered commands and their arguments

        :param file_path: in which InfoFile will be created
        :return: true on success, false otherwise
        """
        if not self.logging_enabled:
            print(f"Cannot save logged commands, into: '{file_path}', logging is not enabled!")
            return False
        info_file: InfoFile = InfoFile(file_path)
        return info_file.save(commands=self.get_ordered_commands())

    def log_command(function: callable, logger: 'CommandLogger' = None) -> Any:
        """
        Decorator for function to log their command names and arguments in CommandLogger,
        methods should be called [method_name]_command,
        can be used as decorator only by subclasses of logger

        :param function: method
        :param logger: class to which the logs will be writen to, default None,
        (only added if method to be logged is not present in subclass of UserInterface)
        :return: return value of function
        """
        # noinspection PyTypeChecker
        @wraps(function)
        def wrapper(*args, **kwargs):
            self: Optional[CommandLogger] = None
            if logger is not None:
                self = logger
            # If logging is done by subclass of CommandLogger the class is first argument
            elif len(args) > 0 and isinstance(args[0], CommandLogger):
                self = args[0]
            # Check if decorator was used on correct class method
            # or given logger is not None and logging is enabled
            if self is not None and self.logging_enabled:
                mapping = CommandParser.get_mapping(function)
                formatted_args: str = CommandParser.get_formatted_args(mapping, keep_default=False)
                arguments: list = list(args[1:]) if isinstance(args[0], CommandLogger) else list(args)
                # Find missing key word arguments
                for arg_name in CommandParser.get_default_args(mapping):
                    if arg_name in kwargs:
                        arguments.append(kwargs[arg_name])
                    else:
                        arguments.append(mapping[arg_name].default)
                command_name: str = str(function.__name__).replace("_command", "")
                # print(formatted_args, arguments)
                # print(args, kwargs)
                self.add_logg(command_name, formatted_args.format(*arguments))
            else:
                print(f"Cannot log method: '{function.__name__}' into logger of type: 'None'!")
            # noinspection PyCallingNonCallable
            return function(*args, **kwargs)
        # This line is done so that PyCharm shows hints
        # on arguments methods not on decorator
        wrapper: function
        return wrapper

    def set_logger(self, target: object, methods: List[callable]) -> None:
        """
        Sets self as logging class to given methods of given class

        :param target: class to be logged
        :param methods: methods of given object to be logged
        :return: None
        """
        target_methods: Set[str] = set(dir(target))
        for method in methods:
            if method.__name__ not in target_methods:
                print(f"Unable to log method: '{method}', target: '{type(target)}' does not have it!")
            else:  # Set wrapper
                print(f"Found method: {method.__name__}, setting logger")
                setattr(target, method.__name__, CommandLogger.log_command(method, self))
                print(f"Done setting logger")
