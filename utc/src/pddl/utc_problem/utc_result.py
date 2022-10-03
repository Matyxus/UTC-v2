from utc.src.pddl.pddl_problem import PddlResult
from utc.src.graph.components import Route
from utc.src.simulator.scenario import Scenario
from utc.src.file_system import MyFile, MyDirectory, FilePaths, FileExtension
from typing import Dict, List, Set
import xml.etree.ElementTree as ET


class UtcResult(PddlResult):
    """
    Class converting 'utc' result files into '.sumocfg' files
    """

    def __init__(self, scenario: Scenario, new_scenario: str):
        super().__init__(scenario, new_scenario)

    def parse_result(self, result_name: str, *args, **kwargs) -> Dict[str, str]:
        """
        :param result_name: name of pddl result file
        :return: Dictionary mapping vehicle id to edge id's (on route)
        """
        paths: Dict[str, str] = {}
        with MyFile(FilePaths.SCENARIO_RESULTS.format(self.new_scenario, result_name), "r") as pddl_result:
            if pddl_result is None:
                return paths
            for line in pddl_result:
                line = line.split()
                car_id: str = line[1]
                route_id: str = line[3]
                if car_id not in paths:
                    paths[car_id] = ""
                paths[car_id] += (" ".join(self.scenario.graph.skeleton.routes[route_id].get_edge_ids()) + " ")
        return paths

    def results_to_scenario(self, *args, **kwargs) -> bool:
        result_folder: List[str] = MyDirectory.list_directory(FilePaths.PDDL_RESULTS + f"/{self.new_scenario}")
        if not result_folder:  # Check against None and empty
            print(f"Result directory is empty, generate results before converting to scenario!")
            return False
        elif not self.scenario:  # Check against None
            print(f"Scenario must not be of type 'None' !")
            return False
        # ------------------------------ Multiple extension ------------------------------
        # It is expected that higher the extension (be it numerical or otherwise, after sorting,
        # means better the plan), meaning lowest extension in terms of sorting has to have
        # the most amount of planned files (base line plans)
        file_extensions: Dict[str, Set[str]] = {
            extension: set(files) for extension, files in MyDirectory.group_files(result_folder).items()
        }
        if len(file_extensions.keys()) > 1:
            print(f"Found multiple extensions of pddl result files: {file_extensions.keys()}")
            print("Generating unique scenario files for each of them.")
        elif len(file_extensions.keys()) == 0:
            print("Error, expected result files to have at least one extension, found None!")
            return False
        # Currently found unique routes (default is shortest path from scenario)
        unique_routes: Dict[str, Dict[str, str]] = {
            xml_route.attrib["id"]: xml_route.attrib for xml_route
            in self.scenario.routes_generator.root.findall("route")
        }
        # Currently found edges of routes (maps edge routes to route id, default shortest path from scenario)
        edge_mapping: Dict[str, str] = {
            attrib["edges"]: route_id for route_id, attrib in unique_routes.items()
        }
        # Map of vehicle id's to route id (default is shortest path from scenario),
        # used for updating (starting from lowest pddl result extension to highest)
        vehicles: Dict[str, str] = {
            vehicle.attrib["id"]: vehicle.attrib["route"] for vehicle
            in self.scenario.routes_generator.root.findall("vehicle")
        }
        # ------------------------------ Generate scenario ------------------------------
        for extension, result_files in file_extensions.items():
            # Check for ".pddl"
            if not extension.endswith(FileExtension.PDDL):
                print(f"Invalid extension: {extension}, does not end with: {FileExtension.PDDL} !")
                continue
            extension = extension.replace(FileExtension.PDDL, "")  # Remove ".pddl" extension from files
            # Remove shortest paths (they may not be needed)
            for xml_route in self.scenario.routes_generator.root.findall("route"):
                self.scenario.routes_generator.root.remove(xml_route)
            # ------------------------------ Parse result files -----------------------------
            for result_file in result_files:
                # Add extension unless file already has one
                result_file += (extension if "." not in result_file else "")
                # Get dict mapping vehicles to their edges (on route)
                for vehicle_id, route_edges in self.parse_result(result_file).items():
                    if vehicle_id not in vehicles:
                        print(
                            f"Invalid vehicle id: '{vehicle_id}' not found "
                            f"in routes file of scenario: {self.scenario.name} !"
                        )
                        continue
                    route_edges = route_edges.rstrip()
                    # Record new route
                    if route_edges not in edge_mapping:
                        route: ET.Element = Route(
                            [self.scenario.graph.skeleton.edges[edge_id] for edge_id in route_edges.split()]
                        ).to_xml()
                        edge_mapping[route_edges] = route.attrib["id"]
                        unique_routes[route.attrib["id"]] = route.attrib
                    # Update vehicle route id
                    vehicles[vehicle_id] = edge_mapping[route_edges]
            # Add routes to scenario
            for route_id in (unique_routes.keys() & vehicles.values()):
                self.scenario.routes_generator.root.insert(1, ET.Element("route", unique_routes[route_id]))
            # Change routes for vehicles
            for xml_vehicle in self.scenario.routes_generator.root.findall("vehicle"):
                xml_vehicle.attrib["route"] = vehicles[xml_vehicle.attrib["id"]]
            # ------------------------------ Save -----------------------------
            new_scenario: str = self.new_scenario + extension.replace(".", "_")
            if not self.scenario.routes_generator.save(FilePaths.SCENARIO_ROUTES.format(new_scenario)):
                print(f"Error when saving routes file for planned scenario: {new_scenario}")
                return False
            self.scenario.config_generator.set_routes_file(new_scenario)
            if not self.scenario.config_generator.save(FilePaths.SCENARIO_SIM_PLANNED.format(new_scenario)):
                print(f"Error when saving config file for planned scenario: {new_scenario}")
                return False
            # Reload SumoRoutesFile, since we change its xml elements
            self.scenario.routes_generator.load(self.scenario.name)
        self.scenario.config_generator.set_routes_file(self.scenario.name)  # Change back routes to original
        return True


if __name__ == "__main__":
    pass

