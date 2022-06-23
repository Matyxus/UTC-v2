from Project.Simplify.Components.Parts.Figure import Figure
from Project.Simplify.Components.Parts.Edge import Edge
from Project.Utils import XmlObject
from Project.Utils.constants import EDGE_DEFAULT_COLOR
from typing import List, Tuple


class Route(Figure, XmlObject):
    """ Route is class holding edges, trough which the route goes """

    _counter: int = 0  # Variable serving to count number of class instances (to assign id's to routes)

    def __init__(self, identifier: int, edges: List[Edge]):
        Figure.__init__(self, color=EDGE_DEFAULT_COLOR)
        XmlObject.__init__(self, tag="route")
        self.id = identifier
        self.edge_list: List[Edge] = edges
        self.attributes["edges"] = ""
        self.attributes["id"] = f"r{Route._counter}"
        Route._counter += 1

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
            distance += edge.attributes["length"]
        return distance, self.get_destination()

    # ---------------------------- Getters ----------------------------

    def get_destination(self) -> str:
        """
        :return: Id of junction route leads to
        """
        assert (self.last_edge() is not None)
        return self.last_edge().attributes["to"]

    def get_start(self) -> str:
        """
        :return: Id of junction, route starts at
        """
        assert (self.first_edge() is not None)
        return self.first_edge().attributes["from"]

    def get_junctions(self) -> List[str]:
        """
        :return: List of junction id's route goes trough, empty if route is empty
        """
        ret_val: List[str] = []
        if len(self.edge_list) == 0:
            return ret_val
        ret_val.append(self.first_edge().attributes["from"])
        for edge in self.edge_list:
            ret_val.append(edge.attributes["to"])
        return ret_val

    def get_edge_ids(self) -> List[str]:
        """
        :return: List of all edge id's
        """
        return [edge.attributes["id"] for edge in self.edge_list]

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

    def __or__(self, other):
        """
        :param other:
        :return:
        """
        if isinstance(other, Route):
            for edge in other.edge_list:
                self.edge_list.append(edge)
        return self

    def __ror__(self, other):
        """
        :param other:
        :return:
        """
        return self.__or__(other)

    def __str__(self) -> str:
        """
        :return:
        """
        return f"Route: {self.id}, path: {[edge.attributes['id'] for edge in self.edge_list]}"

    def __eq__(self, another) -> bool:
        """
        :param another: object of comparison
        :return: True if objects are equal, false otherwise
        """
        return isinstance(another, Route) and self.id == another.id

    def __hash__(self) -> int:
        """
        :return: Hash of attribute 'id'
        """
        return hash(self.id)
