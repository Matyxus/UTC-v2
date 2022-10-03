from utc.src.pddl.pddl_problem.pddl_problem import PddlProblem
from utc.src.pddl.pddl_problem.pddl_result import PddlResult
from utc.src.simulator.scenario import Scenario
from utc.src.file_system import MyFile, MyDirectory, FilePaths, FileExtension
from utc.src.ui import UserInterface, Command
from typing import List, Optional


class PddlLauncher(UserInterface):
    """ Class that implements interface methods for generating pddl problems/results """

    def __init__(self, log_commands: bool = True):
        super().__init__("PddlLauncher", log_commands)
        # -------------- Pddl --------------
        self.pddl_problem: Optional[PddlProblem] = None
        self.pddl_result: Optional[PddlResult] = None
        # Scenario
        self.scenario: Optional[Scenario] = None
        self.new_scenario_name: str = ""
        # Directories for pddl problem/result files (set by method 'initialize')
        self.problems_dir: str = ""
        self.results_dir: str = ""

    # ---------------------------------- Commands ----------------------------------

    def initialize_commands(self) -> None:
        super().initialize_commands()
        self.user_input.add_command([Command("initialize", self.initialize_command)])

    @UserInterface.log_command
    def initialize_command(self, scenario: str, new_scenario: str, network: str = "default") -> bool:
        """
        Initializes environment for generating pddl problem/result files and
        conversion of result files to scenarios, unlocks commands

        :param scenario: name of scenario to load (".sumocfg" file)
        :param new_scenario: namespace of newly generated pddl problem/result files
        and planned scenario, routes
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
        self.problems_dir = (FilePaths.PDDL_PROBLEMS + "/" + self.new_scenario_name)
        self.results_dir = (FilePaths.PDDL_RESULTS + "/" + self.new_scenario_name)
        # Unlock commands for generating pddl files and scenario
        if self.user_input is not None:
            self.user_input.add_command([
                Command("generate_problems", self.generate_problems_command),
                Command("generate_problem", self.generate_problem_command),
                Command("generate_results", self.generate_results_command),
                Command("generate_result", self.generate_result_command),
                Command("generate_scenario", self.generate_scenario_command),
                Command("plan_scenario", self.plan_scenario_command)
            ])
        return True

    # -------------------------------------------- Problem --------------------------------------------

    def generate_problems_command(self, domain: str, *args, **kwargs) -> None:
        """
        Generates ".pddl" problem files corresponding to loaded scenario,
        resulting files will be named: "new_scenario_problem[suffix].pddl",
        where suffix is added by Subclass

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Method 'generate_problems' must be implemented by children of PddlLauncher")

    def generate_problem_command(self, domain: str, *args, **kwargs) -> None:
        """
        Generates single ".pddl" problem file corresponding to loaded scenario,
        resulting file will be named: "new_scenario_problem[suffix].pddl",
        where suffix is added by Subclass

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Method 'generate_problem' must be implemented by children of PddlLauncher")

    # -------------------------------------------- Result --------------------------------------------

    def generate_results_command(
            self, planner: str, domain: str,
            timeout: int = 30, thread_count: int = 1,
            *args, **kwargs
            ) -> None:
        """
        Generates ".pddl" results files to loaded scenario,
        the generated result files will be named: "new_scenario_result[suffix].pddl,
        where suffix is added by Subclass

        :param planner: name of planner to be used (must be defined in /utc/src/util/constants -> PLANNERS)
        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param timeout: seconds given to planner execution
        :param thread_count: number of parallel planner calls (default one -> current process)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Method 'generate_results' must be implemented by children of PddlLauncher")

    def generate_result_command(
            self, problem: str, planner: str,
            domain: str, timeout: int = 30, *args, **kwargs
            ) -> bool:
        """
        Generates single ".pddl" result files from given problem file name,
        the generated result file will be named: "new_scenario_result[suffix].pddl,
        where suffix is added by Subclass

        :param problem: name of problem file (must be in /utc/data/scenarios/problems/new_scenario)
        :param planner: name of planner to be used (must be defined in /utc/src/util/constants -> PLANNERS)
        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param timeout: seconds given to planner execution
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: true on success, false otherwise
        """
        raise NotImplementedError("Method 'generate_result' must be implemented by children of PddlLauncher")

    # -------------------------------------------- Scenario --------------------------------------------

    def generate_scenario_command(self, keep_files: bool = True, *args, **kwargs) -> None:
        """
        Generates new scenario from ".pddl" result files

        :param keep_files: if pddl problem/result files should be kept (default True)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Method 'generate_scenario' must be implemented by children of PddlLauncher")

    def plan_scenario_command(self, domain: str, planner: str, timeout: int = 30, *args, **kwargs) -> None:
        """
        Plans scenario "on the go" during the simulation (displayed on SumoGUI), automatically
        generates statistics files

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param planner: name of planner to be used (must be defined in /utc/src/util/constants -> PLANNERS)
        :param timeout: seconds given to planner execution
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Method 'plan_scenario' must be implemented by children of PddlLauncher")

    # ------------------------------------------------ Utils -----------------------------------------------

    def prepare_directory(self, pddl_type: str) -> bool:
        """
        Creates directory under the name of 'new_scenario' in
        /utc/data/scenarios/problems or /utc/data/scenarios/results depending on
        argument pddl_type

        :param pddl_type: either problem or result
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
        if not, renames such files so that their extension
        ends with ".pddl"

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
