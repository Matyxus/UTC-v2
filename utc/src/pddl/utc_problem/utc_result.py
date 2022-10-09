from utc.src.pddl.pddl_problem import PddlResult
from utc.src.graph.components import Route, Skeleton
from utc.src.simulator.scenario import Scenario
from utc.src.file_system import MyFile, MyDirectory, FilePaths, FileExtension
from typing import Dict, List, Set
import xml.etree.ElementTree as ET


class UtcResult(PddlResult):
    """
    Class converting 'utc' result files into '.sumocfg' files
    """
    def __init__(self, scenario: Scenario, skeleton: Skeleton):
        super().__init__(scenario,  skeleton)

    def parse_result(self, result_name: str, *args, **kwargs) -> Dict[str, str]:
        """
        :param result_name: name of pddl result file
        :return: Dictionary mapping vehicle id to edge id's (on route)
        """
        paths: Dict[str, str] = {}
        # Check
        result_path: str = FilePaths.PDDL_RESULT.format(self.scenario.scenario_folder, self.scenario.name, result_name)
        if not MyFile.file_exists(result_path):
            return paths
        with open(result_path, "r") as pddl_result:
            for line in pddl_result:
                line = line.split()
                car_id: str = line[1]
                route_id: str = line[3]
                if car_id not in paths:
                    paths[car_id] = ""
                paths[car_id] += (" ".join(self.skeleton.routes[route_id].get_edge_ids()) + " ")
        return paths

    def results_to_scenario(self, *args, generate_best: bool = True, **kwargs) -> bool:
        result_folder: List[str] = self.scenario.results_dir.get_files(extension=True)
        if result_folder is None or not result_folder:  # Check against None and empty
            print(f"Result directory is empty, generate results before converting to scenario!")
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
            print(f"Error, expected result files to have at least one extension: {FileExtension.PDDL}, found 0!")
            return False
        # Currently found unique routes (default is shortest path from scenario)
        unique_routes: Dict[str, Dict[str, str]] = {
            xml_route.attrib["id"]: xml_route.attrib for xml_route
            in self.scenario.routes_file.root.findall("route")
        }
        # Currently found edges of routes (maps edge routes to route id, default shortest path from scenario)
        edge_mapping: Dict[str, str] = {
            attrib["edges"]: route_id for route_id, attrib in unique_routes.items()
        }
        # Map of vehicle id's to route id (default is shortest path from scenario),
        # used for updating (starting from lowest pddl result extension to highest)
        vehicles: Dict[str, str] = {
            vehicle.attrib["id"]: vehicle.attrib["route"] for vehicle
            in self.scenario.routes_file.root.findall("vehicle")
        }
        # ------------------------------ Generate scenario ------------------------------
        for index, (extension, result_files) in enumerate(file_extensions.items()):
            # Check for ".pddl"
            if not extension.endswith(FileExtension.PDDL):
                print(f"Invalid extension: {extension}, does not end with: {FileExtension.PDDL} !")
                continue
            extension = extension.replace(FileExtension.PDDL, "")  # Remove ".pddl" extension from files

            # ------------------------------ Parse result files -----------------------------
            for result_file in result_files:
                # Add extension unless file already has one
                result_file += (extension if "." not in result_file else "")
                # Get dict mapping vehicles to their edges (on route)
                for vehicle_id, route_edges in self.parse_result(result_file).items():
                    if vehicle_id not in vehicles:
                        print(
                            f"Invalid vehicle id: '{vehicle_id}' not found "
                            f"in routes file of scenario: {self.scenario.scenario_folder} !"
                        )
                        continue
                    route_edges = route_edges.rstrip()
                    # Record new route
                    if route_edges not in edge_mapping:
                        route: ET.Element = Route(
                            [self.skeleton.edges[edge_id] for edge_id in route_edges.split()]
                        ).to_xml()
                        edge_mapping[route_edges] = route.attrib["id"]
                        unique_routes[route.attrib["id"]] = route.attrib
                    # Update vehicle route id
                    vehicles[vehicle_id] = edge_mapping[route_edges]
            # Change routes for vehicles
            for xml_vehicle in self.scenario.routes_file.root.findall("vehicle"):
                xml_vehicle.attrib["route"] = vehicles[xml_vehicle.attrib["id"]]
            # If we only want to save the best result parse others first
            if generate_best and index != (len(file_extensions.keys())-1):
                continue
            # Remove shortest paths (they may not be needed)
            for xml_route in self.scenario.routes_file.root.findall("route"):
                self.scenario.routes_file.root.remove(xml_route)
            # Add routes to scenario
            for route_id in (unique_routes.keys() & vehicles.values()):
                self.scenario.routes_file.root.insert(1, ET.Element("route", unique_routes[route_id]))
            # ------------------------------ Save -----------------------------
            # If we only have '.pddl' extension, new_scenario will be the same as scenario_name
            new_scenario: str = self.scenario.name + extension.replace(".", "_")
            if not self.scenario.routes_file.save(
                    FilePaths.SCENARIO_ROUTES.format(self.scenario.scenario_folder, new_scenario)
                    ):
                print(f"Error when saving routes file for planned scenario: {new_scenario}")
                return False
            self.scenario.config_file.set_routes_file(new_scenario)
            if not self.scenario.config_file.save(
                    FilePaths.SCENARIO_CONFIG.format(self.scenario.scenario_folder, new_scenario)
                    ):
                print(f"Error when saving config file for planned scenario: {new_scenario}")
                return False
            # Reload the original SumoRoutesFile, since we change its xml elements
            self.scenario.routes_file.reload()
        self.scenario.config_file.set_routes_file(self.scenario.scenario_folder)  # Change back routes to original
        return True


if __name__ == "__main__":
    pass

