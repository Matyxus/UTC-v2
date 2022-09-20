from utc.src.graph.components import Skeleton, Graph, Route
from utc.src.file_system import MyFile, InfoFile, FilePaths, ProbabilityFile
from utc.src.simulator import ScenarioMain
from typing import Dict, List, Union, Optional, Tuple


class ScenarioFactory:
    """

    """
    def __init__(self):
        self.scenario_main: ScenarioMain = None
        # True if method "initialize" was successfully called
        self.is_initialized: bool = False
        self.scenario_name: str = ""

    # -------------------------------------- Commands --------------------------------------

    def initialize(self, scenario_name: str, network_name: str) -> None:
        """
        :param scenario_name: name of scenario
        :param network_name: name of sumo network
        :return: None
        """
        self.scenario_main = ScenarioMain()
        self.scenario_main.initialize_input()
        self.scenario_main.process_input(
            "generate-scenario",
            f'scenario_name="{scenario_name}" network_name="{network_name}"'
        )
        if self.scenario_main.scenario is None:
            self.is_initialized = False
            return
        self.is_initialized = True
        self.scenario_name = scenario_name

    def add_flows(self, flows: List[Tuple[str, str]]) -> None:
        """
        Adds flows to scenario, saves scenario afterwards and
        generates statistics

        :param flows: list of tuples (flow_name, flow_args),
        same format as passed from command line / file
        :return: None
        """
        if not self.is_initialized:
            return
        for flow in flows:
            self.scenario_main.process_input("add-" + flow[0], flow[1])
        self.scenario_main.process_input("save-scenario", "")
        self.scenario_main.process_input(
            "launch-scenario",
            f'scenario_name="{self.scenario_name}" statistics="t" '
            f'display="f" traffic_lights="t"'
        )

    # -------------------------------------- Utils --------------------------------------

# For testing purposes
if __name__ == "__main__":
    temp: ScenarioFactory = ScenarioFactory()
    temp.initialize("Test", "Dejvice")

