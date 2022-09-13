from utc.src.ui import UserInterface, Command
from utc.src.file_system import MyFile, MyDirectory, FilePaths, InfoFile, SumoConfigFile
from utc.src.simulator.scenario import Scenario
from utc.src.utils import TraciOptions
import traci
from typing import List


class ScenarioMain(UserInterface):
    """ Class that ask user for input related to generating SUMO scenarios, generating and running scenarios """

    def __init__(self):
        super().__init__("scenario")
        self.scenario: Scenario = None
        # Commands enabled when generating scenario + method for generating vehicles
        self.generating_commands: List[str] = ["save-scenario", "plot"]
        # Info file
        self.info_file = InfoFile("")
        self.info_file.add_allowed_commands(
            ["generate-scenario", "save-scenario"]
        )

    # ---------------------------------- Commands ----------------------------------

    def initialize_commands(self) -> None:
        super().initialize_commands()
        self.user_input.add_command([
            ("generate-scenario", Command("generate-scenario", self.generate_scenario_command)),
            ("launch-scenario", Command("launch-scenario", self.launch_scenario_command)),
            ("delete-scenario", Command("delete-scenario", self.delete_scenario_command))
        ])

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
        # Add vehicle commands to generating commands and info file (only once)
        if len(self.generating_commands) == 2:
            vehicle_commands: List[str] = list(self.scenario.vehicle_factory.get_methods().keys())
            self.generating_commands.extend(vehicle_commands)
            self.info_file.add_allowed_commands(vehicle_commands)
        # Add new commands
        self.user_input.add_command([
            (command_name, Command(command_name, function)) for command_name, function
            in self.scenario.vehicle_factory.get_methods().items()
        ])
        self.user_input.add_command([
            ("save-scenario", Command("save-scenario", self.save_command)),
            ("plot-scenario", Command("plot-scenario", self.scenario.graph.display.plot))
        ])

    # noinspection PyMethodMayBeStatic
    def launch_scenario_command(
            self, scenario_name: str, statistics: bool = True,
            display: bool = True, traffic_lights: bool = True
            ) -> None:
        """
        :param scenario_name: name of existing scenario (can be user-generated or planned)
        :param statistics: bool, if file containing vehicle statistics should be generated (default true)
        :param display: bool, if simulation should be launched with GUI (default true)
        :param traffic_lights: bool, fi simulation should use traffic lights (default true)
        :return: None
        """
        # Get scenario path (can be planned or user-generated)
        scenario_path: str = SumoConfigFile(scenario_name).file_path
        if not MyFile.file_exists(scenario_path, message=False):
            print(f"Scenario named: {scenario_name} does not exist!")
            return
        traci_options: TraciOptions = TraciOptions()
        options: List[str] = traci_options.get_options(scenario_path)
        if statistics:
            options += traci_options.get_statistics(scenario_name)
        try:
            traci.start([traci_options.get_display(display), *options])
            # Turn of traffic lights
            if not traffic_lights:
                for traffic_light_id in traci.trafficlight.getIDList():
                    traci.trafficlight.setProgram(traffic_light_id, "off")
            while traci.simulation.getMinExpectedNumber() > 0:  # -> "while running.."
                traci.simulationStep()
            traci.close()
            print(f"Simulation of scenario: '{scenario_name}' ended, exiting ...")
        except traci.exceptions.FatalTraCIError as e:
            # Closed by user
            if str(e) == "connection closed by SUMO":
                print("Closed GUI, exiting ....")
            else:
                print(f"Error occurred: {e}")

    # noinspection PyMethodMayBeStatic
    def delete_scenario_command(self, scenario_name: str) -> None:
        """
        Deletes scenario and associated files (pddl, routes, info)

        :param scenario_name: name of scenario
        :return: None
        """
        print(f"Proceeding to delete scenario: '{scenario_name}' and associated files")
        scenario_path: str = SumoConfigFile(scenario_name).file_path
        if not MyFile.file_exists(scenario_path):
            return
        # ---------------------------------- Files ----------------------------------
        # Delete ".sumocfg" file
        if not MyFile.delete_file(scenario_path):
            return
        # Delete ".rou.xml" file
        route_paths: str = FilePaths.SCENARIO_ROUTES.format(scenario_name)
        if not MyFile.delete_file(route_paths):
            return
        # Delete ".info" file
        info_path: str = InfoFile(scenario_name).file_path
        if not MyFile.delete_file(info_path):
            return
        # ---------------------------------- Folders ----------------------------------
        # Delete pddl problems folder (with files)
        pddl_problems: str = FilePaths.PDDL_PROBLEMS + "/" + scenario_name
        if not MyDirectory.delete_directory(pddl_problems):
            return
        # Delete pddl results folder (with files)
        pddl_results: str = FilePaths.PDDL_RESULTS + "/" + scenario_name
        if not MyDirectory.delete_directory(pddl_results):
            return
        print(f"Successfully deleted scenario: '{scenario_name}' and associated files")

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
        self.user_input.remove_command(self.generating_commands)


if __name__ == "__main__":
    scenario_launcher: ScenarioMain = ScenarioMain()
    scenario_launcher.run()

