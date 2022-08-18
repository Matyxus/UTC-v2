from utc.src.ui import UserInterface
from utc.src.file_system import MyFile, MyDirectory, FilePaths, InfoFile, SumoConfigFile
from utc.src.simulator.scenario import Scenario
import traci
from typing import Dict
from sumolib import checkBinary


class ScenarioMain(UserInterface):
    """ Class that ask user for input related to generating SUMO scenarios, generating and running scenarios """

    def __init__(self):
        super().__init__("scenario")
        self.scenario: Scenario = None
        self.commands["generate-scenario"] = self.generate_scenario_command
        self.commands["launch-scenario"] = self.launch_scenario_command
        self.commands["delete-scenario"] = self.delete_scenario_command
        # Commands enabled when generating scenario
        self.generating_commands: Dict[str, callable] = {}
        # Info file
        self.info_file = InfoFile("")
        self.info_file.add_allowed_commands(
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
            "add-cars": self.scenario.vehicle_factory.vehicle_trips.add_vehicles,
            "add-random-trips": self.scenario.vehicle_factory.vehicle_trips.random_trips,
            "add-random-flow": self.scenario.vehicle_factory.vehicle_flows.random_flow,
            "add-uniform-flow": self.scenario.vehicle_factory.vehicle_flows.uniform_flow,
            "save": self.save_command,
            "plot": self.scenario.graph.display.plot
        }
        self.add_commands(self.generating_commands)

    def launch_scenario_command(self, scenario_name: str, statistics: bool = True, display: bool = True) -> None:
        """
        :param scenario_name: name of existing scenario (can be user-generated or planned)
        :param statistics: bool, if file containing vehicle statistics should be generated (default true)
        :param display: bool, if simulation should be launched with GUI (default true)
        :return: None
        """
        # Get scenario path (can be planned or user-generated)
        scenario_path: str = SumoConfigFile(scenario_name).file_path
        if not MyFile.file_exists(scenario_path, message=False):
            print(f"Scenario named: {scenario_name} does not exist!")
            return
        sumo_run = checkBinary("sumo-gui") if display else checkBinary("sumo")
        # Basic running options
        options: list = [
            "-c", scenario_path
            # "--route-steps", "0",  # Force sumo to load all vehicles at once
        ]
        # Generate file containing vehicle statistics
        if statistics:
            options += [
                "--duration-log.statistics", "true",
                "--statistic-output", f"{FilePaths.SCENARIO_STATISTICS.format(scenario_name)}"
                # "--tripinfo-output", "tripinfo.xml",
                # "--summary", "summary.txt"
            ]
        try:
            traci.start([sumo_run, *options])
            while traci.simulation.getMinExpectedNumber() > 0:  # -> "while running.."
                # TODO online planning
                traci.simulationStep()
            traci.close()
            print(f"Simulation of scenario: '{scenario_name}' ended, exiting ...")
        except traci.exceptions.FatalTraCIError as e:
            # Closed by user
            if str(e) == "connection closed by SUMO":
                print("Closed GUI, exiting ....")
            else:
                print(f"Error occurred: {e}")

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
        if MyFile.file_exists(route_paths, message=False) and not MyFile.delete_file(route_paths):
            return
        # Delete ".info" file
        info_path: str = InfoFile(scenario_name).file_path
        if MyFile.file_exists(info_path, message=False) and not MyFile.delete_file(info_path):
            return
        # ---------------------------------- Folders ----------------------------------
        # Delete pddl problems folder (with files)
        pddl_problems: str = FilePaths.PDDL_PROBLEMS + "/" + scenario_name
        if MyDirectory.dir_exist(pddl_problems, message=False) and not MyDirectory.delete_directory(pddl_problems):
            return
        # Delete pddl results folder (with files)
        pddl_results: str = FilePaths.PDDL_RESULTS + "/" + scenario_name
        if MyDirectory.dir_exist(pddl_results, message=False) and not MyDirectory.delete_directory(pddl_results):
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
        self.remove_commands(list(self.generating_commands.keys()))


if __name__ == "__main__":
    scenario_launcher: ScenarioMain = ScenarioMain()
    scenario_launcher.run()

