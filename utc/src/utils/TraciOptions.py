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
            "--statistic-output", f"{FilePaths.SCENARIO_STATISTICS}"
            # "--tripinfo-output", "tripinfo.xml",
            # "--summary", "summary.txt"
        ]

    # -------------------------- Getters --------------------------

    def get_all(self, scenario_path: str) -> List[str]:
        """
        :param scenario_path: absolute path to scenario
        :return: all options to run traci
        """
        return self.get_options(scenario_path) + self.get_statistics(MyFile.get_file_name(scenario_path))

    # noinspection PyMethodMayBeStatic
    def get_display(self, display: bool):
        """
        :param display: true if simulation should be shown in SumoGui, false otherwise
        :return: SumoGui
        """
        return checkBinary("sumo-gui") if display else checkBinary("sumo")

    def get_options(self, scenario_path: str) -> List[str]:
        """
        :param scenario_path: absolute path to scenario
        :return: list containing main option to run scenario using traci
        """
        return self._options + [scenario_path]

    def get_statistics(self, scenario_name: str) -> List[str]:
        """
        :param scenario_name: name of scenario
        :return: list containing commands for traci to generate statistics file
        """
        self._statistics[3] = self._statistics[3].format(scenario_name)
        return self._statistics



