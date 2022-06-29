from Project.Traci.scenarios.generators.generator import Generator
from Project.Utils.constants import PATH
from typing import Dict, Tuple
from Project.Traci.simulation import VehicleGenerator
from Project.Simplify.components import Graph


class RoutesGenerator(Generator):
    """ Class that generates '.route.xml' files for SUMO """

    def __init__(self, graph: Graph = None, routes_path: str = PATH.SUMO_ROUTES_TEMPLATE):
        """
        :param graph: graph of road network (default None)
        :param routes_path: path of '.route.xml' file
        """
        super().__init__(routes_path)
        assert (self.tree is not None)
        assert (self.root is not None)
        # Binary search tree for sorting vehicles
        self.vehicle_generator: VehicleGenerator = VehicleGenerator(graph)

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
        self.vehicle_generator.vehicles_bst.sorted_append(self.vehicle_generator.vehicles_bst.root, self.root)
        super().save(file_path)

    # ------------------------------------------ Utils  ------------------------------------------

    def get_vehicles(self, start_time: int, end_time: int) -> Dict[str, Tuple[str, str]]:
        """
        Extracts vehicles from .ruo.xml file, filtered by start/end time.

        :param start_time: earliest vehicle arrival
        :param end_time: latest vehicle arrival
        :return: Vehicle dictionary mapping vehicle id to initial and ending junctions of its route
        """
        print("Parsing vehicles")
        vehicles: Dict[str, Tuple[str, str]] = {}
        if self.tree is None:
            print("XML Tree is not set!")
            return vehicles
        routes: Dict[str, Tuple[str, str]] = {}
        root = self.tree.getroot()
        # Routes
        for route in root.findall("route"):
            routes[route.attrib["id"]] = (route.attrib["fromJunction"], route.attrib["toJunction"])
        # Vehicles
        for vehicle in root.findall("vehicle"):
            if start_time <= float(vehicle.attrib["depart"]) <= end_time:
                vehicles[vehicle.attrib["id"]] = routes[vehicle.attrib["route"]]
        return vehicles


# For testing purposes
if __name__ == "__main__":
    temp: RoutesGenerator = RoutesGenerator()
