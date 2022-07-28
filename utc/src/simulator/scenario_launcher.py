from utc.src.ui import UserInterface
from utc.src.utils.constants import file_exists, PATH
from utc.src.simulator.scenario import Scenario
from utc.src.simulator.simulation import SimulationLauncher
from typing import Dict


class ScenarioLauncher(UserInterface):
    """ Class that ask user for input related to generating SUMO scenarios, generating and running scenarios """

    def __init__(self):
        super().__init__()
        self.scenario: Scenario = None
        self.commands["generate-scenario"] = self.generate_scenario_command
        # Commands enabled when generating scenario
        self.generating_commands: Dict[str, callable] = {}
        # Launcher of scenarios and '.sumocfg' files,
        # allows to use planner to generate vehicle routes while
        # simulation runs
        self.simulation_launcher: SimulationLauncher = None

    # ---------------------------------- Commands ----------------------------------

    def generate_scenario_command(self, scenario_name: str, network_name: str) -> None:
        """
        :param scenario_name: name of scenario folder
        :param network_name: name of network on which simulation will be displayed
        :return: None
        """
        if not file_exists(PATH.NETWORK_SUMO_MAPS.format(network_name)):
            return
        self.scenario = Scenario(scenario_name, network_name)
        self.generating_commands = {
            "add-cars": self.scenario.vehicle_generator.add_vehicles,
            "add-random-flow": self.scenario.vehicle_generator.random_flow,
            "add-uniform-flow": self.scenario.vehicle_generator.uniform_flow,
            "add-random-trips": self.scenario.vehicle_generator.random_trips,
            "save": self.save_command,
            "plot": self.scenario.graph.display.plot
        }
        self.add_commands(self.generating_commands)

    def save_command(self) -> None:
        """
        :return:
        """
        self.scenario.save()
        self.scenario = None
        self.remove_commands(list(self.generating_commands.keys()))


if __name__ == "__main__":
    scenario_launcher: ScenarioLauncher = ScenarioLauncher()
    scenario_launcher.run()

