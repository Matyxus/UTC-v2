from typing import Tuple, List, Dict
from utc.src.graph.utils import Attributes, Colors
from utc.src.graph.components.parts.figure import Figure
from utc.src.graph.components.parts.route import Route
from utc.src.utils.xml_object import XmlObject


class Junction(Figure, XmlObject):
    """ Class representing junction from .net.xml file """

    def __init__(self, attributes: dict):
        Figure.__init__(self, Colors.JUNCTION_COLOR)
        XmlObject.__init__(self, "junction")
        # Main attributes of Junction extracted from network (.net.xml) file
        [
            self.attributes.update({key: value}) for key, value in attributes.items()
            if key in Attributes.JUNCTION_ATTRIBUTES
        ]
        # Mapping incoming routes to possible out-coming routes
        self.neighbours: Dict[Route, List[Route]] = {}
        self.MARKER_SIZE: int = 8  # Size of displayed point (representing junction)
        self.TEXT_SIZE: int = 6  # Size of annotated text written on junction (its id)
        self.traffic_lights: bool = False
    
    def add_connection(self, from_route: Route, out_route: Route) -> None:
        """
        :param from_route: incoming route to this node
        :param out_route: route going from this node (if we came into junction using from_route)
        :return: None
        """
        if from_route not in self.neighbours:
            self.neighbours[from_route] = []
        self.neighbours[from_route].append(out_route)

    def remove_out_route(self, route: Route) -> None:
        """
        :param route: outgoing route to be removed
        :return: None
        """
        for in_route, out_routes in self.neighbours.items():
            if route in out_routes:
                # Remove mapping from list
                out_routes.remove(route)

    def remove_in_route(self, route: Route) -> None:
        """
        :param route: incoming route to be removed
        :return: None
        """
        assert (route in self.neighbours)
        self.neighbours.pop(route)

    def replace_in_route(self, in_route: Route, new_in_route: Route) -> None:
        """
        :param in_route: to be replaced
        :param new_in_route: replacing
        :return: None
        """
        assert (in_route in self.neighbours)
        assert (new_in_route not in self.neighbours)
        self.neighbours[new_in_route] = self.neighbours.pop(in_route)

    def travel(self, from_route: Route) -> List[Route]:
        """
        :param from_route: one of incoming routes, if equal to None, returns all routes
        :return: list of routes
        """
        if from_route is None:  # Return all possible out routes
            return self.get_out_routes()
        assert (from_route in self.neighbours)
        return self.neighbours[from_route]

    def set_traffic_lights(self, has: bool) -> None:
        """
        :param has: true if junction has traffic lights
        :return: None
        """
        self.traffic_lights = has

    def is_traffic_light(self) -> bool:
        """
        :return: true if junction has traffic lights, false otherwise
        """
        return self.traffic_lights

    def plot(self, axes, color: str = "") -> None:
        color = (color if color != "" else self.color)
        pos: Tuple[float, float] = self.get_position()
        axes.plot(pos[0], pos[1], marker="o", markersize=self.MARKER_SIZE, color=color)
        axes.annotate(
            self.get_id(), xy=(pos[0], pos[1]), color='black',
            fontsize=self.TEXT_SIZE, weight='normal',
            horizontalalignment='center', verticalalignment='center'
        )

    # -------------------------------- Getters --------------------------------

    def get_position(self) -> Tuple[float, float]:
        """
        :return: Tuple containing (x, y) coordinates
        """
        return float(self.get_attribute("x")), float(self.get_attribute("y"))

    def get_in_routes(self) -> List[Route]:
        """
        :return: List of in_edge_id's
        """
        return list(self.neighbours.keys())

    def get_out_routes(self) -> List[Route]:
        """
        :return: List of all out coming routes
        """
        return [route for route_list in self.neighbours.values() for route in route_list]

    # -------------------------------- Magic Methods --------------------------------

    def __str__(self) -> str:
        ret_val: str = f"Junction: {self.get_id()}\n"
        for in_route, out_routes in self.neighbours.items():
            ret_val += f"From: {in_route} to: \n"
            for out_route in out_routes:
                ret_val += f"\t{out_route}\n"
        return ret_val

    def __or__(self, other) -> 'Junction':
        """
        Merges with another junction (of same attributes), but with different connections

        :param other: junction
        :return: self
        """
        if other != self:
            raise TypeError(f"Expected other to be of type: 'Junction', got: '{type(other)}'")
        for in_route, out_routes in other.neighbours.items():
            if in_route not in self.neighbours:  # Add new mapping
                self.neighbours[in_route] = out_routes
            else:  # Merge out_routes
                for out_route_id in out_routes:
                    if out_route_id not in self.neighbours[in_route]:
                        self.neighbours[in_route].append(out_route_id)
        return self

    def __ror__(self, other) -> 'Junction':
        """
        :param other: junction
        :return: self.__or__(other)
        """
        return self.__or__(other)
