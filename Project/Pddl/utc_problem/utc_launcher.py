from Project.Pddl.pddl_problem import PddlLauncher
from Project.Pddl.utc_problem.utc_problem import UtcProblem
from Project.Pddl.utc_problem.utc_result import UtcResult
from Project.Traci.scenarios.generators import RoutesGenerator
from Project.Simplify.components import Skeleton, Graph
from Project.Utils.constants import file_exists, get_file_extension, PATH, scenario_is_valid, get_file_name
from Project.Pddl.Utils import PLANNERS
from typing import List, Callable, Optional, Tuple, Set
from os import listdir, rename


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
        network = self.get_network(scenario, network)
        file_names: List[str] = listdir(PATH.TRACI_SCENARIOS.format(scenario) + "/problems")
        # Checks
        if not scenario_is_valid(scenario):
            return
        elif not network:
            return
        elif len(file_names):  # Check if '/problems' folder is empty
            print(f"/problems folder is not empty in scenario: {scenario} -> {file_names}")
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

    def generate_results(self, scenario: str, planner: str, domain: str, timeout: int = 30, *args, **kwargs) -> None:
        # Checks
        if not scenario_is_valid(scenario):
            return
        file_names: List[str] = listdir(PATH.TRACI_SCENARIOS.format(scenario) + "/problems")
        if not len(file_names):
            print(f"No problem files found in: {file_names}!")
            return
        elif not file_exists(PATH.PDDL_DOMAINS.format(domain)):
            return
        elif self.shell is None:
            print(f"Shell method is None!")
            return
        elif planner not in PLANNERS:
            return
        print(f"Generating {len(file_names)} pddl result files from: {file_names}")
        result_files: Set[str] = set()
        for pddl_problem in file_names:
            pddl_problem = get_file_name(pddl_problem)
            result_name: str = pddl_problem.replace("problem", "result")
            print(f"Generating: {result_name}")
            planner_args: List[str] = self.get_planner_args(
                domain, scenario, pddl_problem, result_name
            )
            success, output = self.shell(PLANNERS[planner].format(*planner_args), timeout)
            # If file was not generated, return
            new_result_files: Set[str] = set(listdir(PATH.TRACI_SCENARIOS.format(scenario) + "/results"))
            if not len(new_result_files) > len(result_files) or not success:
                print(f"Unable to generate {result_name}, try increasing timeout")
                return
            new_file_name: str = ""
            # Iterate over newly generated files
            for file in (result_files ^ new_result_files):
                # File correctly ends with '.pddl'
                if file.endswith(".pddl"):
                    continue
                file = (PATH.TRACI_SCENARIOS.format(scenario) + "/results/" + file)
                print(f"Incorrect extension found in pddl result file: {file}")
                # File does not end with '.pddl'
                if ".pddl" in file:  # '.pddl' suffix is not at the end
                    new_file_name: str = file.replace(".pddl", "")
                new_file_name += ".pddl"
                print(f"Renaming to: {new_file_name}")
                rename(file, new_file_name)
            result_files = new_result_files
            print(f"Finished generating: {result_name}")

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
    # utc_launcher.generate_problems("test2", network="test", window=10)
    # utc_launcher.generate_results("test2", "Cerberus", "utc")

