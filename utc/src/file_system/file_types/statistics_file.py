from utc.src.file_system.file_types.xml_file import XmlFile
from utc.src.file_system.file_constants import FileExtension, FilePaths
from typing import Optional, Dict, Union


class StatisticsFile(XmlFile):
    """
    File class handling statistics files of scenarios (".stat.xml" extension),
    has utility methods, such as comparing different statistics files
    """

    def __init__(self, file_path: str):
        super().__init__(file_path, extension=FileExtension.SUMO_STATS)

    def get_vehicle_stats(self) -> Optional[Dict[str, str]]:
        """
        :return: Vehicle statistics (average values of speed, travel time, ... etc.), None if file is incorrect
        """
        if not self.is_loaded():
            print(f"Cannot return vehicle statistics, file: '{self.file_path}' is not loaded or does not exist!")
            return None
        elif self.root.find("vehicleTripStatistics") is None:
            print(f"Cannot find xml element 'vehicleTripStatistics' in file: '{self.file_path}' !")
            return None
        return self.root.find("vehicleTripStatistics").attrib

    def get_known_path(self, file_name: str) -> str:
        # Does not exist, return original value
        return file_name


# For testing purposes
if __name__ == "__main__":
    pass


