from typing import Dict, Set, List
from Project.Simplify.Components import Route, Edge, Junction
from copy import deepcopy


class Skeleton:
    """ Skeleton of Graph, holds junctions, edges, routes ... """

    def __init__(self):
        print("Created 'Skeleton' class")
        self.junctions: Dict[str, Junction] = {}
        self.edges: Dict[str, Edge] = {}
        self.routes: Dict[int, Route] = {}
        self.starting_junctions: Set[str] = set()
        self.ending_junctions: Set[str] = set()
        self.roundabouts: List[List[str]] = []
        self.map_name: str = ""
        self.index: int = 0  # For generating new id's of routes, has to start at 0 !

    def get_skeleton(self):
        """
        :return: Skeleton class (itself)
        """
        return self

    def load(self, other) -> bool:
        """
        Loads attributes from other struct

        :param other: Skeleton Class (loaded from the same file)
        :return: True on success, false otherwise
        """
        if not isinstance(other, Skeleton) or (self.map_name != other.map_name):
            return False
        self.junctions = deepcopy(other.junctions)
        self.edges = deepcopy(other.edges)
        self.routes = deepcopy(other.routes)
        self.starting_junctions = deepcopy(other.starting_junctions)
        self.ending_junctions = deepcopy(other.ending_junctions)
        self.roundabouts = deepcopy(other.roundabouts)
        self.index = len(self.routes)
        return True

    # -------------------------- Sub-graph --------------------------
    def create_sub_graph(self, routes: List[Route]):
        """
        Creates sub-graph from this graph.

        :param routes: List of routes from which sub-graph will be created
        :return: Skeleton (sub-graph), None if routes are empty
        """
        sub_graph: Skeleton = Skeleton()
        sub_graph.map_name = self.map_name
        if len(routes) == 0 or not sub_graph.load(self):
            return None
        # -------------------------- Cut graph --------------------------
        junctions: Set[str] = set()  # Junctions to be kept in graph
        edges: Set[Edge] = set()  # Edges to be kept in graph
        # Extract junctions and edges from routes
        for route in routes:
            edges |= set(route.edge_list)
            junctions |= set(route.get_junctions())
        # Delete others edges, junctions
        for edge in (set(self.edges.values()) ^ edges):
            sub_graph.remove_edge(edge.attributes["id"])
        for junction_id in (self.junctions.keys() ^ junctions):
            sub_graph.remove_junction(junction_id)
        return sub_graph

    # ----------------------------------- Utils -----------------------------------

    def merge(self, other, plot: bool) -> None:
        """
        Merges this graph with another graph.

        :param other: another graph current graph is merging with
        :param plot: bool, if plot should be displayed
        :return: None
        """
        assert (isinstance(other, Skeleton))
        if self.map_name != other.map_name:
            print(f"Only graphs from the same network may be merged {self.map_name} != {other.map_name}")
            return
        print("Merging with another graph")
        # ------------------------ Junctions ------------------------
        self.starting_junctions |= other.starting_junctions
        self.ending_junctions |= other.ending_junctions
        for junction_id, junction in other.junctions.items():
            if junction_id in self.junctions:
                self.junctions[junction_id] |= junction
            else:
                self.junctions[junction_id] = deepcopy(junction)
        # ------------------------ Routes ------------------------
        for route in other.routes.values():
            if route.id not in self.routes:
                self.routes[route.id] = deepcopy(route)
        # ------------------------ Edges ------------------------
        for edge_id, edge in other.edges.items():
            if edge_id not in self.edges:
                self.edges[edge_id] = deepcopy(edge)

    # ------------------------------ Utils ------------------------------

    def validate_graph(self) -> None:
        """
        Checks all junctions, edges, routes.
        Removes unused junctions, routes, edges,
        should be called on final sub-graph

        :return: None
        """
        print("Validating graph")
        routes_to_remove: List[int] = []
        # Check routes, find routes that have edge which are no longer in graph
        for route in self.routes.values():
            for edge in route.edge_list:
                if edge not in self.edges.values():
                    routes_to_remove.append(route.id)
                    break
        # Remove routes such routes
        for route_id in routes_to_remove:
            self.routes.pop(route_id)
        # Among junctions check routes, if route is not used, remove it
        for junction in self.junctions.values():
            in_routes: List[Route] = junction.get_in_routes()
            for in_route in in_routes:
                if in_route.id not in self.routes:
                    junction.remove_in_route(in_route)
            out_routes: List[Route] = junction.get_out_routes()
            for out_route in out_routes:
                if out_route.id not in self.routes:
                    junction.remove_out_route(out_route)
        print("Finished validating graph")

    def remove_junction(self, junction_id: str) -> None:
        """
        :param junction_id: to be removed
        :return: None
        """
        if junction_id not in self.junctions:
            return
        self.junctions.pop(junction_id, None)
        if junction_id in self.starting_junctions:
            self.starting_junctions.remove(junction_id)
        if junction_id in self.ending_junctions:
            self.ending_junctions.remove(junction_id)

    def add_route(self, route: Route) -> None:
        """
        :param route: to be added to dictionary of routes
        :return: None
        """
        assert (route.id not in self.routes)
        self.routes[route.id] = route

    def get_new_route_id(self) -> int:
        """
        :return: new id of route
        """
        self.index += 1
        return self.index

    def remove_edge(self, edge_id: str) -> None:
        """
        :param edge_id: to be removed
        :return: None
        """
        if edge_id in self.edges:
            self.edges.pop(edge_id, None)

    def construct_route(self, junction_list: List[str]) -> Route:
        """
        :param junction_list: of junctions ids on path
        :return: None in case junction is empty or path does not exist, temporary Route Class otherwise
        """
        if len(junction_list) == 0:
            return None
        ret_val: Route = Route(-1,  [])
        in_route: Route = None
        for i in range(0, len(junction_list)-1):
            # Also sets self.route as current one
            follow_route: Route = self.find_route(junction_list[i], junction_list[i+1], from_route=in_route)
            if follow_route is None:
                return ret_val
            in_route = follow_route
            ret_val |= follow_route
        return ret_val

    def find_route(self, from_junction_id: str, to_junction_id: str, from_route: Route = None) -> Route:
        """
        :param from_route: optional parameter, incoming route to from_junction_id
        :param from_junction_id: starting junction
        :param to_junction_id: target junction (must be neighbour)
        :return: Route between junctions, None if it doesn't exist
        """
        for route in self.junctions[from_junction_id].travel(from_route):
            if route.get_destination() == to_junction_id:
                return route
        return None

    def get_new_route(self) -> Route:
        """
        :return: new route, with new route_id, empty edge_list
        """
        return Route(self.get_new_route_id(), [])
