from typing import FrozenSet


class Attributes:
    """
    Class containing constant variables for default (wanted) attributes of edges/junctions/lanes
    """
    EDGE_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "from", "to", "type", "shape"])
    LANE_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "length", "speed", "shape"])
    JUNCTION_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "type", "x", "y", "shape"])


class Colors:
    """
    Class containing constant variables for default colors of edges/junctions
    """
    EDGE_COLOR: str = "#999999"  # grey
    JUNCTION_COLOR: str = "white"
    JUNCTION_START_COLOR: str = "green"
    JUNCTION_END_COLOR: str = "blue"
    JUNCTION_START_END_COLOR: str = "#FFD632"  # "turquoise"
