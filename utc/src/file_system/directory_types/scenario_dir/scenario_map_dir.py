from utc.src.file_system.directory_types.default_dir import DefaultDir
from utc.src.file_system.file_types import InfoFile, SumoNetworkFile
from utc.src.file_system.file_constants import DirPaths, FileExtension
from typing import List


class ScenarioMapDir(DefaultDir):
    """
    Class representing directory of scenario maps, has 2 sub-directories:\n
    1 - network_dir (containing network '.net.xml' files)\n
    2 - information_dir (containing information '.info' files about commands used to generate network)
    """
    def __init__(self, scenario_name: str):
        """
        :param scenario_name: name of scenario folder
        """
        super().__init__(scenario_name, DirPaths.SCENARIO_MAPS)
        self.network_dir: DefaultDir = DefaultDir(
            scenario_name, DirPaths.SCENARIO_MAPS_NETWORKS,
            FileExtension.SUMO_NETWORK, SumoNetworkFile
        )
        self.information_dir: DefaultDir = DefaultDir(
            scenario_name, DirPaths.SCENARIO_MAPS_INFOS,
            FileExtension.INFO, InfoFile
        )

    def initialize_dir_structure(self) -> bool:
        to_initialize: List[DefaultDir] = [self, self.network_dir, self.information_dir]
        for directory in to_initialize:
            if directory is None:
                print(f"Cannot initialize directory of type 'None' !")
                return False
            if not directory.initialize_dir():
                return False
        return True


if __name__ == "__main__":
    pass


