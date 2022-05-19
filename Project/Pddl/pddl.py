from typing import List, Tuple
from Project.Simplify.Components import Graph
from Project.Utils.constants import file_exists, dir_exist, PATH
from Project.Pddl.Domain import UtcProblem
from Project.Traci.scenarios.generators.routes_generator import RoutesGenerator
import subprocess


class Pddl:
    """ Class that launches program for UTC problem.pddl generation, ask user for input """

    def __init__(self):
        super().__init__()
        # -------------- Graph --------------
        self.graph: Graph = None
        # -------------- Domain --------------
        self.generator: UtcProblem = UtcProblem()
        # -------------- Utils --------------
        self.route_parser: RoutesGenerator = RoutesGenerator()
        self.generating_problem: bool = False
        self.TIME_OUT: int = 120  # Seconds

    def set_network(self, network_name: str) -> None:
        if not file_exists(PATH.NETWORK_SUMO_MAPS.format(network_name)):
            return
        self.graph = Graph()
        self.graph.loader.load_map(network_name)
        self.graph.simplify.simplify()
        self.graph.skeleton.validate_graph()
        self.route_parser.load_network(network_name)

    def generate_problem(self, scenario_name: str, start_time: int, end_time: int) -> None:
        if self.graph is None:
            return
        # Start generator
        self.generator = UtcProblem()
        self.generator.add_network(self.graph.skeleton)
        self.generator.set_problem_name(f"problem{start_time}_{end_time}")  # Set problem name (same as file name)
        self.route_parser.load_routes(PATH.TRACI_SCENARIOS.format(scenario_name)+"/routes.ruo.xml")
        # Add vehicles
        for vehicle_id, junctions in self.route_parser.get_vehicles(start_time, end_time).items():
            print(vehicle_id, junctions)
            self.generator.add_car(vehicle_id, junctions[0], junctions[1])
        self.generator.save(PATH.TRACI_SCENARIOS_PROBLEMS.format(scenario_name, f"problem{start_time}_{end_time}.pddl"))

    def generate_result(self, scenario_name: str, problem_name: str, result_name: str) -> None:
        # Call planner
        planner_args: List[str] = [
            PATH.PDDL_DOMAINS.format("utc"),  # Domain
            PATH.TRACI_SCENARIOS_PROBLEMS.format(scenario_name, problem_name),  # Problem
            PATH.TRACI_SCENARIOS_RESULTS.format(scenario_name, result_name)  # Result
        ]
        print(f"Calling command: {PATH.PLANNERS['Merwin'].format(*planner_args)}")
        print(f"With {self.TIME_OUT} second timeout")
        success, output = self.run_commmand(PATH.PLANNERS["Merwin"].format(*planner_args), self.TIME_OUT)
        if success:
            print("Successfully created result file, printing planner output:")
            print(output)

    def parse_result(self, scenario_name: str, result_name: str) -> None:
        paths: dict = {}
        with open(PATH.TRACI_SCENARIOS_RESULTS.format(scenario_name, result_name), "r") as file:
            for line in file:
                line = line.split()
                car_id: str = line[1]
                route_id: str = line[3][1:]
                if car_id not in paths:
                    paths[car_id] = []
                paths[car_id].append(route_id)
        routes: list = []
        for car, route in paths.items():
            edges: list = []
            for route_id in route:
                for edge_id in self.graph.skeleton.routes[int(route_id)].get_edge_ids():
                    edges.append(edge_id)
            if edges not in routes:
                routes.append(edges)
            print(f"Car: {car} goes trough: route{routes.index(edges)}")
        for index, route in enumerate(routes):
            print(f"route{index}: {' '.join(route)}")
        # print(f"unique edges: {routes}")

    def run_commmand(self, command: str, timeout: int = None, encoding: str = "utf-8") -> Tuple[bool, str]:
        """
        https://stackoverflow.com/questions/41094707/setting-timeout-when-using-os-system-function

        :param command: console/terminal command string
        :param timeout: wait max timeout (seconds) for run console command (default None)
        :param encoding: console output encoding, default is utf-8
        :return: True/False on success/failure, console output as string
        """
        success: bool = False
        console_output: str = ""
        try:
            console_output_byte = subprocess.check_output(command, shell=True, timeout=timeout)
            console_output = console_output_byte.decode(encoding)  # '640x360\n'
            console_output = console_output.strip()  # '640x360'
            success = True
        except subprocess.CalledProcessError as callProcessErr:
            if callProcessErr != subprocess.TimeoutExpired:
                print(f"Error {str(callProcessErr)} for run command {command}\n\n")
        return success, console_output


if __name__ == "__main__":
    launcher: Pddl = Pddl()
    launcher.set_network("test2")
    # launcher.generate_problem("test2", 21, 30)
    # launcher.generate_result("test2", "problem21_30.pddl", "result21_30")
    launcher.parse_result("test2", "result0_10.2")
    launcher.parse_result("test2", "result11_20.2")
    launcher.parse_result("test2", "result21_30.2")
    #
    #
