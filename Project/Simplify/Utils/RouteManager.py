from typing import Tuple, List
from Components import Struct, Route


class RouteManager:
    """ Class for managing route class """

    def __init__(self, struct: Struct):
        print("Initializing RouteManager")
        self.index: int = 0  # For generating new id's of routes, has to start at 0 !
        self.struct: Struct = struct

    def add_route(self, route: Route) -> None:
        """
        :param route: to be added to dictionary of routes
        :return: None
        """
        assert (route.id not in self.struct.routes)
        self.struct.routes[route.id] = route

    def traverse(self, route_id: int) -> Tuple[float, str]:
        """
        :return: tuple containing length of  route and destination junction id
        """
        distance: float = 0
        for edge_id in self.struct.routes[route_id].edge_list:
            distance += self.struct.edges[edge_id].attributes["length"]
        return (distance, self.get_destination(route_id))

    def construct_route(self, junction_list: List[str]) -> Route:
        """
        :param junction_list: of junctions on path
        :return: None in case junction is empty or path does not exist, route otherwise
        """
        if len(junction_list) == 0:
            return None
        ret_val: Route = Route(-1,  [])
        in_route: int = 0
        for i in range(0, len(junction_list)-1):
            # Also sets self.route as current one
            follow_route: Route = self.find_route(junction_list[i], junction_list[i+1], in_route)
            if follow_route is None:
                return ret_val
            in_route = follow_route.id
            ret_val |= follow_route
        return ret_val

    def find_route(self, from_junction_id: str, to_junction_id: str, from_route_id: int = 0) -> Route:
        """
        :param from_route_id: optional parameter, incoming route to from_junction_id
        :param from_junction_id: starting junction
        :param to_junction_id: target junction (must be neighbour)
        :return: Route between junctions, None if it doesn't exist
        """
        for route_id in self.struct.junctions[from_junction_id].travel(from_route_id):
            if self.get_destination(route_id) == to_junction_id:
                return self.struct.routes[route_id]
        return None

    def get_destination(self, route_id: int) -> str:
        """
        :return: Id of junction route leads to
        """
        return self.struct.edges[self.struct.routes[route_id].last_edge()].attributes["to"]

    def get_start(self, route_id: int) -> str:
        """
        :param route_id:
        :return: Id of junction, route starts at
        """
        return self.struct.edges[self.struct.routes[route_id].first_edge()].attributes["from"]

    def get_new_route_id(self) -> int:
        """
        :return: new id of route
        """
        self.index += 1
        return self.index

    def get_new_route(self) -> Route:
        """
        :return: new route, with new route_id, empty edge_list
        """
        return Route(self.get_new_route_id(), [])

    def get_junctions(self, route: Route) -> List[str]:
        """
        :param route:
        :return:
        """
        assert (route is not None)
        junctions: List[str] = [self.struct.edges[route.edge_list[0]].attributes["from"]]
        for edge_id in route.edge_list:
            junctions.append(self.struct.edges[edge_id].attributes["to"])
        return junctions

    def plot(self, axes, route: Route, color: str = "") -> None:
        """
        :param axes: of pyplot on which plotting will be done
        :param route: to be plotted
        :param color: of route
        :return: None
        """
        if route.render:
            color = (color if color != "" else route.color)
            # Plot edges on the route
            for edge_id in route.edge_list:
                assert (edge_id in self.struct.edges)
                self.struct.edges[edge_id].plot(axes, color)
