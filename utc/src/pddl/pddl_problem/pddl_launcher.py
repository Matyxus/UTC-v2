from utc.src.pddl.pddl_problem.pddl_problem import PddlProblem
from utc.src.pddl.pddl_problem.pddl_result import PddlResult
from utc.src.simulator.scenario import Scenario
from utc.src.file_system import MyFile, MyDirectory, FilePaths, FileExtension
from typing import List, Optional


class PddlLauncher:
    """ Class that implements interface methods for generating pddl problems/results """

    def __init__(self):
        # -------------- Pddl --------------
        self.pddl_problem: Optional[PddlProblem] = None
        self.pddl_result: Optional[PddlResult] = None
        # Scenario
        self.scenario: Optional[Scenario] = None
        self.new_scenario_name: str = ""
        # Directories for pddl problem/result files (format string, formatted by initialize)
        self.problems_dir: str = (FilePaths.PDDL_PROBLEMS + "/{0}")
        self.results_dir: str = (FilePaths.PDDL_RESULTS + "/{0}")

    def initialize(self, scenario: str, new_scenario: str, network: str = "default") -> bool:
        """

        :param scenario: name of scenario to load (".sumocfg" file)
        :param new_scenario: name of scenario which will be created (after converting ".pddl"
        result files to scenario)
        :param network: name of network, if default, will be extracted from ".sumocfg" file (scenario)
        :return: None
        """
        # Checks
        if not MyFile.file_exists(FilePaths.SCENARIO_SIM_GENERATED.format(scenario)):  # Scenario must be user generated
            return False
        elif MyFile.file_exists(FilePaths.SCENARIO_SIM_PLANNED.format(new_scenario), message=False):
            print(
                f"Scenario made from '.pddl' result files named: {new_scenario}"
                f" already exists -> {FilePaths.SCENARIO_SIM_PLANNED.format(new_scenario)} !"
            )
            return False
        try:
            self.scenario = Scenario(scenario, network=network)
        except (FileNotFoundError, ValueError) as _:  # Error occurred during loading of scenario
            return False
        self.new_scenario_name = new_scenario
        self.problems_dir = self.problems_dir.format(self.new_scenario_name)
        self.results_dir = self.results_dir.format(self.new_scenario_name)
        return True

    def generate_problems(self, domain: str, *args, **kwargs) -> None:
        """
        Generates ".pddl" problem files corresponding to loaded scenario,
        their name must contain "new_scenario" attribute, extension must be ".pddl"

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
        if MyDirectory.dir_exist(dir_path, message=False):
            return True
        print(f"Creating directory for pddl {pddl_type} files")
        if not MyDirectory.make_directory(dir_path):
            print(f"Error at creating directory: {dir_path}")
            return False
        print(f"Successfully created directory {dir_path}")
        return True

    def check_pddl_extension(self, dir_path: str) -> None:
        """
        Checks if files in directory end with ".pddl" extension,
        if not, renames such files.

        :param dir_path: path to directory
        :return: None
        """
        files: Optional[List[str]] = MyDirectory.list_directory(dir_path)
        if files is None:
            print(f"Invalid directory: {dir_path} passed to method: 'check_pddl_extension'")
            return
        for file in files:
            if file.endswith(".pddl"):
                continue
            # Add absolute path
            file = dir_path + "/" + file
            # If ".pddl" extension is not last, remove it
            new_file = file.replace(FileExtension.PDDL, "") + FileExtension.PDDL
            if not MyFile.rename_file(file, new_file):
                continue

    def is_initialized(self) -> bool:
        """
        :return: True if Class was initialized with "initialize" method, false otherwise
        """
        if self.scenario is None:
            return False
        elif not self.new_scenario_name:
            return False
        return True
