from Project.Traci.scenarios.generators.generator import Generator
from Project.Utils.constants import PATH
from typing import Dict, Tuple
from Project.Traci.simulation import VehicleGenerator
from Project.Simplify.components import Graph


class RoutesGenerator(Generator):
    """ Class that generates '.rou.xml' files for SUMO """

    def __init__(self, graph: Graph = None, routes_path: str = PATH.SUMO_ROUTES_TEMPLATE):
        """
        :param graph: graph of road network (default None)
        :param routes_path: path of '.route.xml' file
        """
        super().__init__(routes_path)
        assert (self.tree is not None)
        assert (self.root is not None)
        # Class handling generation of vehicles and routes
        self.vehicle_generator: VehicleGenerator = VehicleGenerator(graph)
        # Memory of previously searched vehicles (end_time, index)
        self.previous_search: Tuple[int, int] = (0, 0)


    # ------------------------------------------Load & Save ------------------------------------------

    def load(self, file_path: str) -> None:
        if ".ruo.xml" not in file_path and file_path != PATH.SUMO_ROUTES_TEMPLATE:
            print("File must be of type '.ruo.xml'!")
            return
        super().load(file_path)

    def save(self, file_path: str) -> None:
        # Append routes (before vehicles!)
        for route in self.vehicle_generator.routes:
            self.root.append(route.to_xml())
        # Append vehicles
        self.vehicle_generator.save(self.root)
        super().save(file_path)

    # ------------------------------------------ Utils  ------------------------------------------

    def get_end_time(self) -> int:
        """
        :return: Last vehicle arrival time (-1 if no vehicles are found)
        """
        if not len(self.root.findall("vehicle")):
            return -1
        return int(self.root.findall("vehicle")[-1].attrib["depart"])

    def get_vehicles(self, start_time: int, end_time: int) -> Dict[str, Tuple[str, str]]:
        """
        Extracts vehicles from '.ruo.xml' file, filtered by start/end time as <start_time, end_time)

        :param start_time: earliest vehicle arrival
        :param end_time: latest vehicle arrival (without) -> (end_time-1) is the latest arrival of vehicle
        :return: Vehicle dictionary mapping vehicle id to initial and ending junctions of its route
        """
        print("Parsing vehicles")
        vehicles: Dict[str, Tuple[str, str]] = {}
        if self.tree is None:
            print("XML Tree is not set!")
            return vehicles
        routes: Dict[str, Tuple[str, str]] = {}
        # Routes mapping (id: from, to)
        for route in self.root.findall("route"):
            routes[route.attrib["id"]] = (route.attrib["fromJunction"], route.attrib["toJunction"])
        # Find if previous end_time is less than or equal to current start_time, if so
        # get saved index of last vehicle
        search_start: int = 0
        if self.previous_search is not None and self.previous_search[0] <= start_time:
            search_start = self.previous_search[1]  # Index
        # Vehicles
        for index, vehicle in enumerate(self.root.findall("vehicle")[search_start:]):
            if start_time <= int(vehicle.attrib["depart"]) < end_time:
                vehicles[vehicle.attrib["id"]] = routes[vehicle.attrib["route"]]
            elif int(vehicle.attrib["depart"]) >= end_time:
                self.previous_search = (end_time, index)
                break
        return vehicles


# For testing purposes
if __name__ == "__main__":
    temp: RoutesGenerator = RoutesGenerator(routes_path=PATH.TRACI_SCENARIOS.format(""))

