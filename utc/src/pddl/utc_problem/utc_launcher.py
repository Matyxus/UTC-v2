from utc.src.pddl.pddl_problem import PddlLauncher
from utc.src.pddl.utc_problem.utc_problem import UtcProblem
from utc.src.pddl.utc_problem.utc_result import UtcResult
from utc.src.simulator.scenario.generators import RoutesGenerator, ConfigGenerator
from utc.src.graph.components import Skeleton, Graph, Route
from utc.src.utils.constants import file_exists, get_file_extension, PATH, get_planner, get_file_name, dir_exist
from utc.src.ui import UserInterface
from typing import List, Callable, Optional, Tuple, Set, Dict
from os import listdir, rename, mkdir
import xml.etree.ElementTree as ET


class UtcLauncher(PddlLauncher):
    """ Class that implements interface methods for generating pddl problems/results """

    def __init__(self):
        super().__init__()

    def generate_problems(self, domain: str, window: int = 20, *args, **kwargs) -> None:
        """
        Generates ".pddl" problem files corresponding to loaded scenario

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param window: planning window time (seconds) corresponding to each pddl problem time
        frame in simulation (fist problem is generated from time: 0-window, second from time: window-window*2, ...)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return
        if dir_exist(self.problems_dir, message=False) and len(listdir(self.problems_dir)) != 0:
            print(f"Pddl problem files already exist in: {self.problems_dir}")
            return
        elif not self.prepare_directory("problem"):
            return
        # Initialize PddlProblem
        self.pddl_problem = UtcProblem()
        self.pddl_problem.pddl_network.process_graph(self.graph.skeleton)
        # Start generating problem files
        last_vehicle_depart: float = self.routes.get_end_time()
        interval: int = max(int(round(last_vehicle_depart / window)), 1)
        print(f"Generating {interval} problem files")
        problem_files: List[str] = []
        start_time: int = 0
        end_time: int = window
        for i in range(interval):
            self.pddl_problem.set_problem_name(f"{self.new_scenario_name}_problem{start_time}_{end_time}")
            self.pddl_problem.pddl_vehicle.add_vehicles(self.routes.get_vehicles(start_time, end_time))
            self.pddl_problem.save(
                PATH.SCENARIO_PROBLEMS.format(self.new_scenario_name, self.pddl_problem.problem_name)
            )
            if not file_exists(PATH.SCENARIO_PROBLEMS.format(self.new_scenario_name, self.pddl_problem.problem_name)):
                print(f"Error at generating: {i+1} problem file: {self.pddl_problem.problem_name}, exiting ..")
                return
            # Reset cars
            self.pddl_problem.pddl_vehicle.clear()
            print(f"Finished generating {i+1} problem file: {self.pddl_problem.problem_name}")
            problem_files.append(self.pddl_problem.problem_name)
            start_time = end_time
            end_time += window
        print("Finished generating problem files")

    def generate_results(self, planner: str, domain: str, timeout: int = 30, *args, **kwargs) -> None:
        # Checks
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return
        elif not file_exists(PATH.PDDL_DOMAINS.format(domain)):
            return
        elif not get_planner(planner):
            return
        elif not dir_exist(self.problems_dir, message=False) or len(listdir(self.problems_dir)) == 0:
            print(f"Pddl problem files must be generated before calling 'generate_results'!")
            return
        elif not self.prepare_directory("result"):
            return
        problem_files: List[str] = listdir(self.problems_dir)
        result_count: int = len(listdir(self.results_dir))  # Count of already generated result files
        if result_count != 0:
            print(f"Pddl result files already exist in: {self.results_dir}")
            return
        print(f"Generating {len(problem_files)} pddl result files from: {problem_files}")
        for index, pddl_problem in enumerate(problem_files):
            assert (
                    pddl_problem.endswith(".pddl") and
                    "problem" in pddl_problem and pddl_problem.startswith(self.new_scenario_name)
            )
            pddl_problem = get_file_name(pddl_problem)
            result_name: str = pddl_problem.replace("problem", "result")
            print(f"Generating: {result_name}")
            planner_call: str = get_planner(planner).format(
                PATH.PDDL_DOMAINS.format(domain),
                PATH.SCENARIO_PROBLEMS.format(self.new_scenario_name, pddl_problem),
                PATH.SCENARIO_RESULTS.format(self.new_scenario_name, result_name)
            )
            success, output = self.shell(planner_call, timeout)
            # If file was not generated, return (possibly low timeout)
            current_count: int = len(listdir(self.results_dir))
            if not success or not (current_count > result_count):
                print(f"Error at generating result file: {result_name}, try to increase timeout: {timeout}")
                return
            result_count = current_count
            print(f"Finished generating {index+1} result file: {result_name}")
        # Check result directory, Cerberus planner adds its own extension at the end of file
        self.check_pddl_extension(self.results_dir)
        print("Finished generating result files")

    def generate_scenario(self, *args, **kwargs) -> None:
        # Checks
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return
        elif not dir_exist(self.results_dir, message=False):
            print(f"Result directory does not exist, generate result files before converting to scenario!")
            return
        result_files: List[str] = listdir(self.results_dir)
        if not len(result_files):
            print(f"Result directory is empty, generate results before converting to scenario!")
            return
        # Check all result files for multiple extension, group them by extension
        scenarios: Dict[str, List[str]] = {
            # extension : [file1, ....]
        }
        for result_file in result_files:
            # Expecting all files to be '.pddl'
            assert (result_file.endswith(".pddl"))
            extension: str = "".join(get_file_extension(result_file))
            if extension not in scenarios:
                scenarios[extension] = []
            scenarios[extension].append(get_file_name(result_file))
        if len(scenarios.keys()) > 1:
            print(f"Found multiple extensions of pddl result files: {scenarios.keys()}")
            print("Generating '.sumocfg' files for each of them")
        for extension, result_files in scenarios.items():
            assert (extension.endswith(".pddl"))
            extension = extension.replace(".pddl", "")
            print(f"Generating scenario for extension: {extension}, result file: {result_files}")
            self.results_to_scenario(extension, result_files)

# ----------------------------------------------- Temporary -----------------------------------------------

    def parse_result(self, result_name: str) -> dict:
        """

        :param result_name: name of pddl result file
        :return: Dictionary mapping vehicle_id to edge id's
        """
        paths: Dict[str, str] = {}
        with open(PATH.SCENARIO_RESULTS.format(self.new_scenario_name, result_name), "r") as file:
            for line in file:
                line = line.split()
                car_id: str = line[1]
                route_id: int = int(line[3][1:])
                if car_id not in paths:
                    paths[car_id] = ""
                paths[car_id] += (" ".join(self.graph.skeleton.routes[route_id].get_edge_ids()) + " ")
        return paths

    def results_to_scenario(self, extension: str,  result_files: List[str]) -> None:
        """

        :param extension: extension of result_files (will be used in ".sumocfg" and "rou.xml" file names
        :param result_files: result files corresponding to extension
        :return:
        """
        unique_routes: Dict[str, str] = {}
        vehicles: Dict[str, str] = {}
        # Create new routes, config, since we modify them
        route_generator: RoutesGenerator = RoutesGenerator(
            routes_path=PATH.SCENARIO_ROUTES.format(self.simulation.name)
        )
        config_generator: ConfigGenerator = ConfigGenerator(PATH.SCENARIO_SIM_GENERATED.format(self.simulation.name))
        # Remove all routes, they will be replaced by new routes
        for xml_route in route_generator.root.findall("route"):
            route_generator.root.remove(xml_route)
        # Parse all result files (names of result files)
        for file in result_files:
            # Get dict mapping vehicles to their
            paths: Dict[str, str] = self.parse_result(file + extension)
            for vehicle_id, route_edges in paths.items():
                route_edges = route_edges.rstrip()
                # Record new route
                if route_edges not in unique_routes:
                    route: Route = Route(0, [self.graph.skeleton.edges[edge_id] for edge_id in route_edges.split()])
                    tmp = route.to_xml()
                    # Insert behind "vType"
                    route_generator.root.insert(1, ET.Element(tmp.tag, tmp.attrib))
                    unique_routes[route_edges] = route.attributes["id"]
                vehicles[vehicle_id] = unique_routes[route_edges]
        # Change cars routes
        for xml_vehicle in route_generator.root.findall("vehicle"):
            xml_vehicle.attrib["route"] = vehicles[xml_vehicle.attrib["id"]]
        extension = extension.replace(".", "_")
        route_generator.save(PATH.SCENARIO_ROUTES.format(self.new_scenario_name + extension))
        config_generator.set_routes_file(PATH.SCENARIO_ROUTES.format(self.new_scenario_name + extension))
        config_generator.save(PATH.SCENARIO_SIM_PLANNED.format(self.new_scenario_name + extension))


# For testing purposes
if __name__ == "__main__":
    tmp: UserInterface = UserInterface()
    utc_launcher: UtcLauncher = UtcLauncher()
    utc_launcher.initialize("test", "test_planned", tmp.run_command, network="test")
    # utc_launcher.generate_problems("utc")
    # utc_launcher.generate_results("merwin", "utc")
    utc_launcher.generate_scenario()
    # utc_launcher.generate_problems("test2", network="test", window=10)
    # utc_launcher.generate_results("test2", "Cerberus", "utc")

