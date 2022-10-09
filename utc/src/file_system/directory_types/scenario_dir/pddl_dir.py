from utc.src.file_system.directory_types.default_dir import DefaultDir, MyFile
from utc.src.file_system.file_constants import FileExtension
from typing import Optional


class PddlDir(DefaultDir):
    """
    Class representing scenario pddl directory,
    provides methods to get subdirectories specific to planned scenario name
    """
    def __init__(self, scenario_name: str, dir_path: str):
        """
        :param scenario_name: name of scenario folder
        :param dir_path: either SCENARIO_PROBLEMS or SCENARIO_RESULTS
        """
        super().__init__(scenario_name, dir_path)

    def get_planned_dir(self, scenario_name: str) -> Optional['DefaultDir']:
        """
        :param scenario_name: name of planned scenario
        :return: DefaultDir class of given subdirectory, or None if it does not exist
        """
        if self.dir_exist(self.path.format(scenario_name)):
            return DefaultDir(scenario_name, self.path.format(scenario_name), FileExtension.PDDL, MyFile)
        return None

    def create_sub_dir(self, subdir_name: str, *args, **kwargs) -> Optional[DefaultDir]:
        return super().create_sub_dir(subdir_name, extension=FileExtension.PDDL, file_type=MyFile)

    def initialize_dir_structure(self) -> bool:
        return self.initialize_dir()


if __name__ == "__main__":
    pass


