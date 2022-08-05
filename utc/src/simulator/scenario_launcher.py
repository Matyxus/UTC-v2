from utc.src.ui import UserInterface
from utc.src.file_system import MyFile, FilePaths, InfoFile
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
        # Info file
        self.info_file = InfoFile("")
        self.info_file.allow_commands(
            ["generate-scenario", "add-cars", "add-random-flow",
             "add-uniform-flow", "add-random-trips", "save"]
        )

    # ---------------------------------- Commands ----------------------------------

    def generate_scenario_command(self, scenario_name: str, network_name: str) -> None:
        """
        :param scenario_name: name of scenario folder
        :param network_name: name of network on which simulation will be displayed
        :return: None
        """
        if not MyFile.file_exists(FilePaths.NETWORK_SUMO_MAPS.format(network_name)):
            return
        elif MyFile.file_exists(FilePaths.SCENARIO_SIM_GENERATED.format(scenario_name), message=False):
            print(
                f"Scenario named: {scenario_name} already exists in:"
                f" {FilePaths.SCENARIO_SIM_GENERATED.format(scenario_name)}, choose different name!"
            )
            return
        # Scenario
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
        # Save scenario
        self.scenario.save()
        # Save info file
        self.info_file.save(FilePaths.SCENARIO_SIM_INFO.format(self.scenario.name))
        self.info_file.clear()
        # Reset
        self.scenario = None
        self.remove_commands(list(self.generating_commands.keys()))


if __name__ == "__main__":
    scenario_launcher: ScenarioLauncher = ScenarioLauncher()
    scenario_launcher.run()

