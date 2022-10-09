from utc.src.graph.components.parts.figure import Figure
from utc.src.graph.components.parts.edge import Edge
from utc.src.utils import XmlObject
from utc.src.graph.utils import Colors
from typing import List, Tuple, Union


class Route(Figure, XmlObject):
    """ Route is class holding edges, trough which the route goes """

    _counter: int = 0  # Variable serving to count number of class instances (to assign id's to routes)

    def __init__(self, edges: List[Edge], route_id: int = None):
        """
        :param edges: list of edges forming route
        :param route_id: optional argument, if route is loaded from file
        value should be set, otherwise None
        """
        Figure.__init__(self, color=Colors.EDGE_COLOR)
        XmlObject.__init__(self, tag="route")
        self.edge_list: List[Edge] = edges
        self.attributes["edges"] = ""
        self.attributes["id"] = self.set_id(route_id)
        Route._counter += 1

    def set_id(self, route_id: int = None) -> str:
        """
        :param route_id: to be et
        :return:
        """
        if route_id is None:
            return f"r{Route._counter}"
        return f"r{route_id}"

    def plot(self, axes, color: str = "") -> None:
        """
        :param axes: of pyplot on which plotting will be done
        :param color: of route
        :return: None
        """
        # color = (color if color != "" else EDGE_DEFAULT_COLOR)
        # Plot edges on the route
        for edge in self.edge_list:
            edge.plot(axes, color)

    def traverse(self) -> Tuple[float, str]:
        """
        :return: tuple containing length of route and its destination (as junction id)
        """
        distance: float = 0
        for edge in self.edge_list:
            distance += edge.get_length()
        return round(distance, 2), self.get_destination()

    # ---------------------------- Getters ----------------------------

    def get_destination(self) -> str:
        """
        :return: Id of junction route leads to
        """
        return self.last_edge().get_attribute("to")

    def get_start(self) -> str:
        """
        :return: Id of junction, route starts at
        """
        return self.first_edge().get_attribute("from")

    def get_junctions(self) -> List[str]:
        """
        :return: List of junction id's route goes trough, empty if route is empty
        """
        ret_val: List[str] = []
        if len(self.edge_list) == 0:
            return ret_val
        ret_val.append(self.first_edge().get_attribute("from"))
        for edge in self.edge_list:
            ret_val.append(edge.get_attribute("to"))
        return ret_val

    def get_edge_ids(self, as_int: bool = False) -> List[Union[str, int]]:
        """
        :param as_int: true if edge ids should be returned as integers (default false)
        :return: List of all edge id's
        """
        if as_int:
            return [int(edge.get_id()) for edge in self.edge_list]
        return [edge.get_id() for edge in self.edge_list]

    # ---------------------------- Utils ----------------------------

    def last_edge(self) -> Edge:
        """
        :return: Id of last edge on route
        """
        return self.edge_list[-1]

    def first_edge(self) -> Edge:
        """
        :return: Id of first edge on route
        """
        return self.edge_list[0]

    def to_xml(self):
        self.attributes["edges"] = " ".join(self.get_edge_ids())
        self.attributes["fromJunction"] = self.get_start()
        self.attributes["toJunction"] = self.get_destination()
        return super().to_xml()

    # -------------------------------- Magic Methods --------------------------------

    def __or__(self, other: 'Route') -> 'Route':
        """
        :param other: route to be merged with
        :return: self merged with other Route
        """
        if isinstance(other, Route):
            for edge in other.edge_list:
                self.edge_list.append(edge)
        return self

    def __ror__(self, other: 'Route') -> 'Route':
        """
        :param other: route to be merged with
        :return: self merged with other Route
        """
        return self.__or__(other)

    def __str__(self) -> str:
        """
        :return:
        """
        return f"Route: {self.get_id()}, path: {[edge.get_id() for edge in self.edge_list]}"

    def __lt__(self, other: 'Route') -> bool:
        """
        :param other: route to compare with
        :return: true if other route id is less than self
        """
        return int(other.get_id()[1:]) < int(self.get_id()[1:])

    def __le__(self, other: 'Route') -> bool:
        """
        :param other: route to compare with
        :return: true if other route id is less than or equal to  self
        """
        if self < other:
            return True
        return int(other.get_id()[1:]) == int(self.get_id()[1:])
