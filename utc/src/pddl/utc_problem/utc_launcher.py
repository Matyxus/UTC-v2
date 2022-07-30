from utc.src.pddl.pddl_problem import PddlLauncher
from utc.src.pddl.utc_problem.utc_problem import UtcProblem
from utc.src.pddl.utc_problem.utc_result import UtcResult
from utc.src.file_system import MyFile, MyDirectory, FilePaths, PLANNERS, FileExtension
from typing import List, Optional


class UtcLauncher(PddlLauncher):
    """ Class that implements interface methods for generating pddl problems/results """

    def __init__(self):
        super().__init__()

    def generate_problems(self, domain: str, window: int = 20, *args, **kwargs) -> None:
        """
        Generates ".pddl" problem files corresponding to loaded scenario

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param window: planning window time (seconds) corresponding to each pddl problem time
        frame in simulation (fist problem is generated from time: 0-window, second from time: window-window*2, ...)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return
        elif MyDirectory.list_directory(self.problems_dir):  # Checks against None and empty list
            print(f"Pddl problem files already exist in: {self.problems_dir}")
            return
        elif not self.prepare_directory("problem"):
            return
        # Initialize PddlProblem
        self.pddl_problem = UtcProblem()
        self.pddl_problem.pddl_network.process_graph(self.scenario.graph.skeleton)
        # Start generating problem files
        last_vehicle_depart: float = self.scenario.routes_generator.get_end_time()
        interval: int = max(int(round(last_vehicle_depart / window)), 1)
        print(f"Generating {interval} problem files")
        start_time: int = 0
        end_time: int = window
        for i in range(interval):
            self.pddl_problem.set_problem_name(f"{self.new_scenario_name}_problem{start_time}_{end_time}")
            self.pddl_problem.pddl_vehicle.add_vehicles(
                self.scenario.routes_generator.get_vehicles(start_time, end_time)
            )
            self.pddl_problem.save(
                FilePaths.SCENARIO_PROBLEMS.format(self.new_scenario_name, self.pddl_problem.problem_name)
            )
            if not MyFile.file_exists(
                    FilePaths.SCENARIO_PROBLEMS.format(self.new_scenario_name, self.pddl_problem.problem_name)
                    ):
                print(f"Error at generating: {i+1} problem file: {self.pddl_problem.problem_name}, exiting ..")
                return
            # Reset cars
            self.pddl_problem.pddl_vehicle.clear()
            print(f"Finished generating {i+1} problem file: {self.pddl_problem.problem_name}")
            start_time = end_time
            end_time += window
        print("Finished generating problem files")

    def generate_results(self, planner: str, domain: str, timeout: int = 30, *args, **kwargs) -> None:
        # Checks
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return
        elif not MyFile.file_exists(FilePaths.PDDL_DOMAINS.format(domain)):
            return
        elif not PLANNERS.get_planner(planner):
            return
        elif not self.prepare_directory("result"):
            return
        problem_files: Optional[List[str]] = MyDirectory.list_directory(self.problems_dir)
        if not problem_files:  # Checks against None and empty list
            print(f"Pddl problem files must be generated before calling 'generate_results'!")
            return
        # Count of already generated result files (dir exists, since we used prepare_directory method)
        result_count: int = len(MyDirectory.list_directory(self.results_dir))
        if result_count != 0:
            print(f"Pddl result files already exist in: {self.results_dir}")
            return
        print(f"Generating {len(problem_files)} pddl result files from: {problem_files}")
        for index, pddl_problem in enumerate(problem_files):
            assert (
                    pddl_problem.endswith(FileExtension.PDDL) and
                    "problem" in pddl_problem and pddl_problem.startswith(self.new_scenario_name)
            )
            pddl_problem = MyFile.get_file_name(pddl_problem)
            result_name: str = pddl_problem.replace("problem", "result")
            print(f"Generating: {result_name}")
            planner_call: str = PLANNERS.get_planner(planner).format(
                FilePaths.PDDL_DOMAINS.format(domain),
                FilePaths.SCENARIO_PROBLEMS.format(self.new_scenario_name, pddl_problem),
                FilePaths.SCENARIO_RESULTS.format(self.new_scenario_name, result_name)
            )
            success, output = self.shell(planner_call, timeout)
            # If file was not generated, return (possibly low timeout)
            current_count: int = len(MyDirectory.list_directory(self.results_dir))
            if not success or not (current_count > result_count):
                print(f"Error at generating result file: {result_name}, try to increase timeout: {timeout}")
                return
            result_count = current_count
            print(f"Finished generating {index+1} result file: {result_name}")
        # Check result directory, Cerberus planner adds its own extension at the end of file
        self.check_pddl_extension(self.results_dir)
        print("Finished generating result files")

    def generate_scenario(self, *args, **kwargs) -> None:
        # Checks
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return
        self.pddl_result = UtcResult(self.scenario, self.new_scenario_name)
        self.pddl_result.results_to_scenario()
