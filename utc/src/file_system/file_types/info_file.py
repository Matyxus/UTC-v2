from utc.src.file_system.my_file import MyFile
from utc.src.file_system.file_constants import FileExtension, FilePaths
from typing import List, Set, Tuple


class InfoFile(MyFile):
    """
    Class holding commands used to generate scenarios/graphs
    """

    def __init__(self, file_path: str, mode: str = "w+"):
        super().__init__(file_path, mode)
        self.default_extension = FileExtension.INFO
        self.commands: List[Tuple[str, str]] = []
        self.allowed_commands: Set[str] = set()

    def record_command(self, command_name: str, args: str) -> None:
        """
        :param command_name: name of command
        :param args: arguments of command in format: arg_name1="arg_value1" .... (can be empty)
        :return: None
        """
        if command_name not in self.allowed_commands:
            # print(f"Command name: {command_name} is not allowed to be recorded!")
            return
        self.commands.append((command_name, args))

    def allow_commands(self, commands: List[str]) -> None:
        """
        :param commands: names of allowed commands which will be recorded
        :return: None
        """
        self.allowed_commands = set(commands)

    def clear(self) -> None:
        """
        Clears all entries of saved commands and their arguments

        :return: None
        """
        self.commands.clear()

    def save(self, file_path: str = "default") -> bool:
        if file_path != "default":
            self.file_path = file_path
        if not self.file_path.endswith(".info"):
            print(f"For Info file expected extension to be: {self.default_extension} !")
            return False
        # Save file
        self.mode = "w+"
        with self as info_file:
            if info_file is None:
                return False
            for command_name, args in self.commands:
                info_file.write(command_name + " " + args + "\n")
        print(f"Successfully saved '.info' file: {file_path}")
        return True

    def get_known_path(self, file_name: str) -> str:
        # Info files for graphs
        if self.file_exists(FilePaths.MAPS_INFO.format(file_name), message=False):
            return FilePaths.MAPS_INFO.format(file_name)
        # Info files for scenarios
        elif self.file_exists(FilePaths.SCENARIO_SIM_INFO.format(file_name), message=False):
            return FilePaths.SCENARIO_SIM_INFO.format(file_name)
        return file_name  # No default path
