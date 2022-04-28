from os.path import isfile, dirname, abspath, isdir
from typing import FrozenSet, Dict
from pathlib import Path as Pt  # Avoid confusion with PATH Class
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


#  ---------------------------------- Path ----------------------------------
class PATH:
    """ (static) Class holding different project paths, used with .format(args) """
    CWD: str = str(Pt(__file__).parent.parent)  # Project Root
    OSM_FILTER: str = (CWD + "/Converter/OSMfilter/osmfilter")  # Path to osmfilter (executable)
    # Path to template of sumo config file
    SUMO_CONFIG_TEMPLATE: str = (CWD + "/Traci/scenarios/sumo_config_template.xml")
    # -------------- Maps --------------
    # Path to folder containing maps from open street map (.osm)
    ORIGINAL_OSM_MAPS: str = (CWD + "/Maps/osm/original/{0}.osm")
    # Path to folder containing filtered .osm maps
    FILTERED_OSM_MAPS: str = (CWD + "/Maps/osm/filtered/{0}_filtered.osm")
    NETWORK_SUMO_MAPS: str = (CWD + "/Maps/sumo/{0}.net.xml")  # Path to folder containing .net.xml maps for SUMO
    #  -------------- Pddl --------------
    PDDL_DOMAINS: str = (CWD + "/Pddl/Domain/Domains/{0}")  # Path to folder containing pddl domains
    PDDL_PLANERS: str = (CWD + "/Pddl/Planners/{0}")   # Path to folder containing pddl planners
    PDDL_GENERATED_PROBLEMS: str = (CWD + "/Pddl/Problems/generated/{0}")  # Path to folder containing pddl problems
    # Path to folder containing results of pddl problems
    PDDL_SOLVED_PROBLEMS: str = (CWD + "/Pddl/Problems/solved/{0}")
    # -------------- Planners --------------
    PLANNERS: Dict[str, str] = {
        # Planner_name : command to run planner (.format(args) string)
        "Cerberus": "python3 " + PDDL_PLANERS + "Cerberus/plan.py" + " {0} {1} {2}",
        "Merwin": PDDL_PLANERS + "Merwin/plan" + " {0} {1} {2}"
    }
    # -------------- Traci --------------
    TRACI_SCENARIOS: str = (CWD + "/Traci/scenarios/{0}")  # Path to generated scenarios for SUMO


# ---------------------------------- Functions ----------------------------------

def get_file_name(file_name: str) -> str:
    """
    :param file_name: of file (can be path)
    :return: name of file
    """
    if not file_name:
        return file_name
    return Pt(file_name).stem


def file_exists(file_name: str, message: bool = True) -> bool:
    """
    :param file_name: of file to be checked
    :param message: optional argument, (default True), if message 'File .. does not exist' should be printed
    :return: true if file exists, false otherwise
    """
    if isinstance(file_name, str) and isfile(file_name):
        return True
    if message:
        print(f"File: {file_name} does not exist!")
    return False


def dir_exist(dir_name: str, message: bool = True) -> bool:
    """
    :param dir_name: of directory to be checked
    :param message: optional argument, (default True), if message 'Directory .. does not exist' should be printed
    :return: true if directory exists, false otherwise
    """
    if isinstance(dir_name, str) and isdir(dir_name):
        return True
    if message:
        print(f"Directory: {dir_name} does not exist!")
    return False
