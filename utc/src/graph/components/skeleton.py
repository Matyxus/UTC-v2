from typing import Dict, Set, List, Optional, Union
from utc.src.graph.components import Route, Edge, Junction
from utc.src.graph.components.skeleton_types import SkeletonType
from copy import deepcopy


class Skeleton:
    """ Skeleton of Graph, holds its type, junctions, edges, routes ... """

    def __init__(self, name: str = "", graph_type: SkeletonType = None):
        """
        :param name: of skeleton (default none)
        :param graph_type: of skeleton (default none)
        """
        # Type of skeleton
        self.type: SkeletonType = graph_type if graph_type is not None else SkeletonType(name)
        # Components of skeleton
        self.junctions: Dict[str, Junction] = {}
        self.edges: Dict[str, Edge] = {}
        self.routes: Dict[str, Route] = {}
        self.starting_junctions: Set[str] = set()
        self.ending_junctions: Set[str] = set()
        self.roundabouts: List[List[str]] = []
        # Original map from which skeleton was made (can be subgraph)
        self.map_name: str = ""

    def validate_graph(self) -> None:
        """
        Checks all junctions, edges, routes.
        Removes unused junctions, routes, edges,
        should be called on final sub-graph

        :return: None
        """
        print("Validating graph")
        routes_to_remove: List[str] = []
        # Check routes, find routes that have edge which are no longer in graph
        for route in self.routes.values():
            for edge in route.edge_list:
                if edge.get_id() not in self.edges.keys():
                    routes_to_remove.append(route.get_id())
                    break
        # Remove routes such routes
        for route_id in routes_to_remove:
            self.routes.pop(route_id)
        # Among junctions check routes, if route is not used, remove it
        for junction in self.junctions.values():
            in_routes: List[Route] = junction.get_in_routes()
            for in_route in in_routes:
                if in_route.get_id() not in self.routes:
                    junction.remove_in_route(in_route)
            out_routes: List[Route] = junction.get_out_routes()
            for out_route in out_routes:
                if out_route.get_id() not in self.routes:
                    junction.remove_out_route(out_route)
        print("Finished validating graph")

    # -------------------------------------------------- Adders --------------------------------------------------

    def add_junctions(self, junction: Junction) -> None:
        """
        :param junction: to be added
        :return: None
        """
        if junction.get_id() in self.junctions:
            print(f"Junction with id: '{junction.get_id()}' is already present in Skeleton!")
            return
        self.junctions[junction.get_id()] = junction

    def add_edge(self, edge: Edge) -> None:
        """
        :param edge: to be added
        :return: None
        """
        if edge.get_id() in self.junctions:
            print(f"Edge with id: '{edge.get_id()}' is already present in Skeleton!")
            return
        self.edges[edge.get_id()] = edge

    def add_route(self, route: Route) -> None:
        """
        :param route: to be added to dictionary of routes
        :return: None
        """
        if route.get_id() in self.junctions:
            print(f"Route with id: '{route.get_id()}' is already present in Skeleton!")
            return
        self.routes[route.get_id()] = route

    # -------------------------------------------------- Removers --------------------------------------------------

    def remove_junction(self, junction: Union[str, Junction]) -> Optional[Junction]:
        """
        :param junction: to be removed
        :return: removed Junction if it exists, None otherwise
        """
        junction_id: str = junction.get_id() if isinstance(junction, Junction) else junction
        if junction_id not in self.junctions:
            # print(f"Cannot remove junction with id: '{junction_id}', it does not exist!")
            return None
        if junction_id in self.starting_junctions:
            self.starting_junctions.remove(junction_id)
        if junction_id in self.ending_junctions:
            self.ending_junctions.remove(junction_id)
        return self.junctions.pop(junction_id, None)

    def remove_edge(self, edge: Union[str, Edge]) -> Optional[Edge]:
        """
        :param edge: to be removed (either class or id)
        :return: removed Edge if it exists, None otherwise
        """
        edge_id: str = edge.get_id() if isinstance(edge, Edge) else edge
        # if edge_id not in self.edges:
        # print(f"Cannot remove edge with id: '{edge_id}', it does not exist!")
        return self.edges.pop(edge_id, None)

    def remove_route(self, route: Union[str, Route]) -> Optional[Route]:
        """
        :param route: to be removed
        :return: removed Route if it exists, None otherwise
        """
        route_id: str = route.get_id() if isinstance(route, Route) else route
        # if route_id not in self.routes:
        # print(f"Cannot remove route with id: '{route_id}', it does not exist!")
        return self.routes.pop(route_id, None)

    # -------------------------------------------------- Utils --------------------------------------------------

    def construct_route(self, junction_list: List[str]) -> Optional[Route]:
        """
        :param junction_list: of junctions ids on path
        :return: None in case junction is empty or path does not exist, temporary Route Class otherwise
        """
        if len(junction_list) == 0:
            return None
        ret_val: Route = Route([])
        in_route: Optional[Route] = None
        for i in range(0, len(junction_list)-1):
            # Also sets self.route as current one
            follow_route: Route = self.find_route(junction_list[i], junction_list[i+1], from_route=in_route)
            if follow_route is None:
                return ret_val
            in_route = follow_route
            ret_val |= follow_route
        return ret_val

    def find_route(self, from_junction_id: str, to_junction_id: str, from_route: Route = None) -> Optional[Route]:
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

    def get_network_length(self) -> int:
        """
        :return: length of all edges in network
        """
        ret_val: int = 0
        for edge in self.edges.values():
            ret_val += round(edge.get_length())
        return ret_val

    def set_name(self, name: str) -> None:
        """
        :param name: of skeleton to be set
        :return: None
        """
        self.type.name = name

    def get_name(self) -> str:
        """
        :return: name of subgraph
        """
        return self.type.name

    def load(self, other: 'Skeleton') -> bool:
        """
        Loads skeleton from another skeleton class

        :param other: Skeleton Class (loaded from the same file)
        :return: True on success, false otherwise
        """
        if not isinstance(other, Skeleton):
            print("Can only load Skeleton class from other Skeleton class!")
            return False
        self.junctions = deepcopy(other.junctions)
        self.edges = deepcopy(other.edges)
        self.routes = deepcopy(other.routes)
        self.starting_junctions = deepcopy(other.starting_junctions)
        self.ending_junctions = deepcopy(other.ending_junctions)
        self.roundabouts = deepcopy(other.roundabouts)
        self.type = deepcopy(other.type)
        self.map_name = deepcopy(other.map_name)
        return True
