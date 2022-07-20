from os.path import isfile, isdir
from typing import FrozenSet, List
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
    CWD: str = str(Pt(__file__).parent.parent)  # Project Root
    OSM_FILTER: str = (CWD + "/Converter/OSMfilter/osmfilter")  # Path to osmfilter (executable)
    # Template for '.sumocfg' file
    SUMO_CONFIG_TEMPLATE: str = (CWD + "/Traci/scenarios/generators/templates/sumo_config_template.xml")
    # Template for '.ruo.xml' file
    SUMO_ROUTES_TEMPLATE: str = (CWD + "/Traci/scenarios/generators/templates/sumo_routes_template.xml")
    # -------------------------------------- Maps --------------------------------------
    # Path to folder containing maps from open street map (.osm)
    ORIGINAL_OSM_MAPS: str = (CWD + "/Maps/osm/original/{0}.osm")
    # Path to folder containing filtered .osm maps
    FILTERED_OSM_MAPS: str = (CWD + "/Maps/osm/filtered/{0}_filtered.osm")
    # Path to folder containing .net.xml maps for SUMO
    NETWORK_SUMO_MAPS: str = (CWD + "/Maps/sumo/{0}.net.xml")
    # --------------------------------------  Pddl --------------------------------------
    PDDL_DOMAINS: str = (CWD + "/Pddl/Domains/{0}.pddl")  # Path to folder containing pddl domains
    PDDL_PLANERS: str = (CWD + "/Pddl/Planners/{0}")   # Path to folder containing pddl planners
    PDDL_GENERATED_PROBLEMS: str = (CWD + "/Pddl/Problems/generated/{0}")  # Path to folder containing pddl problems
    # Path to folder containing results of pddl problems
    PDDL_SOLVED_PROBLEMS: str = (CWD + "/Pddl/Problems/solved/{0}")
    # -------------------------------------- Traci --------------------------------------
    TRACI_SCENARIOS: str = (CWD + "/Traci/scenarios/{0}")  # Path to generated scenarios for SUMO
    TRACI_SIMULATION: str = (CWD + "/Traci/scenarios/{0}/{1}.sumocfg")  # Path to generated '.sumocfg' file
    TRACI_ROUTES: str = (CWD + "/Traci/scenarios/{0}/{1}.rou.xml")  # Path to generated '.ruo.xml' file
    TRACI_SCENARIOS_PROBLEMS: str = (CWD + "/Traci/scenarios/{0}/problems/{1}.pddl")  # Path to folder with pddl problems
    TRACI_SCENARIOS_RESULTS: str = (CWD + "/Traci/scenarios/{0}/results/{1}.pddl")  # Path to folder with pddl results


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


def scenario_is_valid(scenario: str) -> bool:
    """
    :param scenario: name of scenario
    :return: true, if scenario is correct -> (has /problems, /results, 'routes.rou.xml', 'simulation.sumocfg' file)
    false otherwise
    """
    if not dir_exist(PATH.TRACI_SCENARIOS.format(scenario)):
        return False
    elif not file_exists(PATH.TRACI_SIMULATION.format(scenario, "simulation")):
        return False
    elif not file_exists(PATH.TRACI_ROUTES.format(scenario, "routes")):
        return False
    elif not dir_exist(PATH.TRACI_SCENARIOS.format(scenario) + "/problems"):
        return False
    elif not dir_exist(PATH.TRACI_SCENARIOS.format(scenario) + "/results"):
        return False
    return True
