import xml.etree.ElementTree as ET
from typing import Dict, List
from Project.Simplify.components import Junction, Edge, Route
from Project.Utils.constants import (
    PATH, file_exists, get_file_name, JUNCTION_START_COLOR, JUNCTION_START_END_COLOR, JUNCTION_END_COLOR
)
from Project.Simplify.graph_modules.graph_module import GraphModule
from Project.Simplify.components import Skeleton


class Loader(GraphModule):
    """ Loads graph from SUMO's '.net.xml' file """

    def __init__(self, skeleton: Skeleton = None):
        super().__init__(skeleton)
        print("Created 'Loader' class")
        # Xml root of .net.xml file
        self.root: ET.Element = None
        # Mapping edges to their respective routes
        self.edge_to_route: Dict[str, Route] = {}

    def load_map(self, file_name: str) -> bool:
        """

        :param file_name: of map to be loaded
        :return: True on success, false otherwise
        """
        file_name = get_file_name(file_name)
        print(f"Loading road network form: {PATH.NETWORK_SUMO_MAPS.format(file_name)}")
        if not (file_exists(PATH.NETWORK_SUMO_MAPS.format(file_name))):
            return False
        self.root = ET.parse(PATH.NETWORK_SUMO_MAPS.format(file_name)).getroot()
        assert (self.skeleton is not None)
        self.load_junctions()
        self.load_edges()
        self.skeleton.roundabouts = self.load_roundabouts()
        self.edge_to_route.clear()
        self.skeleton.map_name = file_name
        print("Finished loading road network")
        return True

    def load_junctions(self) -> None:
        """
        Loads junctions from .net.xml

        :return: None
        """
        print("Loading & creating junctions")
        # Create Junctions classes
        for junction in self.root.findall("junction"):
            # Filter internal junctions
            if ("type" in junction.attrib) and (junction.attrib["type"] != "internal"):
                self.skeleton.junctions[junction.attrib["id"]] = Junction(junction.attrib)
        print("Finished loading & creating junctions")

    def load_edges(self) -> None:
        """
        Loads edges and connections from .net.xml file,
        sets routes classes, identifies starting/ending junctions

        :return: None
        """
        print("Loading & creating edges, connections")
        connections: Dict[str, set] = {}
        # ----------------- Connections -----------------
        for connection in self.root.findall("connection"):
            # Filter internal connections
            if connection.attrib["from"][0] != ":":
                if connection.attrib["to"] not in connections:
                    connections[connection.attrib["to"]] = set()
                connections[connection.attrib["to"]].add(connection.attrib["from"])
        # ------------------- Edges -----------------
        for edge in self.root.findall("edge"):
            # Filter internal edges
            if not ("function" in edge.attrib):
                edge_id: str = edge.attrib["id"]
                self.skeleton.edges[edge_id] = Edge(edge.attrib)
                # Give each edge its lanes
                for lane in edge.findall("lane"):
                    self.skeleton.edges[edge_id].add_lane(lane.attrib)
                # Create route from edge
                route: Route = self.get_route(self.skeleton.edges[edge_id])
                # Set destination junction in_route as this one
                self.skeleton.junctions[edge.attrib["to"]].neighbours[route] = []
        # ------------------- Assign routes, to junctions -------------------
        for route in self.skeleton.routes.values():
            # Routes only have 1 edge each
            edge_id: str = route.first_edge().attributes["id"]
            from_junction: Junction = self.skeleton.junctions[route.get_start()]
            if edge_id in connections:
                for in_edge_id in connections[edge_id]:
                    assert (in_edge_id in self.edge_to_route)
                    assert (self.edge_to_route[in_edge_id] in from_junction.get_in_routes())
                    from_junction.add_connection(self.edge_to_route[in_edge_id], route)
            else:  # No connection to this edge, from_junction is starting
                from_junction.add_connection(route, route)
                from_junction.set_color(JUNCTION_START_COLOR)
                self.skeleton.starting_junctions.add(from_junction.attributes["id"])
                # print(f"Junction: {from_junction.attributes['id']} is starting !")
        # ------------------- Check -------------------
        for edge in self.skeleton.edges.values():
            # print(f"Checking edge: {edge.attributes['id']}")
            route: Route = self.edge_to_route[edge.attributes["id"]]
            from_junction: Junction = self.skeleton.junctions[edge.attributes["from"]]
            to_junction: Junction = self.skeleton.junctions[edge.attributes["to"]]
            # print("From junction: ", from_junction.attributes["id"], from_junction.neighbours)
            # print("To junction: ", to_junction.attributes["id"], to_junction.neighbours)
            assert (route in to_junction.get_in_routes())
            assert (route in from_junction.get_out_routes())
        # ------------------- Starting & ending junctions -----------------
        # Find nodes, which have only 1 in_route and 1 out_route,
        # if in_route_start is equal to out_route_destination, remove it
        for junction_id, junction in self.skeleton.junctions.items():
            in_routes: List[Route] = junction.get_in_routes()
            out_routes: List[Route] = junction.get_out_routes()
            if (len(in_routes) == 1) and (len(out_routes) == 1):
                in_route: Route = in_routes[0]
                out_route: Route = out_routes[0]
                # Check if incoming route is from the same Junction, as the destination of out_route
                if out_route.get_destination() == in_route.get_start():
                    self.skeleton.starting_junctions.add(junction_id)
                    self.skeleton.ending_junctions.add(junction_id)
                    junction.set_color(JUNCTION_START_END_COLOR)
                    # print(f"Junction: {junction_id} is starting and ending!")
                    # Remove the connection between this two routes
                    junction.neighbours[in_route] = []
                    # Since route is starting, add corresponding mapping to out_route
                    junction.add_connection(out_route, out_route)
            elif len(out_routes) == 0:  # Ending nodes, no connection out
                self.skeleton.ending_junctions.add(junction_id)
                self.skeleton.junctions[junction_id].set_color(JUNCTION_END_COLOR)
                # print(f"Junction: {junction_id} is ending!")
                # print(junction_id, self.skeleton.junctions[junction_id].neighbours)
        print("Finished loading & creating edges, connections")

    def load_roundabouts(self) -> List[List[str]]:
        """
        :return: List of roundabouts (each roundabout is list of junctions ids forming it)
        """
        roundabouts: list = []
        for xml_node in self.root.findall("roundabout"):
            roundabout: list = xml_node.attrib["nodes"].split()
            roundabouts.append(roundabout)
        return roundabouts

    # ------------------------- Utils -------------------------

    def get_route(self, edge: Edge) -> Route:
        """
        :param edge:
        :return: New route created from edge_id, or exiting one
        """
        if edge.attributes["id"] in self.edge_to_route:
            return self.edge_to_route[edge.attributes["id"]]
        route_id: int = self.skeleton.get_new_route_id()
        assert (route_id not in self.skeleton.routes)
        self.skeleton.routes[route_id] = Route(route_id, [edge])
        self.edge_to_route[edge.attributes["id"]] = self.skeleton.routes[route_id]
        return self.skeleton.routes[route_id]
