from utc.src.pddl.pddl_problem import PddlResult
from utc.src.graph.components import Route
from utc.src.simulator.scenario import Scenario, RoutesGenerator, ConfigGenerator
from utc.src.utils.constants import PATH, dir_exist
from typing import Dict, List
import xml.etree.ElementTree as ET
from os import listdir


class UtcResult(PddlResult):
    """
    Class converting 'utc' result files into '.sumocfg' files
    """

    def __init__(self, scenario: Scenario):
        super().__init__(scenario)

    def parse_result(self, result_name: str, *args, **kwargs) -> dict:
        """

        :param result_name: name of pddl result file
        :return: Dictionary mapping vehicle_id to edge id's
        """
        paths: Dict[str, str] = {}
        with open(PATH.SCENARIO_RESULTS.format(self.scenario.name, result_name), "r") as file:
            for line in file:
                line = line.split()
                car_id: str = line[1]
                route_id: int = int(line[3][1:])
                if car_id not in paths:
                    paths[car_id] = ""
                paths[car_id] += (" ".join(self.scenario.graph.skeleton.routes[route_id].get_edge_ids()) + " ")
        return paths

    def results_to_scenario(self, new_scenario: str, *args, **kwargs) -> None:
        assert (dir_exist(PATH.CWD + f"/data/scenarios/results/{new_scenario}"))
        result_files: List[str] = listdir(PATH.CWD + f"/data/scenarios/results/{new_scenario}")
        if not len(result_files):
            print(f"Result directory is empty, generate results before converting to scenario!")
            return
        # ------------------------------ Multiple extension ------------------------------
        file_extensions: Dict[str, List[str]] = self.group_result_files(result_files)
        if len(file_extensions.keys()) > 1:
            print(f"Found multiple extensions of pddl result files: {file_extensions.keys()}")
            print("Generating unique '.sumocfg' files for each of them")
        # ------------------------------ Generate scenario ------------------------------
        for extension, result_files in file_extensions.items():
            print(
                f"Generating scenario for extension: {'.pddl' if not extension else extension},"
                f" result files: {result_files}"
            )
            # ------------------------------ Initialize ------------------------------
            unique_routes: Dict[str, str] = {}
            vehicles: Dict[str, str] = {}
            # Create new routes & config, since we modify them
            route_generator: RoutesGenerator = RoutesGenerator(
                routes_path=PATH.SCENARIO_ROUTES.format(self.scenario.name)
            )
            config_generator: ConfigGenerator = ConfigGenerator(PATH.SCENARIO_SIM_GENERATED.format(self.scenario.name))
            # ------------------------------ Parse result files -----------------------------
            # Remove all routes, they will be replaced by new routes
            for xml_route in route_generator.root.findall("route"):
                route_generator.root.remove(xml_route)
            # Parse all result files (names of result files)
            for result_name in result_files:
                # Get dict mapping vehicles to their
                paths: Dict[str, str] = self.parse_result(result_name + extension)
                for vehicle_id, route_edges in paths.items():
                    route_edges = route_edges.rstrip()
                    # Record new route
                    if route_edges not in unique_routes:
                        route: Route = Route(
                            0, [self.scenario.graph.skeleton.edges[edge_id] for edge_id in route_edges.split()]
                        )
                        tmp = route.to_xml()
                        # Insert behind "vType"
                        route_generator.root.insert(1, ET.Element(tmp.tag, tmp.attrib))
                        unique_routes[route_edges] = route.attributes["id"]
                    vehicles[vehicle_id] = unique_routes[route_edges]
            # Change cars routes
            for xml_vehicle in route_generator.root.findall("vehicle"):
                xml_vehicle.attrib["route"] = vehicles[xml_vehicle.attrib["id"]]
            extension = extension.replace(".", "_")
            # ------------------------------ Save -----------------------------
            route_generator.save(PATH.SCENARIO_ROUTES.format(new_scenario + extension))
            config_generator.set_routes_file(PATH.SCENARIO_ROUTES.format(new_scenario + extension))
            config_generator.save(PATH.SCENARIO_SIM_PLANNED.format(new_scenario + extension))
