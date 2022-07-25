from utc.src.pddl.pddl_problem.pddl_problem import PddlProblem
from utc.src.pddl.pddl_problem.pddl_result import PddlResult
from utc.src.simulator.scenario.generators import ConfigGenerator, RoutesGenerator
from utc.src.graph.components import Graph, Skeleton
from utc.src.utils.constants import PATH, file_exists, get_file_name, dir_exist
from os import mkdir, listdir, rename
from typing import List


class PddlLauncher:
    """ Class that implements interface methods for generating pddl problems/results """

    def __init__(self):
        self.graph: Graph = None
        # -------------- Pddl --------------
        self.pddl_problem: PddlProblem = None
        self.pddl_result: PddlResult = None
        # function able to call commands into shell/cmd (expecting 'UserInterface.run_command')
        self.shell: callable = None
        # Scenario
        self.simulation: ConfigGenerator = None
        self.routes: RoutesGenerator = None
        self.new_scenario_name: str = ""
        # Directories for pddl problem/result files (format string, formatted by initialize)
        self.problems_dir: str = (PATH.CWD + "/data/scenarios/problems/{0}")
        self.results_dir: str = (PATH.CWD + "/data/scenarios/results/{0}")

    def initialize(
            self, scenario: str, new_scenario: str,
            shell: callable, network: str = "default"
            ) -> bool:
        """

        :param scenario: name of scenario to load (".sumocfg" file)
        :param new_scenario: name of scenario which will be created (after converting ".pddl"
        result files to scenario)
        :param shell: function able to pass commands into shell/cmd (expecting 'UserInterface.run_command')
        :param network: name of network, if default, will be extracted from ".sumocfg" file (scenario)
        :return: None
        """
        # Checks
        if not file_exists(PATH.SCENARIO_SIM_GENERATED.format(scenario)):
            return False
        elif not file_exists(PATH.SCENARIO_ROUTES.format(scenario)):
            return False
        elif file_exists(PATH.SCENARIO_SIM_PLANNED.format(new_scenario), message=False):
            print(
                f"Scenario made from '.pddl' result files "
                f"named: {new_scenario} already exists -> {PATH.SCENARIO_SIM_PLANNED.format(new_scenario)} !"
            )
            return False
        elif shell is None:
            print(f"Method 'shell' is None!")
            return False
        self.shell = shell
        # Load scenario
        self.simulation = ConfigGenerator(PATH.SCENARIO_SIM_GENERATED.format(scenario))
        # (graph is not needed for routes, since we are not generating vehicles here)
        self.routes = RoutesGenerator(routes_path=PATH.SCENARIO_ROUTES.format(scenario))
        self.new_scenario_name = new_scenario
        # Load graph
        if network == "default":
            network = get_file_name(self.simulation.get_network_name())
            print(f"Extracted network from scenario -> {network}")
        if not file_exists(PATH.NETWORK_SUMO_MAPS.format(network)):
            return False
        self.graph = Graph(Skeleton())
        self.graph.loader.load_map(network)
        self.graph.simplify.simplify_graph()
        self.graph.skeleton.validate_graph()
        self.problems_dir = self.problems_dir.format(self.new_scenario_name)
        self.results_dir = self.results_dir.format(self.new_scenario_name)
        return True

    def generate_problems(self, domain: str, *args, **kwargs) -> None:
        """
        Generates ".pddl" problem files corresponding to loaded scenario,
        their name must contain "new_scenario" attribute, extension must be ".pdd"

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Method 'generate_problems' must be implemented by children of PddlLauncher")

    def generate_results(self, planner: str, domain: str, timeout: int = 30, *args, **kwargs) -> None:
        """
        Generates ".pddl" results files to loaded scenario,
        their name must contain "new_scenario" attribute, extension must be ".pdd"


        :param planner: name of planner to be used (must be defined in /utc/src/util/constants -> PLANNERS)
        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param timeout: seconds given to planner execution
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Method 'generate_results' must be implemented by children of PddlLauncher")

    def generate_scenario(self, *args, **kwargs) -> None:
        """
        Generates new scenario from ".pddl" result files

        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Method 'generate_scenario' must be implemented by children of PddlLauncher")

    # ------------------------------------------------ Utils -----------------------------------------------

    def prepare_directory(self, pddl_type: str) -> bool:
        """
        Creates directory under the name of new_scenario_attribute in
        /utc/data/problems or /utc/data/results depending on
        argument pddl_type

        :param pddl_type: either problem/result
        :return: true on success, false otherwise
        """
        if pddl_type not in ["result", "problem"]:
            print(f"Invalid pddl_type: {pddl_type}, expected either 'problem' or 'result'")
            return False
        elif not self.is_initialized():
            print(f"Launcher class is not initialized!")
            return False
        dir_path: str = (self.problems_dir if pddl_type == "problem" else self.results_dir)
        if dir_exist(dir_path, message=False):
            return True
        print(f"Creating directory for pddl {pddl_type} files")
        mkdir(dir_path)
        if not dir_exist(dir_path):
            print(f"Error at creating directory: {dir_path}")
            return False
        print(f"Successfully created directory {dir_path}")
        return True

    def check_pddl_extension(self, path: str) -> None:
        """
        Checks if files in directory end with ".pddl" extension,
        if not, renames such files.

        :return: None
        """
        if not dir_exist(path, message=False):
            print(f"Invalid directory: {path} passed to method: 'check_pddl_extension'")
            return
        files: List[str] = listdir(path)
        for file in files:
            # Add absolute path
            file = path + "/" + file
            if file.endswith(".pddl"):
                continue
            # If ".pddl" extension is not last, remove it
            new_file = file.replace(".pddl", "")
            new_file += ".pddl"
            if file_exists(path + f"/{new_file}", message=False):
                print(f"Cannot change extension of: {file}, because {new_file} already exists!")
                return
            rename(file, new_file)
            print(f"Done renaming file: {file} -> {new_file}")

    def is_initialized(self) -> bool:
        """
        :return: True if Class was initialized with "initialize" method, false otherwise
        """
        if self.simulation is None:
            print("simulation is None")
            return False
        elif self.routes is None:
            print("routes is None")
            return False
        elif self.graph is None:
            print("graph is None")
            return False
        elif self.shell is None:
            print("shell is None")
            return False
        elif not self.new_scenario_name:
            print("new_scenario_name is None")
            return False
        return True
