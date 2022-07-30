from utc.src.pddl.pddl_problem import PddlResult
from utc.src.graph.components import Route
from utc.src.simulator.scenario import Scenario
from utc.src.file_system import MyFile, MyDirectory, FilePaths, FileExtension
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET


class UtcResult(PddlResult):
    """
    Class converting 'utc' result files into '.sumocfg' files
    """

    def __init__(self, scenario: Scenario, new_scenario: str):
        super().__init__(scenario, new_scenario)

    def parse_result(self, result_name: str, *args, **kwargs) -> dict:
        """

        :param result_name: name of pddl result file
        :return: Dictionary mapping vehicle_id to edge id's
        """
        paths: Dict[str, str] = {}
        with MyFile(FilePaths.SCENARIO_RESULTS.format(self.new_scenario, result_name), "r") as pddl_result:
            if pddl_result is None:
                return paths
            for line in pddl_result:
                line = line.split()
                car_id: str = line[1]
                route_id: int = int(line[3][1:])
                if car_id not in paths:
                    paths[car_id] = ""
                paths[car_id] += (" ".join(self.scenario.graph.skeleton.routes[route_id].get_edge_ids()) + " ")
        return paths

    def results_to_scenario(self, *args, **kwargs) -> None:
        result_files: Optional[List[str]] = MyDirectory.list_directory(FilePaths.PDDL_RESULTS + f"/{self.new_scenario}")
        if not result_files:  # Check against None and empty
            print(f"Result directory is empty, generate results before converting to scenario!")
            return
        elif not self.scenario:
            print(f"Scenario must not be of type 'None' !")
            return
        # ------------------------------ Multiple extension ------------------------------
        file_extensions: Dict[str, List[str]] = MyDirectory.group_files(result_files)
        if len(file_extensions.keys()) > 1:
            print(f"Found multiple extensions of pddl result files: {file_extensions.keys()}")
            print("Generating unique scenario files for each of them")
        # ------------------------------ Generate scenario ------------------------------
        for extension, result_files in file_extensions.items():
            assert (extension.endswith(FileExtension.PDDL))
            extension = extension.replace(FileExtension.PDDL, "")  # Remove ".pddl" extension from files
            print(
                f"Generating scenario for extension: '{FileExtension.PDDL if not extension else extension}',"
                f" result files: {result_files}"
            )
            # ------------------------------ Initialize ------------------------------
            unique_routes: Dict[str, str] = {}
            vehicles: Dict[str, str] = {}
            # ------------------------------ Parse result files -----------------------------
            # Remove all routes, they will be replaced by new routes
            for xml_route in self.scenario.routes_generator.root.findall("route"):
                self.scenario.routes_generator.root.remove(xml_route)
            # Parse all result files (names of result files)
            for result_file in result_files:
                # Get dict mapping vehicles to their
                paths: Dict[str, str] = self.parse_result(MyFile.get_file_name(result_file) + extension)
                for vehicle_id, route_edges in paths.items():
                    route_edges = route_edges.rstrip()
                    # Record new route
                    if route_edges not in unique_routes:
                        route: Route = Route(
                            0, [self.scenario.graph.skeleton.edges[edge_id] for edge_id in route_edges.split()]
                        )
                        tmp = route.to_xml()
                        # Insert behind "vType"
                        self.scenario.routes_generator.root.insert(1, ET.Element(tmp.tag, tmp.attrib))
                        unique_routes[route_edges] = route.attributes["id"]
                    vehicles[vehicle_id] = unique_routes[route_edges]
            # Change cars routes
            for xml_vehicle in self.scenario.routes_generator.root.findall("vehicle"):
                xml_vehicle.attrib["route"] = vehicles[xml_vehicle.attrib["id"]]
            # ------------------------------ Save -----------------------------
            new_scenario: str = self.new_scenario + extension.replace(".", "_")
            if not self.scenario.routes_generator.save(
                    FilePaths.SCENARIO_ROUTES.format(new_scenario)
                    ):
                print(f"Error when saving routes file for planned scenario: {new_scenario}")
                return
            self.scenario.config_generator.set_routes_file(new_scenario)
            if not self.scenario.config_generator.save(FilePaths.SCENARIO_SIM_PLANNED.format(new_scenario)):
                print(f"Error when saving config file for planned scenario: {new_scenario}")
                return
            # Reload SumoRoutesFile, since we change its xml elements
            self.scenario.routes_generator.load(self.scenario.name)
        self.scenario.config_generator.set_routes_file(self.scenario.name)  # Change back routes to original


if __name__ == "__main__":
    temp: UtcResult = UtcResult(Scenario("example", "test"), "example_test")
    temp.results_to_scenario()

