from utc.src.graph.components.parts.figure import Figure
from utc.src.utils.xml_object import XmlObject
from utc.src.graph.utils import Attributes, Colors
from typing import Tuple, List


class Edge(Figure, XmlObject):
    """ Class describing Edge of road network from .net.xml file """

    def __init__(self, attributes: dict):
        Figure.__init__(self, Colors.EDGE_COLOR)
        XmlObject.__init__(self, "edge")
        # Main attributes of Edge extracted from network (.net.xml) file
        [
            self.attributes.update({key: value}) for key, value in attributes.items()
            if key in Attributes.EDGE_ATTRIBUTES
        ]
        self.lanes: dict = {}
        self.LINE_WIDTH: float = 1  # Thickness of displayed line

    def add_lane(self, lane: dict) -> None:
        """
        :param lane: dictionary holding attributes of lane
        :return: None
        """
        self.lanes[lane["id"]] = {key: lane[key] for key in lane if key in Attributes.LANE_ATTRIBUTES}
        self.attributes["length"] = lane["length"]  # measured in meters
        self.attributes["speed"] = lane["speed"]  # measured in meters/second, maximal speed on edge

    # ------------------------------------------ Getters ------------------------------------------

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
        :return: length of lane (it is assumed, all lanes of edge have the same length)
        """
        return float(self.get_attribute("length"))

    def get_speed(self) -> float:
        """
        :return: maximal allowed speed (m/s)
        """
        return round(float(self.get_attribute("speed")), 3)

    def get_lane_count(self) -> int:
        """
        :return: number of lanes on Edge
        """
        return len(self.lanes.keys())

    # ------------------------------------------ Utils ------------------------------------------

    def travel(self) -> Tuple[str, float]:
        """
        :return: Tuple containing destination junction id and length
        """
        return self.get_attribute("to"), self.get_length()

    def plot(self, axes, color: str = "") -> None:
        color = (color if color != "" else self.color)
        for lane_id in self.lanes:
            # [[x, y], [x, y], ...]
            points: list = self.get_lane_shape(lane_id)
            for i in range(1, len(points)):
                x: list = [points[i-1][0], points[i][0]]
                y: list = [points[i-1][1], points[i][1]]
                axes.plot(x, y, linewidth=self.LINE_WIDTH, color=color)
