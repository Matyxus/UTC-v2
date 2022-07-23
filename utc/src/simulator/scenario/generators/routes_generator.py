from utc.src.simulator.scenario.generators.generator import Generator
from utc.src.utils.constants import PATH
from typing import Dict, Tuple
from utc.src.simulator.simulation import VehicleGenerator
from utc.src.graph.components import Graph


class RoutesGenerator(Generator):
    """ Class that generates '.rou.xml' files for SUMO """

    def __init__(self, graph: Graph = None, routes_path: str = PATH.SUMO_ROUTES_TEMPLATE):
        """
        :param graph: graph of road network (default None)
        :param routes_path: path of '.route.xml' file
        """
        super().__init__(routes_path)
        # Check template
        assert (self.tree is not None)
        assert (self.root is not None)
        assert (self.root.find("vType") is not None)
        assert (self.root.find("vType").attrib["id"] == "CarDefault")
        # Class handling generation of vehicles and routes
        self.vehicle_generator: VehicleGenerator = VehicleGenerator(graph)
        # Memory of previously searched vehicles (end_time, index)
        self.previous_search: Tuple[int, int] = (0, 0)

    # ------------------------------------------Load & Save ------------------------------------------

    def load(self, file_path: str) -> None:
        if ".rou.xml" not in file_path and file_path != PATH.SUMO_ROUTES_TEMPLATE:
            print("File must be of type '.rou.xml'!")
            return
        super().load(file_path)

    def save(self, file_path: str) -> None:
        # Append vehicles
        self.vehicle_generator.save(self.root)
        super().save(file_path)

    # ------------------------------------------ Utils  ------------------------------------------

    def has_vehicles(self) -> bool:
        """
        :return: True if there are any xml elements of tag "vehicle", false otherwise
        """
        return self.root.find("vehicle") is not None

    def get_end_time(self) -> float:
        """
        :return: Last vehicle arrival time (-1 if no vehicles are found)
        """
        if not self.has_vehicles():
            print(f"No vehicles in routes file!")
            return -1
        return float(self.root.findall("vehicle")[-1].attrib["depart"])

    def get_vehicles(self, start_time: int, end_time: int) -> Dict[str, Tuple[str, str]]:
        """
        Extracts vehicles from '.ruo.xml' file, filtered by start/end time as <start_time, end_time)

        :param start_time: earliest vehicle arrival
        :param end_time: latest vehicle arrival (without)
        :return: Vehicle dictionary mapping vehicle id to initial and ending junctions of its route
        """
        print("Parsing vehicles")
        vehicles: Dict[str, Tuple[str, str]] = {}
        if self.tree is None:
            print("XML Tree is not set!")
            return vehicles
        elif not self.has_vehicles():
            print(f"No vehicles in routes file!")
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
            depart: float = float(vehicle.attrib["depart"])
            if start_time <= depart < end_time:
                vehicles[vehicle.attrib["id"]] = routes[vehicle.attrib["route"]]
            elif depart >= end_time:
                self.previous_search = (end_time, index)
                break
        return vehicles


# For testing purposes
if __name__ == "__main__":
    temp: RoutesGenerator = RoutesGenerator()

