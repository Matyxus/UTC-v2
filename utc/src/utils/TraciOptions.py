from typing import List
from utc.src.file_system import FilePaths, MyFile
from sumolib import checkBinary


class TraciOptions:
    """

    """
    def __init__(self):
        self._options: List[str] = ["-c"]
        # "--route-steps", "0",  # Force sumo to load all vehicles at once
        self._statistics: List[str] = [
            "--duration-log.statistics", "true",
            "--statistic-output",  # Path to file
            # "--tripinfo-output", "tripinfo.xml",
            # "--summary", "summary.txt"
        ]

    # -------------------------- Getters --------------------------

    def get_all(self, scenario_name: str, scenario_folder: str) -> List[str]:
        """
        :param scenario_name: name of config file
        :param scenario_folder: name of scenario folder
        :return: all options to run traci
        """
        return (
                self.get_options(scenario_name, scenario_folder) +
                self.get_statistics(scenario_name, scenario_folder)
        )

    # noinspection PyMethodMayBeStatic
    def get_display(self, display: bool):
        """
        :param display: true if simulation should be shown in SumoGui, false otherwise
        :return: SumoGui
        """
        return checkBinary("sumo-gui") if display else checkBinary("sumo")

    def get_options(self, scenario_name: str, scenario_folder: str) -> List[str]:
        """
       :param scenario_name: name of scenario
        :param scenario_folder: name of scenario folder
        :return: list containing main option to run scenario using traci
        """
        return self._options + [FilePaths.SCENARIO_CONFIG.format(scenario_folder, scenario_name)]

    def get_statistics(self, scenario_name: str, scenario_folder: str) -> List[str]:
        """
        :param scenario_name: name of scenario
        :param scenario_folder: name of scenario folder
        :return: list containing commands for traci to generate statistics file
        """
        return self._statistics + [FilePaths.SCENARIO_STATISTICS.format(scenario_folder, scenario_name)]



