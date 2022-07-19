from Project.Pddl.pddl_problem import PddlResult
from typing import Dict


class UtcResult(PddlResult):
    """

    """

    def __init__(self):
        super().__init__()

    def parse_result(self, scenario_name: str, result_name: str) -> dict:
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
        unique_routes: Dict[str, str] = {}
        vehicles: Dict[str, str] = {}
        root = self.route_generator.root
        for xml_route in root.findall("route"):
            root.remove(xml_route)
        # Cars and their routes
        for i in range(interval):  # 15
            file: str = f"result{i * 20}_{i * 20 + 20}.1"
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
        self.route_generator.save(PATH.TRACI_SCENARIOS.format(scenario_name) + "/routes1.ruo.xml")


