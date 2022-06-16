from typing import List, Tuple, Dict
from Project.Simplify.Components import Graph, Route
from Project.Utils.constants import file_exists, PATH
from Project.Pddl.Domain import UtcProblem
from Project.Traci.scenarios.sumo_xml.generators import RoutesGenerator
import xml.etree.ElementTree as ET
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

    def parse_result(self, scenario_name: str, result_name: str) -> Dict[str, str]:
        """
        :param scenario_name:
        :param result_name:
        :return:
        """
        paths: Dict[str, str] = {}
        with open(PATH.TRACI_SCENARIOS_RESULTS.format(scenario_name, result_name), "r") as file:
            for line in file:
                line = line.split()
                car_id: str = line[1]
                route_id: int = int(line[3][1:])
                if car_id not in paths:
                    paths[car_id] = ""
                paths[car_id] += (" ".join(self.graph.skeleton.routes[route_id].get_edge_ids()) + " ")
        return paths

    def results_to_scenario(self, scenario_name: str) -> None:
        """
        :param scenario_name:
        :return:
        """
        unique_routes: Dict[str, str] = {}
        vehicles: Dict[str, str] = {}
        self.route_parser.load_routes(PATH.TRACI_SCENARIOS.format(scenario_name)+"/routes.ruo.xml")
        root = self.route_parser.tree.getroot()
        for xml_route in root.findall("route"):
            root.remove(xml_route)
        # Cars and their routes
        for i in range(15):  # 15
            file: str = ""
            if file_exists(PATH.TRACI_SCENARIOS_RESULTS.format(scenario_name, f"result{i * 20}_{i * 20 + 20}.2")):
                file = f"result{i * 20}_{i * 20 + 20}.2"
            else:
                file = f"result{i * 20}_{i * 20 + 20}.1"
            paths: Dict[str, str] = self.parse_result(scenario_name, file)
            for vehicle_id, route_edges in paths.items():
                route_edges = route_edges.rstrip()
                if route_edges not in unique_routes:
                    route: Route = Route(0, [self.graph.skeleton.edges[edge_id] for edge_id in route_edges.split()])
                    tmp = route.to_xml()
                    root.insert(0, ET.Element(tmp.tag, tmp.attrib))
                    unique_routes[route_edges] = route.attributes["id"]
                vehicles[vehicle_id] = unique_routes[route_edges]
        # Change cars routes
        for xml_vehicle in root.findall("vehicle"):
            xml_vehicle.attrib["route"] = vehicles[xml_vehicle.attrib["id"]]
        self.route_parser.save(PATH.TRACI_SCENARIOS.format(scenario_name)+"/routes2.ruo.xml")

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
        except subprocess.TimeoutExpired as callProcessErr:
            print(f"Timeout {timeout} seconds  for command expired, exiting...")
        return success, console_output


if __name__ == "__main__":
    launcher: Pddl = Pddl()
    launcher.set_network("test2")
    launcher.results_to_scenario("test3")
    # launcher.generate_problem("test3", i*20,  i*20 + 20)
    # launcher.generate_result("test3", f"problem{i*20}_{i*20 + 20}.pddl", f"result{i*20}_{i*20 + 20}")
    # launcher.parse_result("test2", "result11_20.2")
    # launcher.parse_result("test2", "result21_30.2")

