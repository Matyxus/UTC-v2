import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element
from Project.Utils.constants import PATH, file_exists
from xml.dom import minidom
from typing import List, Dict, Tuple
from Project.Traci.simulation import Vehicle, Flow
from Project.Simplify.Components import Route, Graph


class RoutesGenerator:
    """ Class that generates '.route.xml' files for SUMO """
    def __init__(self):
        self.tree: ElementTree = ET.parse(PATH.SUMO_ROUTES_TEMPLATE)
        self.routes: List[Route] = []
        self.vehicles: List[Vehicle] = []
        self.flow: Flow = Flow(self.vehicles)
        # Shortest Paths
        self.graph: Graph = None
        self.road_paths: Dict[str, Dict[str, str]] = {
            # Recording found shortest paths
            # from_junction_id : {to_junction_id : route_id, ...}, ...
        }

    def load_network(self, network_name: str) -> None:
        """

        :param network_name:
        :return:
        """
        self.graph: Graph = Graph()
        self.graph.loader.load_map(network_name)
        self.graph.simplify.simplify()

    def add_cars(self, args: List[str]) -> None:
        """
        Adds route (if its new), Vehicle to scenario, expects correct arguments

        :param args: [amount, from_junction_id, to_junction_id, depart_time]
        :return: None
        """
        # Find route
        route_id: str = self.get_path(args[1], args[2])
        if not route_id:
            return
        # Add vehicles
        for i in range(int(args[0])):
            temp: Vehicle = Vehicle()
            temp.set_route(route_id)
            temp.set_depart(float(args[3]))
            self.vehicles.append(temp)

    # --------------- Load & Save ---------------

    def load_routes(self, file_path: str) -> None:
        """
        :param file_path: of .rou.xml file
        :return: None
        """
        if not file_exists(file_path):
            return
        self.tree = ET.parse(file_path)

    def save(self, file_path: str) -> None:
        """
        :param file_path: where file should be saved
        :return: None
        """
        root: Element = self.tree.getroot()
        for route in self.routes:
            root.append(route.to_xml())
        self.vehicles.sort()
        for vehicle in self.vehicles:
            root.append(vehicle.to_xml())
        with open(file_path, 'w') as output:
            output.write(self.prettify(root))

    # ----------------------- Utils  -----------------------

    def prettify(self, root: Element) -> str:
        """
        :param root: of xml tree
        :return: pretty print version of xml file
        """
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def get_path(self, from_junction_id: str, to_junction_id: str) -> str:
        """
        :param from_junction_id: starting junction
        :param to_junction_id: destination junction
        :return: id of route, None if it does not exist
        """
        assert (self.graph is not None)
        if from_junction_id in self.road_paths and to_junction_id in self.road_paths[from_junction_id]:
            return self.road_paths[from_junction_id][to_junction_id]  # Get route from already found routes
        path: Route = self.graph.shortest_path.a_star(from_junction_id, to_junction_id)[1]
        if path is None:
            print(f"Path between {from_junction_id} and {to_junction_id} does not exist!")
            return ""
        # Record path
        if from_junction_id not in self.road_paths:
            self.road_paths[from_junction_id] = {}
        self.road_paths[from_junction_id][to_junction_id] = path.attributes["id"]
        self.routes.append(path)
        return path.attributes["id"]

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

# temp2: Element = Element("vehicle", {"id": "6", "edges": ""})
#    root.append(temp)


if __name__ == "__main__":
    pass




