from utc.src.file_system.my_file import MyFile
from utc.src.file_system.my_directory import MyDirectory
from utc.src.file_system.file_constants import FileExtension, FilePaths


class PddlFile(MyFile):
    """

    """
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.default_extension = FileExtension.PDDL

    def parse_pddl(self):
        """
        :return:
        """
        pass

    def save(self, file_path: str = "default") -> bool:
        if file_path == "default" and not MyDirectory.dir_exist(self.get_absolute_path(self), message=False):
            print(f"Cannot save '.pddl' file, invalid path: {self.file_path}!")
            return False
        elif not MyDirectory.dir_exist(self.get_absolute_path(file_path), message=False):
            print(f"Cannot save '.pddl' file, invalid path: {file_path}!")
            return False
        elif not file_path.endswith(self.default_extension):
            print(f"Expected file type of {self.default_extension}, got: {file_path} !")
            return False
        return True

    # ------------------------------------------ Setters ------------------------------------------

    # ------------------------------------------ Getters ------------------------------------------

    # ------------------------------------------ Utils ------------------------------------------

    def get_known_path(self, file_name: str) -> str:
        # Known path for pddl files does not exist, they depend on scenario_name
        return file_name



