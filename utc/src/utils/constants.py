from os.path import isfile, isdir
from typing import FrozenSet, List, Dict
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


# ---------------------------------- Path ----------------------------------
class PATH:
    """ (static) Class holding different project paths, used with .format(args) """
    CWD: str = str(Pt(__file__).parent.parent.parent)  # Project Root (UTC/utc)
    OSM_FILTER: str = (CWD + "/data/osm_filter/osmfilter")  # Path to osmfilter (executable)
    # -------------------------------------- Templates --------------------------------------
    SUMO_CONFIG_TEMPLATE: str = (CWD + "/data/templates/sumo_config.xml")   # Template for '.sumocfg' file
    SUMO_ROUTES_TEMPLATE: str = (CWD + "/data/templates/sumo_routes.xml")   # Template for '.ruo.xml' file
    # -------------------------------------- Maps --------------------------------------
    # Path to folder containing maps from open street map (.osm)
    ORIGINAL_OSM_MAPS: str = (CWD + "/data/maps/osm/original/{0}.osm")
    # Path to folder containing filtered .osm maps
    FILTERED_OSM_MAPS: str = (CWD + "/data/maps/osm/filtered/{0}_filtered.osm")
    # Path to folder containing .net.xml maps for SUMO
    NETWORK_SUMO_MAPS: str = (CWD + "/data/maps/sumo/{0}.net.xml")
    # --------------------------------------  Pddl --------------------------------------
    PDDL_DOMAINS: str = (CWD + "/data/domains/{0}.pddl")  # Path to folder containing pddl domains
    PDDL_PLANERS: str = (CWD + "/data/planners/{0}")   # Path to folder containing pddl planners
    # -------------------------------------- Scenarios --------------------------------------
    SCENARIO_PROBLEMS: str = (CWD + "/data/scenarios/problems/{0}.pddl")  # Path to folder with pddl problems
    SCENARIO_RESULTS: str = (CWD + "/data/scenarios/results/{0}.pddl")  # Path to folder with pddl results
    SCENARIO_ROUTES: str = (CWD + "/data/scenarios/routes/{0}.rou.xml")  # Path to generated '.rou.xml' file
    SCENARIO_STATISTICS: str = ""  # Path to generate statistics
    SCENARIO_SIMULATION: str = (CWD + "/data/scenarios/simulation/{0}.sumocfg")  # Path to generated '.sumocfg' file


# ---------------------------------- Planners ----------------------------------
class PLANNERS:
    """
    (static) Class defining planner calls as format string (expected
    arguments are "domain.pddl" "problem.pddl" "result_file.pddl")
    """
    CERBERUS: str = ("python3 " + PATH.PDDL_PLANERS.format("Cerberus/plan.py") + " {0} {1} {2}")
    MERWIN: str = (PATH.PDDL_PLANERS.format("Merwin/plan") + " {0} {1} {2}")


def get_planner(planner_name: str) -> str:
    """
    :param planner_name: name of planner
    :return: format string for shell/cmd command of planner, empty if planner does not exist
    """
    planer: str = getattr(PLANNERS, planner_name.upper(), "")
    if not planer:
        print(f"Planner: {planner_name} is not defined in PLANNERS!")
    elif not dir_exist(PATH.PDDL_PLANERS.format(planner_name)):
        return ""
    return planer


# ---------------------------------- Functions ----------------------------------

def get_file_name(file_path: str) -> str:
    """
    :param file_path: of file
    :return: name of file without extension
    """
    if not file_path:
        return file_path
    # Loop until suffix is removed
    while Pt(file_path).suffix != "":
        file_path = Pt(file_path).stem
    return file_path


def get_file_extension(file_path: str) -> List[str]:
    """
    :param file_path: of file
    :return: extension/s of file
    """
    if not file_path:
        return []
    return Pt(file_path).suffixes


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


# For testing purposes
if __name__ == "__main__":
    pass








