from utc.src.file_system.directory_types.default_dir import DefaultDir
from utc.src.file_system.file_types import StatisticsFile, InfoFile, SumoConfigFile
from utc.src.file_system.file_constants import DirPaths, FileExtension
from typing import List


class SimulationDir(DefaultDir):
    """
    Class representing simulation directory of scenario, has 3 sub-directories:\n
    1 - statistics_dir (containing statistical '.stat.xml' files about scenario vehicles)\n
    2 - information_dir (containing information '.info' files about commands used to generate scenario)\n
    3 - config_dir (containing configuration '.sumocfg' files, executables scenarios)
    """
    def __init__(self, scenario_name: str):
        """
        :param scenario_name: name of scenario folder
        """
        super().__init__(scenario_name, DirPaths.SCENARIO_SIMULATIONS)
        self.statistics_dir: DefaultDir = DefaultDir(
            scenario_name, DirPaths.SCENARIO_STATISTICS,
            FileExtension.SUMO_STATS, StatisticsFile
        )
        self.information_dir: DefaultDir = DefaultDir(
            scenario_name, DirPaths.SCENARIO_INFOS,
            FileExtension.INFO, InfoFile
        )
        self.config_dir: DefaultDir = DefaultDir(
            scenario_name, DirPaths.SCENARIO_CONFIGS,
            FileExtension.SUMO_CONFIG, SumoConfigFile
        )

    def initialize_dir_structure(self) -> bool:
        to_initialize: List[DefaultDir] = [
            self, self.statistics_dir,
            self.information_dir, self.config_dir
        ]
        for directory in to_initialize:
            if directory is None:
                print(f"Cannot initialize directory of type 'None' !")
                return False
            if not directory.initialize_dir():
                return False
        return True


if __name__ == "__main__":
    pass


