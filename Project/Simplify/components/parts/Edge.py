from Project.Simplify.components.parts.Figure import Figure
from Project.Utils.xml_object import XmlObject
from Project.Utils.constants import EDGE_ATTRIBUTES, LANE_ATTRIBUTES, EDGE_DEFAULT_COLOR
from typing import Tuple, List


class Edge(Figure, XmlObject):
    """ Class describing Edge of road network from .net.xml file """

    def __init__(self, attributes: dict):
        Figure.__init__(self, EDGE_DEFAULT_COLOR)
        XmlObject.__init__(self, "edge")
        # Main attributes of Edge extracted from network (.net.xml) file
        [self.attributes.update({key: value}) for key, value in attributes.items() if key in EDGE_ATTRIBUTES]
        self.lanes: dict = {}
        self.LINE_WIDTH: float = 1  # Thickness of displayed line

    def add_lane(self, lane: dict) -> None:
        """
        :param lane: dictionary holding attributes of lane
        :return: None
        """
        self.lanes[lane["id"]] = {key: lane[key] for key in lane if key in LANE_ATTRIBUTES}
        self.attributes["length"] = float(lane["length"])  # measured in meters
        self.attributes["speed"] = float(lane["speed"])  # measured in meters/second, maximal speed on edge

    def travel(self) -> Tuple[str, float]:
        """
        :return: Tuple containing destination junction id and length
        """
        return self.attributes["to"], self.attributes["length"]

    def get_lane_shape(self, lane_id: str) -> List[List[float]]:
        """
        :param lane_id: of lane
        :return: list of lists containing pairs of x,y coordinates
        """
        points: list = self.lanes[lane_id]["shape"].split()
        points = [list(map(float, i.split(","))) for i in points]
        return points

    def get_length(self) -> float:
        """
        :return: -1 if parameter length does not exist, else length of
        lane (it is assumed, all lanes of edge have the same length)
        """
        if "length" not in self.attributes:
            return -1
        return self.attributes["length"]

    def get_lane_count(self) -> int:
        """
        :return:
        """
        return len(self.lanes.keys())

    def plot(self, axes, color: str = "") -> None:
        color = (color if color != "" else self.color)
        for lane_id in self.lanes:
            # [[x, y], [x, y], ...]
            points: list = self.get_lane_shape(lane_id)
            for i in range(1, len(points)):
                x: list = [points[i-1][0], points[i][0]]
                y: list = [points[i-1][1], points[i][1]]
                axes.plot(x, y, linewidth=self.LINE_WIDTH, color=color)

    # -------------------------------- Magic Methods --------------------------------

    def __eq__(self, another) -> bool:
        """
        :param another: object of comparison
        :return: True if objects are equal, false otherwise
        """
        return isinstance(another, Edge) and self.attributes["id"] == another.attributes["id"]

    def __hash__(self) -> int:
        """
        :return: Hash of attribute 'id'
        """
        return hash(self.attributes["id"])
