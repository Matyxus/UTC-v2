from os.path import isfile, dirname, abspath, isdir
from typing import FrozenSet, Dict
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


class Path:
    """ (static) Class holding different project paths """
    OSM_FILTER: str = (CWD + "/Converter/OSMfilter/osmfilter")  # Path to osmfilter (executable)
    # Maps
    ORIGINAL_OSM_MAPS: str = (CWD + "/Maps/osm/original/")  # Path to folder containing maps from open street map (.osm)
    FILTERED_OSM_MAPS: str = (CWD + "/Maps/osm/filtered/")  # Path to folder containing filtered .osm maps
    NETWORK_SUMO_MAPS: str = (CWD + "/Maps/sumo/")  # Path to folder containing .net.xml maps for SUMO
    # Pddl
    PDDL_DOMAINS: str = (CWD + "/Pddl/Domain/Domains/")  # Path to folder containing domains for pddl problems
    PDDL_PLANERS: str = (CWD + "/Pddl/Planners/")   # Path to folder containing pddl planners
    PDDL_GENERATED_PROBLEMS: str = (CWD + "/Pddl/Problems/generated/")  # Path to folder containing pddl problems
    PDDL_SOLVED_PROBLEMS: str = (CWD + "/Pddl/Problems/solved/")  # Path to folder containing results of pddl problems
    # Planners
    PLANNERS: Dict[str, str] = {
        # Planner_name : command to run planner (.format string)
        "Cerberus": "python3 " + PDDL_PLANERS + "Cerberus/plan.py" + " {0} {1} {2}",
        "Merwin": PDDL_PLANERS + "Merwin/plan" + " {0} {1} {2}"
    }


def file_exists(file_name: str) -> bool:
    """
    :param file_name: of file to be checked
    :return: true if file exists, false otherwise
    """
    if isinstance(file_name, str) and isfile(file_name):
        return True
    print(f"File: {file_name} does not exist!")
    return False


def dir_exist(dir_name: str) -> bool:
    """
    :param dir_name: of directory to be checked
    :return: true if directory exists, false otherwise
    """
    if isinstance(dir_name, str) and isdir(dir_name):
        return True
    print(f"File: {dir_name} does not exist!")
    return False


