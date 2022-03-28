from os.path import isfile, dirname, abspath
from pathlib import Path
from typing import FrozenSet
# ----------- Edges -----------
EDGE_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "from", "to", "type", "shape"])
LANE_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "length", "speed", "shape"])
EDGE_DEFAULT_COLOR: str = "#999999"  # grey
# ----------- Junctions -----------
JUNCTION_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "type", "x", "y", "shape"])
JUNCTION_DEFAULT_COLOR: str = "white"
JUNCTION_START_COLOR: str = "green"
JUNCTION_END_COLOR: str = "blue"
JUNCTION_START_END_COLOR: str = "#FFD632"  # "turquoise"
# ---------- Path  ----------
CWD: str = dirname(abspath(__file__))  # Project Root


def file_exists(file_name: str) -> bool:
    """
    :param file_name: of file to be loaded
    :return: true if file exists, false otherwise
    """
    if isinstance(file_name, str) and isfile(file_name):
        return True
    print(f"File: {file_name} does not exist!")
    return False
