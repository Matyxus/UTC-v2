from Project.Pddl.pddl_problem import PddlLauncher
from Project.Pddl.utc_problem.utc_problem import UtcProblem
from Project.Pddl.utc_problem.utc_result import UtcResult
from Project.Traci.scenarios.generators import RoutesGenerator, ConfigGenerator
from Project.Simplify.components import Skeleton, Graph
from Project.Utils.constants import file_exists, dir_exist, PATH, scenario_is_valid, get_file_name
from typing import List, Callable, Optional, Tuple
from os import listdir


class UtcLauncher(PddlLauncher):
    """ Class that implements interface methods for generating pddl problems/results """

    def __init__(self, shell: Callable[[str, Optional[int]], Tuple[str, bool]]):
        super().__init__(shell)
        self.route_generator: RoutesGenerator = None

    def generate_problems(self, scenario: str, network: str = "default", window: int = 20, *args, **kwargs) -> None:
        """
        :param scenario: name of scenario (must contain empty '/problems' folder)
        :param network: name of network, on which problem will be generated (if default, name of network
        is extracted from '.ruo.xml' file)
        :param window: planning window time (seconds) corresponding to each pddl problem time
        frame in simulation (fist problem is generated from time: 0-window, second from time: window-window*2, ...)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        # Checks
        if not scenario_is_valid(scenario):
            return
        # Check if '/problems' folder is empty
        file_names: List[str] = listdir(PATH.TRACI_SCENARIOS.format(scenario) + "/problems")
        print(file_names)
        if len(file_names):
            print(f"/problems folder is not empty in scenario: {scenario} -> {file_names}")
            return
        # Extract network from 'simulation.sumocfg' file
        if network == "default":
            temp: ConfigGenerator = ConfigGenerator(config_path=PATH.TRACI_SIMULATION.format(scenario, "simulation"))
            network = get_file_name(temp.get_network_name())
            if not file_exists(PATH.NETWORK_SUMO_MAPS.format(network), message=False):
                print(
                    f"Network: {network} used in simulation "
                    f"file: {PATH.TRACI_SIMULATION.format(scenario, 'simulation')} does not exist!"
                )
                return
        # Load network
        self.graph = Graph(Skeleton())
        self.graph.loader.load_map(network)
        self.graph.simplify.simplify_graph()
        self.graph.skeleton.validate_graph()
        # Generate problems
        self.pddl_problem = UtcProblem()
        self.pddl_problem.pddl_network.process_graph(self.graph.skeleton)
        self.route_generator = RoutesGenerator(routes_path=PATH.TRACI_ROUTES.format(scenario, "routes"))
        last_vehicle_depart: float = self.route_generator.get_end_time()
        print("last_vehicle_depart: ", last_vehicle_depart)
        interval: int = max(int(round(last_vehicle_depart / window)), 1)
        print(f"Generating {interval} problem files")
        start_time: int = 0
        end_time: int = window
        for i in range(interval):
            self.pddl_problem.set_problem_name(f"problem{start_time}_{end_time}")
            self.pddl_problem.pddl_vehicle.add_vehicles(self.route_generator.get_vehicles(start_time, end_time))
            self.pddl_problem.save(
                PATH.TRACI_SCENARIOS_PROBLEMS.format(scenario, f"problem{start_time}_{end_time}")
            )
            # Reset cars
            self.pddl_problem.pddl_vehicle.clear()
            print(f"Finished generating {i+1} problem file: {self.pddl_problem.problem_name}")
            start_time = end_time
            end_time += window
        print("Finished generating problem files")

    def generate_results(self, scenario: str, planner: str, *args, **kwargs) -> None:
        """

        :param scenario: name of scenario (must contain empty '/results' folder)
        :param planner: name of planner to be used (must be defined in /Project/Pddl/Utils/constants.py)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        pass

    def generate_scenario(self, scenario: str, *args, **kwargs) -> None:
        """
        :param scenario: name of scenario (must contain generated pddl files in '/results' folder)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return:
        """
        pass


# For testing purposes
if __name__ == "__main__":
    utc_launcher: UtcLauncher = UtcLauncher(None)
    utc_launcher.generate_problems("test2", network="test", window=10)

