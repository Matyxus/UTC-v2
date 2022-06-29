from typing import List, Tuple, Dict
from Project.Simplify.components import Graph, Route
from Project.Utils.constants import file_exists, dir_exist, PATH
from Project.Pddl.Domain import UtcProblem
from Project.Traci.scenarios.generators import RoutesGenerator
from Project.UI import UserInterface
import xml.etree.ElementTree as ET


class PddlLauncher(UserInterface):
    """ Class that launches program for UTC problem.pddl generation, ask user for input """

    def __init__(self):
        super().__init__()
        # -------------- Graph --------------
        self.graph: Graph = None
        # -------------- Domain --------------
        self.generator: UtcProblem = UtcProblem()
        # -------------- Utils --------------
        self.route_generator: RoutesGenerator = RoutesGenerator()
        self.generating_problem: bool = False
        self.TIME_OUT: int = 60  # Seconds
        # -------------- Commands --------------
        self.commands["generate_plan"] = self.generate_plan

    def generate_plan(
            self, network_name: str, scenario_name: str, planner: str,
            domain: str = "utc", window: int = 20, keep_files: bool = True
            ) -> None:
        """

        :param network_name: name of network, on which problem will be generated
        :param scenario_name: name of scenario
        :param domain: name of pddl domain
        :param planner: name of planner
        :param window: planning window time (seconds) corresponding to each pddl problem time
        frame in simulation (fist problem is generated from time: 0-window, second from time: window-window*2, ...)
        :param keep_files: bool (true/false) if pddl problems and result files should saved
        :return: None
        """
        # Checks
        if not file_exists(PATH.NETWORK_SUMO_MAPS.format(network_name)):
            return
        elif not dir_exist(PATH.TRACI_SCENARIOS.format(scenario_name)):
            return
        elif not window > 0:
            print("Planning window time must be higher than 0")
            return
        elif not file_exists(PATH.PDDL_DOMAINS.format(domain)):
            return
        elif scenario_name not in PATH.PLANNERS:
            print(f"Planner: {scenario_name} does not exist!")
            return
        # Load network
        self.graph = Graph()
        self.graph.loader.load_map(network_name)
        self.graph.simplify.simplify_graph()
        self.graph.skeleton.validate_graph()
        # Generate problems

        # Generate results

        # Convert results to '.sumocfg' files (possible multiple, if planner generated more solutions)



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


# Program start
if __name__ == "__main__":
    launcher: PddlLauncher = PddlLauncher()
    launcher.run()
