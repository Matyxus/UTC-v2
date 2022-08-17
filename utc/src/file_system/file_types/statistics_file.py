from utc.src.file_system.file_types.xml_file import XmlFile
from utc.src.file_system.file_constants import FileExtension, FilePaths
from typing import Optional, Dict, Union


class StatisticsFile(XmlFile):
    """
    File class handling statistics files of scenarios (".stat.xml" extension)
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.default_extension = FileExtension.SUMO_STATS

    # ------------------------------------------ Getters ------------------------------------------

    def get_vehicle_stats(self) -> Optional[Dict[str, str]]:
        """
        :return: Vehicle statistics (average values of speed, travel time, ... etc.), None if file is incorrect
        """
        if self.root is None:
            print(f"Cannot return vehicle statistics, file: '{self.file_path}' is not loaded or does not exist!")
        elif self.root.find("vehicleTripStatistics") is None:
            print(f"Cannot find xml element 'vehicleTripStatistics' in file: '{self.file_path}' !")
            return None
        return self.root.find("vehicleTripStatistics").attrib

    # ------------------------------------------ Utils  ------------------------------------------

    def compare_vehicle_stats(self, other: Union['StatisticsFile', str]) -> Optional[Dict[str, str]]:
        """
        :param other: statistics file (can also be name of file)
        :return: Dictionary mapping value of differences (with respect to self), None in case error occurred
        """
        # check type
        if not isinstance(other, StatisticsFile):
            other = StatisticsFile(other)  # Load file
        elif not isinstance(other, StatisticsFile):
            print(
                "Invalid type passed into method: 'compare_vehicle_stats', "
                f"expected [str / StatisticsFile], got: {type(other)}"
            )
            return None
        my_stats: Dict[str, str] = self.get_vehicle_stats()
        other_stats: Dict[str, str] = other.get_vehicle_stats()
        # Check vehicle statistics
        if my_stats is None:
            print(f"Statistics of file: '{self.file_path}' are of type 'None', cannot compare!")
            return None
        elif other_stats is None:
            print(f"Statistics of file: '{other.file_path}' are of type 'None', cannot compare!")
            return None
        # Compare
        # TODO dynamic spacing
        spaces: str = (" " * 5)  # Spaces for formatting
        offset: int = 25  # Spaces offset for formatting print
        print("Comparing vehicle statistics")
        print(
            f"{self.get_file_name(self.file_path)} {' ' * max(offset-len(self.get_file_name(self.file_path)), 0)} "
            f"vs{spaces}{self.get_file_name(other.file_path)}"
        )
        ret_val: Dict[str, str] = {}
        for key in set(my_stats.keys() | other_stats.keys()):
            my_val: str = my_stats.get(key, "None")
            other_val: str = other_stats.get(key, "None")
            operator: str = "?"
            diff: str = ""
            try:
                my_val_float: float = round(float(my_val), 3)
                other_val_float: float = round(float(other_val), 3)
                ret_val[key] = str(round(my_val_float - other_val_float, 3))
                diff = ", diff: " + ret_val[key]
                if my_val_float > other_val_float:
                    operator = ">"
                elif float(my_val) == float(other_val):
                    operator = "="
                else:
                    operator = "<"
            except ValueError as e:  # Unable to compare
                pass
            comparison_str: str = (
                    key + f": {my_val}" + (" " * max(offset-len(key + my_val), 0)) +
                    operator + spaces + other_val
            )
            print(comparison_str + diff)
        return ret_val

    def get_known_path(self, file_name: str) -> str:
        # Quick check
        if not file_name:
            return file_name
        # Remove extension
        file_name = file_name.replace(self.default_extension, "")
        # Search  uts/data/scenarios/simulation/statistics
        if self.file_exists(FilePaths.SCENARIO_STATISTICS.format(file_name), message=False):
            return FilePaths.SCENARIO_STATISTICS.format(file_name)
        # Does not exist, return original value
        return file_name


# For testing purposes
if __name__ == "__main__":
    temp: StatisticsFile = StatisticsFile("example")
    temp1: StatisticsFile = StatisticsFile("example_test_1")
    print(temp.get_vehicle_stats())
    print(temp1.get_vehicle_stats())
    temp.compare_vehicle_stats(temp1)


