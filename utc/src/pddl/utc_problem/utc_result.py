from utc.src.pddl.pddl_problem import PddlResult
from utc.src.graph.components import Skeleton, Route
from utc.src.simulator.scenario.generators import RoutesGenerator, ConfigGenerator
from utc.src.utils.constants import file_exists, dir_exist, PATH, scenario_is_valid, get_file_name
from typing import Dict, List


class UtcResult(PddlResult):
    """
    Class converting 'utc' result files into '.sumocfg' files
    """

    def __init__(self, skeleton: Skeleton):
        super().__init__()
        self.skeleton: Skeleton = skeleton

    def parse_result(self, scenario_name: str, result_name: str) -> dict:
        paths: Dict[str, str] = {}
        with open(PATH.TRACI_SCENARIOS_RESULTS.format(scenario_name, result_name), "r") as file:
            for line in file:
                line = line.split()
                car_id: str = line[1]
                route_id: int = int(line[3][1:])
                if car_id not in paths:
                    paths[car_id] = ""
                paths[car_id] += (" ".join(self.skeleton.routes[route_id].get_edge_ids()) + " ")
        return paths

    def results_to_scenario(self, scenario: str, simulation: str, result_files: List[str]) -> None:
        # Checks
        if not scenario_is_valid(scenario):
            return
        elif self.skeleton is None:
            print("Skeleton of graph is None!")
            return
        unique_routes: Dict[str, str] = {}
        vehicles: Dict[str, str] = {}
        route_generator: RoutesGenerator = RoutesGenerator(routes_path=PATH.TRACI_ROUTES.format(scenario, "routes"))
        config_generator: ConfigGenerator = ConfigGenerator(PATH.TRACI_SIMULATION.format(scenario, "simulation"))
        for xml_route in route_generator.root.findall("route"):
            route_generator.root.remove(xml_route)
        for file in result_files:  # 15
            paths: Dict[str, str] = self.parse_result(scenario, file)
            for vehicle_id, route_edges in paths.items():
                route_edges = route_edges.rstrip()
                if route_edges not in unique_routes:
                    route: Route = Route(0, [self.skeleton.edges[edge_id] for edge_id in route_edges.split()])
                    tmp = route.to_xml()
                    route_generator.root.insert(0, ET.Element(tmp.tag, tmp.attrib))
                    unique_routes[route_edges] = route.attributes["id"]
                vehicles[vehicle_id] = unique_routes[route_edges]
        # Change cars routes
        for xml_vehicle in route_generator.root.findall("vehicle"):
            xml_vehicle.attrib["route"] = vehicles[xml_vehicle.attrib["id"]]
        route_generator.save(PATH.TRACI_SCENARIOS.format(scenario) + f"/planned_{routes}.ruo.xml")
        config_generator.set_routes_file(PATH.TRACI_SCENARIOS.format(scenario) + f"/planned_{routes}.ruo.xml")
        config_generator.save(PATH.TRACI_SCENARIOS.format(scenario) + f"/planned_{simulation}.ruo.xml")


