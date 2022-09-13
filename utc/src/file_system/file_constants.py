from pathlib import Path


# ---------------------------------- Extension ----------------------------------
class FileExtension:
    """ Class holding extension of files """
    PDDL: str = ".pddl"
    XML: str = ".xml"
    INFO: str = ".info"
    # ------- Simulation -------
    SUMO_ROUTES: str = ".rou.xml"
    SUMO_CONFIG: str = ".sumocfg"  # (is of xml type)
    SUMO_STATS: str = ".stat.xml"  # statistics file
    # ------- Maps -------
    SUMO_NETWORK: str = ".net.xml"
    OSM: str = ".osm"


# ---------------------------------- Path ----------------------------------

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


class FilePaths:
    """ Class holding different project paths, used with .format(args) """
    CWD: str = initialize_cwd()  # Project Root (UTC/utc)
    OSM_FILTER: str = (CWD + "/data/osm_filter/osmfilter")  # Path to osmfilter (executable)
    # -------------------------------------- Templates --------------------------------------
    # Template for '.sumocfg' file
    SUMO_CONFIG_TEMPLATE: str = (CWD + "/data/templates/sumo_config" + FileExtension.SUMO_CONFIG)
    # Template for '.ruo.xml' file
    SUMO_ROUTES_TEMPLATE: str = (CWD + "/data/templates/sumo_routes" + FileExtension.SUMO_ROUTES)
    # -------------------------------------- Maps --------------------------------------
    # Path to folder containing maps from open street map (.osm)
    ORIGINAL_OSM_MAPS: str = (CWD + "/data/maps/osm/original/{0}" + FileExtension.OSM)
    # Path to folder containing filtered .osm maps
    FILTERED_OSM_MAPS: str = (CWD + "/data/maps/osm/filtered/{0}_filtered" + FileExtension.OSM)
    # Path to folder containing .net.xml maps for SUMO
    NETWORK_SUMO_MAPS: str = (CWD + "/data/maps/sumo/{0}" + FileExtension.SUMO_NETWORK)
    MAPS_INFO: str = (CWD + "/data/maps/information/{0}" + FileExtension.INFO)
    # --------------------------------------  Pddl --------------------------------------
    PDDL_DOMAINS: str = (CWD + "/data/domains/{0}" + FileExtension.PDDL)  # Path to folder containing pddl domains
    PDDL_PLANERS: str = (CWD + "/data/planners/{0}")   # Path to folder containing pddl planners
    PDDL_PROBLEMS: str = (CWD + "/data/scenarios/problems")  # Path to folder containing pddl problems
    PDDL_RESULTS: str = (CWD + "/data/scenarios/results")  # Path to folder containing pddl results
    # -------------------------------------- Scenarios --------------------------------------
    # Path to folder with pddl problems (specific to scenario)
    SCENARIO_PROBLEMS: str = (CWD + "/data/scenarios/problems/{0}/{1}" + FileExtension.PDDL)
    # Path to folder with pddl results (specific to scenario)
    SCENARIO_RESULTS: str = (CWD + "/data/scenarios/results/{0}/{1}" + FileExtension.PDDL)
    # Path to generated '.rou.xml' file
    SCENARIO_ROUTES: str = (CWD + "/data/scenarios/routes/{0}" + FileExtension.SUMO_ROUTES)
    # Path to user-generated '.sumocfg' file (with ScenarioLauncher class)
    SCENARIO_SIM_GENERATED: str = (CWD + "/data/scenarios/simulation/generated/{0}" + FileExtension.SUMO_CONFIG)
    # Path to '.sumocfg' files made from ".pddl" result files generated by planner
    SCENARIO_SIM_PLANNED: str = (CWD + "/data/scenarios/simulation/planned/{0}" + FileExtension.SUMO_CONFIG)
    # Path to '.info' files (same name as ".sumocfg") describing used commands to generate original/planned scenarios
    SCENARIO_SIM_INFO: str = (CWD + "/data/scenarios/simulation/information/{0}" + FileExtension.INFO)
    # Path to generate statistics
    SCENARIO_STATISTICS: str = (CWD + "/data/scenarios/simulation/statistics/{0}" + FileExtension.SUMO_STATS)


# ---------------------------------- Planners ----------------------------------

class PLANNERS:
    """
    Class defining planner calls as format string (expected
    arguments are "domain_file.pddl" "problem_file.pddl" "result_file.pddl")
    """
    CERBERUS: str = ("python3 " + FilePaths.PDDL_PLANERS.format("Cerberus/plan.py") + " {0} {1} {2}")
    MERWIN: str = (FilePaths.PDDL_PLANERS.format("Merwin/plan") + " {0} {1} {2}")

    @staticmethod
    def get_planner(planner_name: str) -> str:
        """
        :param planner_name: name of planner
        :return: format string for shell/cmd command of planner, empty if planner does not exist
        """
        planer: str = getattr(PLANNERS, planner_name.upper(), "")
        if not planer:
            print(f"Planner: {planner_name} is not defined in PLANNERS!")
        return planer
