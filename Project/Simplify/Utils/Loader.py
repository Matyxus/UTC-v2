import xml.etree.ElementTree as ET
from typing import Dict, List
from Project.Simplify.Components import Junction, Edge, Route, Skeleton
from Project.constants import CWD, file_exists, JUNCTION_START_COLOR, JUNCTION_START_END_COLOR, JUNCTION_END_COLOR
from Project.Simplify.Utils import RouteManager


class Loader:
    """ Loads graph from SUMO's '.net.xml' file """

    def __init__(self, file_name: str, skeleton: Skeleton, route_manager: RouteManager):
        print(f"Creating Loader Class, loading file form: {CWD}/Maps/sumo/{file_name + '.net.xml'}")
        assert(file_exists(f"{CWD}/Maps/sumo/{file_name+'.net.xml'}"))
        # Xml root of .net.xml file
        self.root: ET.Element = ET.parse(f"{CWD}/Maps/sumo/{file_name+'.net.xml'}").getroot()
        self.skeleton: Skeleton = skeleton
        self.route_manager: RouteManager = route_manager
        # Mapping edges to their respective routes
        self.edge_to_route: Dict[str, int] = {}

    def load_junctions(self) -> None:
        """
        Loads junctions from .net.xml

        :return None:
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
                route_id: int = self.get_route_id(edge_id)
                # Set destination junction in_route as this one
                self.skeleton.junctions[edge.attrib["to"]].neighbours[route_id] = []
        # ------------------- Assign routes, to junctions -------------------
        for route in self.skeleton.routes.values():
            # Routes only have 1 edge each
            edge_id: str = route.edge_list[0]
            from_junction: Junction = self.skeleton.junctions[self.route_manager.get_start(route.id)]
            if edge_id in connections:
                for in_edge_id in connections[edge_id]:
                    assert (in_edge_id in self.edge_to_route)
                    assert (self.edge_to_route[in_edge_id] in from_junction.get_in_routes())
                    from_junction.add_connection(self.edge_to_route[in_edge_id], route.id)
            else:  # No connection to this edge, from_junction is starting
                from_junction.add_connection(route.id, route.id)
                from_junction.set_color(JUNCTION_START_COLOR)
                self.skeleton.starting_junctions.add(from_junction.attributes["id"])
                # print(f"Junction: {from_junction.attributes['id']} is starting !")
        # ------------------- Check -------------------
        for edge in self.skeleton.edges.values():
            # print(f"Checking edge: {edge.attributes['id']}")
            route: Route = self.skeleton.routes[self.edge_to_route[edge.attributes["id"]]]
            from_junction: Junction = self.skeleton.junctions[edge.attributes["from"]]
            to_junction: Junction = self.skeleton.junctions[edge.attributes["to"]]
            # print("From junction: ", from_junction.attributes["id"], from_junction.neighbours)
            # print("To junction: ", to_junction.attributes["id"], to_junction.neighbours)
            assert (route.id in to_junction.get_in_routes())
            assert (route.id in from_junction.get_out_routes())
        # ------------------- Starting & ending junctions -----------------
        # Find nodes, which have only 1 in_route and 1 out_route,
        # if in_route_start is equal to out_route_destination, remove it
        for junction_id, junction in self.skeleton.junctions.items():
            in_routes: List[int] = junction.get_in_routes()
            out_routes: List[int] = junction.get_out_routes()
            if (len(in_routes) == 1) and (len(out_routes) == 1):
                in_route_id: int = in_routes[0]
                out_route_id: int = out_routes[0]
                # Check if incoming route is from the same Junction, as the destination of out_route
                if self.route_manager.get_destination(out_route_id) == self.route_manager.get_start(in_route_id):
                    self.skeleton.starting_junctions.add(junction_id)
                    self.skeleton.ending_junctions.add(junction_id)
                    junction: Junction = self.skeleton.junctions[junction_id]
                    junction.set_color(JUNCTION_START_END_COLOR)
                    # print(f"Junction: {junction_id} is starting and ending!")
                    # Remove the connection between this two routes
                    junction.neighbours[in_route_id] = []
                    # Since route is starting, add corresponding mapping to out_route
                    junction.add_connection(out_route_id, out_route_id)
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

    def get_route_id(self, edge_id: str) -> int:
        """
        :param edge_id:
        :return: New route created from edge_id, or exiting one
        """
        if edge_id in self.edge_to_route:
            return self.edge_to_route[edge_id]
        route_id: int = self.route_manager.get_new_route_id()
        assert (route_id not in self.skeleton.routes)
        self.skeleton.routes[route_id] = Route(route_id, [edge_id])
        self.edge_to_route[edge_id] = route_id
        return route_id
