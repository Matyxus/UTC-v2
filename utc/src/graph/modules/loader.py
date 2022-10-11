from utc.src.graph.components import Junction, Edge, Route
from utc.src.graph.utils import Colors
from utc.src.graph.modules.graph_module import GraphModule
from utc.src.graph.components import Skeleton
from utc.src.graph.components.skeleton_types import MergedType, NetworkType, SubgraphType
from utc.src.file_system import SumoNetworkFile, FilePaths
from typing import Dict, List, Optional


class Loader(GraphModule):
    """ Loads graph from SUMO's '.net.xml' file """

    def __init__(self, skeleton: Skeleton = None):
        super().__init__(skeleton)
        self.network_file: Optional[SumoNetworkFile] = None
        # Mapping edges to their respective routes
        self.edge_to_route: Dict[str, Route] = {}

    def load_map(self, network_path: str) -> bool:
        """
        :param network_path: path to network file (default is
        /data/maps/osm)
        :return: true on success, false otherwise
        """
        if self.skeleton is None:
            print("Skeleton must not be of type: 'None' before loading map!")
            return False
        elif not SumoNetworkFile.file_exists(network_path, message=False):
            network_path = FilePaths.MAP_SUMO.format(SumoNetworkFile.get_file_name(network_path))
        self.network_file = SumoNetworkFile(network_path)
        # File does not exist
        if not self.network_file.file_exists(self.network_file):
            return False
        self.skeleton.type = NetworkType(SumoNetworkFile.get_file_name(network_path), network_path)
        self.load_junctions()
        self.load_edges()
        self.load_subgraphs()
        self.skeleton.roundabouts = self.load_roundabouts()
        self.edge_to_route.clear()
        self.skeleton.map_name = SumoNetworkFile.get_file_name(network_path)
        print("Finished loading road network")
        # Clear
        self.network_file = None
        self.edge_to_route.clear()
        return True

    def load_junctions(self) -> None:
        """
        Loads junctions from '.net.xml' file

        :return: None
        """
        print("Loading & creating junctions")
        for xml_junction in self.network_file.get_junctions():
            self.skeleton.junctions[xml_junction.attrib["id"]] = Junction(xml_junction.attrib)
        print("Finished loading & creating junctions")

    def load_subgraphs(self) -> None:
        """
        Loads subgraphs from '.net.xml' file

        :return: None
        """
        print("Loading & creating junctions")
        sub_graphs = self.network_file.get_subgraphs()
        if sub_graphs is None:
            return
        # Change type of skeleton
        self.skeleton.type = MergedType(
            self.skeleton.get_name(),
            [SubgraphType(*sub_graph.attrib.values()) for sub_graph in sub_graphs]
        )
        print("Finished loading & creating junctions")

    def load_edges(self) -> None:
        """
        Loads edges and connections from .net.xml file,
        sets routes classes, identifies starting/ending junctions

        :return: None
        """
        print("Loading & creating edges, connections")
        # ------------------- Edges -----------------
        for edge in self.network_file.get_edges():
            edge_id: str = edge.attrib["id"]
            self.skeleton.edges[edge_id] = Edge(edge.attrib)
            # Give each edge its lanes
            for lane in edge.findall("lane"):
                self.skeleton.edges[edge_id].add_lane(lane.attrib)
            # Create route from edge
            route: Route = self.get_route(self.skeleton.edges[edge_id])
            # Set destination junction in_route as this one
            self.skeleton.junctions[edge.attrib["to"]].neighbours[route] = []
        # ----------------- Connections -----------------
        connections: Dict[str, set] = {
            # to_edge_id: {from_edge_id, ..}, ..
        }
        for connection in self.network_file.get_connections():
            if connection.attrib["to"] not in connections:
                connections[connection.attrib["to"]] = set()
            if "tl" in connection.attrib:
                junction_id: str = self.skeleton.edges[connection.attrib['from']].attributes['to']
                self.skeleton.junctions[junction_id].set_traffic_lights(True)
            connections[connection.attrib["to"]].add(connection.attrib["from"])
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
                from_junction.set_color(Colors.JUNCTION_START_COLOR)
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
            if len(in_routes) == len(out_routes) == 1:
                in_route: Route = in_routes[0]
                out_route: Route = out_routes[0]
                # Check if incoming route is from the same Junction, as the destination of out_route
                if out_route.get_destination() == in_route.get_start():
                    self.skeleton.starting_junctions.add(junction_id)
                    self.skeleton.ending_junctions.add(junction_id)
                    junction.set_color(Colors.JUNCTION_START_END_COLOR)
                    # print(f"Junction: {junction_id} is starting and ending!")
                    # Remove the connection between this two routes
                    junction.neighbours[in_route] = []
                    # Since route is starting, add corresponding mapping to out_route
                    junction.add_connection(out_route, out_route)
            elif len(out_routes) == 0:  # Ending nodes, no connection out
                self.skeleton.ending_junctions.add(junction_id)
                self.skeleton.junctions[junction_id].set_color(Colors.JUNCTION_END_COLOR)
                # print(f"Junction: {junction_id} is ending!")
                # print(junction_id, self.skeleton.junctions[junction_id].neighbours)
        print("Finished loading & creating edges, connections")

    def load_roundabouts(self) -> List[List[str]]:
        """
        :return: List of roundabouts (each roundabout is list of junctions ids forming it)
        """
        roundabouts: list = []
        for xml_roundabout in self.network_file.get_roundabouts():
            roundabouts.append(xml_roundabout.attrib["nodes"].split())
        return roundabouts

    # ------------------------- Utils -------------------------

    def get_route(self, edge: Edge) -> Route:
        """
        :param edge:
        :return: New route created from edge_id, or exiting one
        """
        if edge.attributes["id"] in self.edge_to_route:
            return self.edge_to_route[edge.attributes["id"]]
        ret_val: Route = Route([edge], int(edge.attributes["id"]))
        self.skeleton.add_route(ret_val)
        self.edge_to_route[edge.attributes["id"]] = ret_val
        return ret_val


if __name__ == "__main__":
    temp: Loader = Loader(Skeleton())
    temp.load_map("Sydney")


