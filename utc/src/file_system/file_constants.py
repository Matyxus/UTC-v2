from pathlib import Path


# ---------------------------------- Extension ----------------------------------
class FileExtension:
    """ Class holding extension of files """
    PDDL: str = ".pddl"
    XML: str = ".xml"
    INFO: str = ".info"
    PROB: str = ".prob"
    JSON: str = ".json"
    CSV: str = ".csv"
    # ------- Simulation -------
    SUMO_ROUTES: str = ".rou.xml"
    SUMO_CONFIG: str = ".sumocfg"  # (is of xml type)
    SUMO_STATS: str = ".stat.xml"  # statistics file
    # ------- Maps -------
    SUMO_NETWORK: str = ".net.xml"
    OSM: str = ".osm"


# ---------------------------------- CWD ----------------------------------

def initialize_cwd() -> str:
    """
    :raise ValueError: in case directory 'utc' cannot be found in path
    :return: absolute path to project root ('UTC/utc')
    """
    cwd: Path = Path(__file__)
    if "utc" not in str(cwd):
        raise ValueError(
            "Location of 'file_constants.py' file is incorrect,"
            f" unable to find 'utc' in {str(cwd)} !"
        )
    while not str(cwd).endswith("utc"):
        cwd = cwd.parent
    return str(cwd)

# -------------------------------------------- Paths --------------------------------------------


class DirPaths:
    """
    Class holding different project paths for directories, used with .format(args) (not always),
    where args is the name of directory
    """
    CWD: str = initialize_cwd()  # Project Root (UTC/utc)
    # -------------------------------------- Maps --------------------------------------
    MAPS: str = (CWD + "/data/maps")  # Path to folder containing folders related to maps
    MAPS_INFO: str = (MAPS + "/information")  # Path to folder containing '.info' files
    MAPS_PROB: str = (MAPS + "/probability")  # Path to folder containing '.prob' probability files
    MAPS_OSM: str = (MAPS + "/osm")  # Path to folder containing maps from open street map (".osm")
    MAPS_FILTERED: str = (MAPS + "/filtered")  # Path to folder containing filtered ".osm" maps
    MAPS_SUMO: str = (MAPS + "/sumo")  # Path to folder containing ".net.xml" maps for SUMO
    # -------------------------------------- Sessions --------------------------------------
    SESSIONS: str = (CWD + "/data/sessions")
    # -------------------------------------- Scenarios --------------------------------------
    SCENARIO: str = (CWD + "/data/scenarios/{0}")
    # Pddl
    PDDL_DOMAINS: str = (CWD + "/data/domains")
    PDDL_PLANNERS: str = (CWD + "/data/planners/{0}")
    PDDL_PROBLEMS: str = (SCENARIO + "/problems")
    SCENARIO_PROBLEMS: str = (PDDL_PROBLEMS + "/{1}")  # Path to specific scenario folder in problems directory
    PDDL_RESULTS: str = (SCENARIO + "/results")
    SCENARIO_RESULTS: str = (PDDL_RESULTS + "/{1}")  # Path to specific scenario folder in results directory
    # Maps (specific to scenarios)
    SCENARIO_MAPS: str = (SCENARIO + "/maps")
    SCENARIO_MAPS_INFOS: str = (SCENARIO_MAPS + "/information")
    SCENARIO_MAPS_NETWORKS: str = (SCENARIO_MAPS + "/networks")
    # Routes
    SCENARIO_ROUTES: str = (SCENARIO + "/routes")
    # Simulation
    SCENARIO_SIMULATIONS: str = (SCENARIO + "/simulation")
    SCENARIO_STATISTICS: str = (SCENARIO_SIMULATIONS + "/statistics")
    SCENARIO_CONFIGS: str = (SCENARIO_SIMULATIONS + "/config")
    SCENARIO_INFOS: str = (SCENARIO_SIMULATIONS + "/information")
    # Planner output
    SCENARIO_PLANNER_OUTS: str = (SCENARIO + "/output")


class FilePaths:
    """
    Class holding different project paths for files, used with .format(args) (not always),
    where args is usually the name of file (without extension)
    """
    OSM_FILTER: str = (DirPaths.CWD + "/data/osm_filter/osmfilter")  # Path to osmfilter (executable)
    # -------------------------------------- Templates --------------------------------------
    # Template for '.sumocfg' file
    SUMO_CONFIG_TEMPLATE: str = (DirPaths.CWD + "/data/templates/sumo_config" + FileExtension.SUMO_CONFIG)
    # Template for '.ruo.xml' file
    SUMO_ROUTES_TEMPLATE: str = (DirPaths.CWD + "/data/templates/sumo_routes" + FileExtension.SUMO_ROUTES)
    SESSSION_TEMPLATE: str = (DirPaths.CWD + "/data/templates/template_session" + FileExtension.JSON)
    # -------------------------------------- Maps --------------------------------------
    MAP_INFO: str = (DirPaths.MAPS_INFO + "/{0}" + FileExtension.INFO)
    MAP_PROB: str = (DirPaths.MAPS_PROB + "/{0}" + FileExtension.PROB)
    # Path to file from open street map (".osm")
    MAP_OSM: str = (DirPaths.MAPS_OSM + "/{0}" + FileExtension.OSM)
    # Path to file of ".osm" map
    MAP_FILTERED: str = (DirPaths.MAPS_FILTERED + "/{0}" + FileExtension.OSM)
    # Path to '.net.xml' file map for SUMO
    MAP_SUMO: str = (DirPaths.MAPS_SUMO + "/{0}" + FileExtension.SUMO_NETWORK)
    # --------------------------------------  Pddl --------------------------------------
    PDDL_DOMAIN: str = (DirPaths.PDDL_DOMAINS + "/{0}" + FileExtension.PDDL)
    # Path scenarios specific pddl problem file
    PDDL_PROBLEM: str = (DirPaths.SCENARIO_PROBLEMS + "/{2}" + FileExtension.PDDL)
    # Path scenarios specific pddl result file
    PDDL_RESULT: str = (DirPaths.SCENARIO_RESULTS + "/{2}" + FileExtension.PDDL)
    # -------------------------------------- Scenarios --------------------------------------
    # Path to '.rou.xml' file specific to scenario
    SCENARIO_ROUTES: str = (DirPaths.SCENARIO_ROUTES + "/{1}" + FileExtension.SUMO_ROUTES)
    # Path to '.sumocfg' file specific to scenario
    SCENARIO_CONFIG: str = (DirPaths.SCENARIO_CONFIGS + "/{1}" + FileExtension.SUMO_CONFIG)
    # Path to '.info' file specific to scenario
    SCENARIO_INFO: str = (DirPaths.SCENARIO_INFOS + "/{1}" + FileExtension.INFO)
    # Path to '.stat.xml' file specific to scenario
    SCENARIO_STATISTICS: str = (DirPaths.SCENARIO_STATISTICS + "/{1}" + FileExtension.SUMO_STATS)
    # Path to '.net.xml' file specific to scenario
    SCENARIO_MAP: str = (DirPaths.SCENARIO_MAPS_NETWORKS + "/{1}" + FileExtension.SUMO_NETWORK)
    # Path to '.info' file specific '.net.xml' in scenario directory
    SCENARIO_MAP_INFO: str = (DirPaths.SCENARIO_MAPS_INFOS + "/{1}" + FileExtension.INFO)
    # Path to '.?' file specific to scenario
    SCENARIO_SESSION: str = (DirPaths.SCENARIO + "/{1}" + "?")
    # Path to '.csv' file containing comparison of scenarios in folder
    SCENARIO_COMPARISON: str = (DirPaths.SCENARIO + "/{1}" + FileExtension.CSV)
    # -------------------------------------- Session --------------------------------------
    # Path to '.json' session file
    SESSION: str = (DirPaths.SESSIONS + "/{0}" + FileExtension.JSON)


def resolve_relative(path: str) -> str:
    """
    :param path: relative path to file (e.g. ../../data)
    :return: transformed relative path to absolute
    """
    return str(Path(path).resolve())


# ---------------------------------- Planners ----------------------------------


class PLANNERS:
    """
    Class defining planner calls as format string (expected
    arguments are "domain_file.pddl" "problem_file.pddl" "result_file.pddl")
    """
    MERWIN: str = (DirPaths.PDDL_PLANNERS.format("Merwin/plan") + " {0} {1} {2}")
    MERCURY: str = (DirPaths.PDDL_PLANNERS.format("Mercury/plan-utc") + " {0} {1} {2}")

    @staticmethod
    def get_planner(planner_name: str) -> str:
        """
        Expecting the input of planner to be domain file, problem file, result file (name)

        :param planner_name: name of planner
        :return: format string for shell/cmd command of planner, empty if planner does not exist
        """
        planer: str = getattr(PLANNERS, planner_name.upper(), "")
        if not planer:
            print(f"Planner: {planner_name} is not defined in PLANNERS!")
        return planer


if __name__ == "__main__":
    print(FilePaths.PDDL_DOMAIN.format("utc"))

