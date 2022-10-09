from utc.src.file_system.directory_types.default_dir import DefaultDir
from utc.src.file_system.file_types import InfoFile, SumoNetworkFile, ProbabilityFile
from utc.src.file_system.file_constants import DirPaths, FileExtension
from typing import List


class MapDir(DefaultDir):
    """
    Class representing directory of maps (user generated or converted from '.osm'), has 5 sub-directories:\n
    1 - osm_dir (containing '.osm' files downloaded from OpenStreetMap)\n
    2 - filtered_dir (containing filtered '.osm' files by osmfilter)
    3 - sumo_dir (containing  '.net.xml' files converted from 'filtered' folder)
    4 - probability_dir (containing '.prob' files mapping junction to junction probability of flow generation)
    5 - information_dir (containing information '.info' files about commands used to generate networks)
    """
    def __init__(self):
        super().__init__("", DirPaths.MAPS)
        self.osm_dir: DefaultDir = DefaultDir(
            "", DirPaths.MAPS_OSM,
            FileExtension.OSM, None
        )
        self.filtered_dir: DefaultDir = DefaultDir(
            "", DirPaths.MAPS_FILTERED,
            FileExtension.OSM, None
        )
        self.sumo_dir: DefaultDir = DefaultDir(
            "", DirPaths.MAPS_SUMO,
            FileExtension.SUMO_NETWORK, SumoNetworkFile
        )
        self.probability_dir: DefaultDir = DefaultDir(
            "", DirPaths.MAPS_PROB,
            FileExtension.PROB, ProbabilityFile
        )
        self.information_dir: DefaultDir = DefaultDir(
            "", DirPaths.MAPS_INFO,
            FileExtension.INFO, InfoFile
        )

    def initialize_dir_structure(self) -> bool:
        to_initialize: List[DefaultDir] = [
            self, self.osm_dir, self.filtered_dir,
            self.sumo_dir, self.probability_dir, self.information_dir
        ]
        for directory in to_initialize:
            if directory is None:
                print(f"Cannot initialize directory of type 'None' !")
                return False
            if not directory.initialize_dir():
                return False
        return True


if __name__ == "__main__":
    temp: MapDir = MapDir()
    print(temp.list_directory(temp.sumo_dir.path))


















