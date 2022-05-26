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
        # Binary search tree for sorting vehicles
        self.bst: RoutesGenerator.BST = RoutesGenerator.BST()
        self.flow: Flow = Flow()
        # Shortest Paths
        self.graph: Graph = None
        self.road_paths: Dict[str, Dict[str, str]] = {
            # Recording found shortest paths
            # from_junction_id : {to_junction_id : route_id, ...}, ...
        }

    def load_network(self, network_name: str) -> None:
        """

        :param network_name: name of road network from SUMO
        :return: None
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
        assert (len(args) == 4)
        # Find route
        route_id: str = self.get_path(args[1], args[2])
        if not route_id:
            return
        # Add vehicles
        for i in range(int(args[0])):
            temp: Vehicle = Vehicle()
            temp.set_route(route_id)
            temp.set_depart(int(args[3]))
            self.bst.binary_insert(temp)

    def add_flow(self, flow_type: str, from_junction_id: str, to_junction_id: str, flow_args: list) -> None:
        """
        :param flow_type: type of flow (same name as function defined in Flow class!)
        :param from_junction_id: starting junction
        :param to_junction_id: ending junction
        :param flow_args: arguments of selected flow
        :return: None
        """
        assert (len(flow_args) > 0)
        flow_type += "_flow"
        flow_method = None
        try:
            flow_method = getattr(self.flow, flow_type)
        except AttributeError as e:
            print(f"Flow called: {flow_type} does not exist!")
            return
        if flow_method is None:
            print(f"Flow called: {flow_type} does not exist!")
            return
        # Insert route as flows_args[0]
        # Find route
        route_id: str = self.get_path(from_junction_id, to_junction_id)
        if not route_id:
            return
        flow_args.insert(0, route_id)
        for vehicle in flow_method(*flow_args):
            # append flow vehicles to list of vehicles
            self.bst.binary_insert(vehicle)

    # ------------------------------------------Load & Save ------------------------------------------

    def load_routes(self, file_path: str) -> None:
        """
        :param file_path: of .rou.xml file
        :return: None
        """
        if not file_exists(file_path):
            return
        elif ".ruo.xml" not in file_path:
            print("File must be of type '.ruo.xml'!")
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
        self.bst.sorted_append(self.bst.root, root)
        with open(file_path, 'w') as output:
            output.write(self.prettify(root))

    # ------------------------------------------ Utils  ------------------------------------------

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

    # ------------------------------ Binary Search Tree ------------------------------

    class BST:
        """ Binary search tree (designed to sort vehicles by time of departure) """

        def __init__(self):
            # Root of BST tree
            self.root: RoutesGenerator.BST.Node = None

        class Node:
            """ Node of binary search tree """
            def __init__(self, vehicle: Vehicle):
                self.l_child = None
                self.r_child = None
                self.vehicle: Vehicle = vehicle

        def binary_insert(self, vehicle: Vehicle) -> None:
            """
            Iteratively inserts vehicle as new node into BST, compares
            others vehicles with their departing time

            :param vehicle: to be inserted
            :return: None
            """
            new_node: RoutesGenerator.BST.Node = RoutesGenerator.BST.Node(vehicle)
            temp_node: RoutesGenerator.BST.Node = self.root
            if temp_node is None:
                self.root = new_node
                return
            temp_pointer: RoutesGenerator.BST.Node = None
            # Find parent node
            while temp_node is not None:
                temp_pointer = temp_node
                if vehicle.get_depart() < temp_node.vehicle.get_depart():
                    temp_node = temp_node.l_child
                else:
                    temp_node = temp_node.r_child
            # Assign new node to tree
            if temp_pointer is None:
                temp_pointer = new_node
            elif vehicle.get_depart() < temp_pointer.vehicle.get_depart():
                temp_pointer.l_child = new_node
            else:
                temp_pointer.r_child = new_node

        def in_order(self, node: Node) -> None:
            """
            Prints vehicles in BST (sorted by lowest departure time to highest)

            :param node: on which traversal should start
            :return: None
            """
            if node is None:
                return
            self.in_order(node.l_child)
            print(node.vehicle)
            self.in_order(node.r_child)

        def sorted_append(self, node: Node, element: Element) -> None:
            """
            Appends vehicles sorted by their departure time to xml element

            :param node: on which appending should start
            :param element: xml element to which vehicles should be appended to
            :return: None
            """
            if node is None:
                return
            self.sorted_append(node.l_child, element)
            element.append(node.vehicle.to_xml())
            self.sorted_append(node.r_child, element)


# For testing purposes
if __name__ == "__main__":
    print([int, str, float])

