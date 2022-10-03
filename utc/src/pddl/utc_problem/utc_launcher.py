from utc.src.pddl.pddl_problem import PddlLauncher
from utc.src.pddl.utc_problem.utc_problem import UtcProblem
from utc.src.pddl.utc_problem.utc_result import UtcResult
from utc.src.file_system import MyFile, MyDirectory, FilePaths, PLANNERS, FileExtension, SumoConfigFile
from utc.src.utils import TraciOptions
import traci
import multiprocessing
from datetime import datetime
from typing import List, Optional, Dict, Set


class UtcLauncher(PddlLauncher):
    """ Class that implements interface methods for generating pddl problems/results """

    def __init__(self, log_commands: bool = True):
        super().__init__(log_commands)

    # ----------------------------------------- Commands -----------------------------------------

    @PddlLauncher.log_command
    def generate_problems_command(self, domain: str, window: int = 20, *args, **kwargs) -> None:
        """
        Generates all ".pddl" problem files corresponding to loaded scenario

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param window: planning window time (seconds) corresponding to each pddl problem time frame in simulation
        (fist problem is generated from time: 0-window, second from time: window-window*2, ...)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        if not self.initialize_problem():
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
            if not self.pddl_problem.save(
                    FilePaths.SCENARIO_PROBLEMS.format(self.new_scenario_name, self.pddl_problem.problem_name)
                    ):
                print(f"Error at generating: {i+1} problem file: {self.pddl_problem.problem_name}, exiting ..")
                return
            # Reset cars
            self.pddl_problem.pddl_vehicle.clear()
            print(f"Finished generating '{i+1}' problem file: '{self.pddl_problem.problem_name}'")
            start_time = end_time
            end_time += window
        print("Finished generating problem files")

    def generate_problem_command(self, domain: str, start: int = 0, window: int = 20, *args, **kwargs) -> None:
        """
        Generates single ".pddl" problem corresponding to loaded scenario

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param start: initial time of problem (must be smaller than last departing vehicle)
        :param window: planning window time (seconds) corresponding to each pddl problem time frame in simulation
        (fist problem is generated from time: 0-window, second from time: window-window*2, ...)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        if not self.initialize_problem():
            return
        last_vehicle_depart: float = self.scenario.routes_generator.get_end_time()
        problem_name: str = f"{self.new_scenario_name}_problem{start}_{start+window}"
        # Checks
        if start > last_vehicle_depart:
            print(f"Starting time: '{start}' cannot be higher than last vehicle depart time: '{last_vehicle_depart}'")
            return
        # File already exists
        elif MyFile.file_exists(FilePaths.SCENARIO_PROBLEMS.format(self.new_scenario_name, problem_name)):
            return
        # Initialize PddlProblem
        elif self.pddl_problem is None:
            self.pddl_problem = UtcProblem()
            self.pddl_problem.pddl_network.process_graph(self.scenario.graph.skeleton)
        # Generate
        print(f"Generating problem file")
        self.pddl_problem.set_problem_name(problem_name)
        self.pddl_problem.pddl_vehicle.add_vehicles(
            self.scenario.routes_generator.get_vehicles(start, start+window)
        )
        if not self.pddl_problem.save(
            FilePaths.SCENARIO_PROBLEMS.format(self.new_scenario_name, self.pddl_problem.problem_name)
                ):
            return
        # Reset cars
        self.pddl_problem.pddl_vehicle.clear()
        print(f"Finished generating problem file: {self.pddl_problem.problem_name}")

    @PddlLauncher.log_command
    def generate_results_command(
            self, planner: str, domain: str,
            timeout: int = 30, thread_count: int = 1,
            *args, **kwargs
            ) -> None:
        # Checks
        if not self.initialize_result(domain, planner):
            return
        elif thread_count < 1:
            print(f"Invalid thread count: '{thread_count}', must be at least 1, defaulting to 1")
            thread_count = 1
        elif thread_count > multiprocessing.cpu_count():
            print(
                f"Invalid thread count: '{thread_count}', "
                f"must be lower than: {multiprocessing.cpu_count()}, defaulting to 1"
            )
            thread_count = 1
        problem_files: Optional[List[str]] = MyDirectory.list_directory(self.problems_dir)
        if not problem_files:  # Checks against None and empty list
            print(f"Pddl problem files must be generated before calling 'generate_results'!")
            return
        # Count of already generated result files (dir exists, since we used prepare_directory method)
        result_count: int = len(MyDirectory.list_directory(self.results_dir))
        if result_count != 0:
            print(f"Pddl result files already exist in: {self.results_dir}")
            return
        print(f"Generating '{len(problem_files)}' pddl result files from: '{problem_files}'")
        print(
            f"Number of allowed threads: '{thread_count}', "
            f"estimated time taken: {(len(problem_files) * timeout) // (60 * thread_count)} minutes."
        )
        if thread_count > 1:
            # Create pool
            print(f"Starting pool !!!")
            pool: multiprocessing.Pool = multiprocessing.Pool(thread_count)
            for pddl_problem in problem_files:
                pool.apply_async(self.generate_result_command, args=(pddl_problem, planner, domain, timeout, False))
            pool.close()
            pool.join()
        else:
            for index, pddl_problem in enumerate(problem_files):
                self.generate_result_command(pddl_problem, planner, domain, timeout, check=False)
                print(f"Finished generating '{index + 1}' result file")
        # Check result directory, Cerberus planner adds its own extension at the end of file
        self.check_pddl_extension(self.results_dir)
        print("Finished generating result files")

    def generate_result_command(
            self, problem: str, planner: str,
            domain: str, timeout: int = 30,
            check: bool = True,
            *args, **kwargs
         ) -> bool:
        # ------------------- Checks -------------------
        problem = MyFile.get_file_name(problem)
        if check:
            if not self.initialize_result(domain, planner):
                return False
            elif not MyFile.file_exists(self.problems_dir + f"/{problem}{FileExtension.PDDL}"):
                return False
            elif "problem" not in problem:
                print(f"Invalid problem name: '{problem}', does not contain 'problem' in name!")
                return False
            elif not problem.startswith(self.new_scenario_name):
                print(
                    f"Invalid problem name: '{problem}', does start with "
                    f"scenario name: '{self.new_scenario_name}' in name!"
                )
                return False
        # ------------------- Init -------------------
        result_name: str = problem.replace("problem", "result")
        # TODO Check if file already  exists
        # (ignore extension, cannot be None, since there is check in "initialize_result")
        print(f"Generating '{FileExtension.PDDL}' result: '{result_name}' from: '{problem}'")
        planner_call: str = PLANNERS.get_planner(planner).format(
            FilePaths.PDDL_DOMAINS.format(domain),
            FilePaths.SCENARIO_PROBLEMS.format(self.new_scenario_name, problem),
            FilePaths.SCENARIO_RESULTS.format(self.new_scenario_name, result_name)
        )
        # ------------------- Generate -------------------
        if self.logging_enabled:
            self.add_comment(f"Planning {result_name} at {datetime.now()}")
        success, output = self.call_shell(planner_call, timeout, message=False)
        # If file was not generated, return (possibly low timeout)
        if not success:
            print(f"Error at generating result file: '{result_name}', try to increase timeout: '{timeout}'")
            return False
        print(f"Finished generating result file: {result_name}")
        # TODO Check result directory, Merwin planner adds its own extension at the end of file
        return True

    @PddlLauncher.log_command
    def generate_scenario_command(self, keep_files: bool = True, *args, **kwargs) -> None:
        # Checks
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return
        self.pddl_result = UtcResult(self.scenario, self.new_scenario_name)
        success: bool = self.pddl_result.results_to_scenario()
        if self.logging_enabled:
            self.save_log(FilePaths.SCENARIO_SIM_INFO.format(self.new_scenario_name))
            self.clear_log()
        # Delete files
        if success and self.user_input is not None:
            # Reset commands
            self.user_input.remove_command(
                list(self.user_input.commands.keys() ^ {"help", "exit", "initialize_pddl"})
            )
            if not keep_files:
                print(f"Deleting pddl problem and result files")
                MyDirectory.delete_directory(FilePaths.PDDL_PROBLEMS + f"/{self.new_scenario_name}")
                MyDirectory.delete_directory(FilePaths.PDDL_RESULTS + f"/{self.new_scenario_name}")

    def plan_scenario_command(
            self, domain: str, planner: str,
            timeout: int = 30, window: int = 20,
            *args, **kwargs
            ) -> None:
        """
        Plans scenario "on the go" during the simulation (displayed on SumoGUI), automatically
        generates statistics files

        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param planner: name of planner to be used (must be defined in /utc/src/util/constants -> PLANNERS)
        :param timeout: seconds given to planner execution
        :param window: planning window time (seconds) corresponding to each pddl problem time frame in simulation
        (fist problem is generated from time: 0-window, second from time: window-window*2, ...)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        # Checks
        if not self.initialize_problem() or not self.initialize_result(domain, planner):
            return
        traci_options: TraciOptions = TraciOptions()
        self.pddl_result = UtcResult(self.scenario, self.new_scenario_name)
        try:
            traci.start(
                [traci_options.get_display(True), *traci_options.get_all(SumoConfigFile(self.scenario.name).file_path)]
            )
            step: int = window  # Start step at time equal to window
            generated: int = 0  # How many pddl problem files were already generated
            vehicles: Dict[str, str] = {}  # Vehicles and their paths
            result_files: Set[str] = set()  # Empty at start
            while traci.simulation.getMinExpectedNumber() > 0:  # -> "while running.."
                if step == window:
                    # Generate pddl files
                    self.generate_problem_command(domain, start=generated*window, window=window)
                    # Pddl problem file was not generated
                    if not MyFile.file_exists(
                            FilePaths.SCENARIO_PROBLEMS.format(self.new_scenario_name, self.pddl_problem.problem_name)
                            ):
                        break
                    self.generate_result_command(self.pddl_problem.problem_name, planner, domain, timeout)
                    # Extract new files (no need to check against non-existing directory)
                    result_files ^= set(MyDirectory.list_directory(self.results_dir))
                    if not len(result_files):
                        print(
                            f"Unable to generate result file from: '{self.pddl_problem.problem_name}',"
                            f" try increasing timeout"
                        )
                        break
                    result_name: str = list(result_files)[-1]
                    # Get vehicle paths from generated pddl result file
                    vehicles |= self.pddl_result.parse_result(result_name.replace(FileExtension.PDDL, ""))
                    generated += 1
                    step = 0
                # Assign new planned routes to vehicle
                for vehicle_id in traci.simulation.getLoadedIDList():  # Id list is empty most of the time
                    if vehicle_id in vehicles:
                        print(f"Changing route of vehicle: '{vehicle_id}'")
                        traci.vehicle.setRoute(vehicle_id, vehicles.pop(vehicle_id).split())
                # Simulation step
                traci.simulationStep()
                step += 1
            traci.close()
            print(f"Simulation of scenario: '{self.scenario.name}' ended, exiting ...")
        except traci.exceptions.FatalTraCIError as e:
            # Closed by user
            if str(e) == "connection closed by SUMO":
                print("Closed GUI, exiting ....")
            else:
                print(f"Error occurred: {e}")

    # ----------------------------------------- Utils -----------------------------------------

    def initialize_problem(self) -> bool:
        """
        :return: True if ".pddl" problem file/s can be generated, false otherwise
        """
        # Checks
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return False
        elif MyDirectory.list_directory(self.problems_dir):  # Checks against None and empty list
            print(f"Pddl problem files already exist in: {self.problems_dir}")
            return False
        elif not self.prepare_directory("problem"):
            return False
        return True

    def initialize_result(self, domain: str, planner: str) -> bool:
        """
        :param domain: name of pddl domain (must be in /utc/data/domains)
        :param planner: name of planner to be used (must be defined in /utc/src/util/constants -> PLANNERS)
        :return: True if ".pddl" result file/s can be generated, false otherwise
        """
        # Checks
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return False
        elif not MyFile.file_exists(FilePaths.PDDL_DOMAINS.format(domain)):
            return False
        elif not PLANNERS.get_planner(planner):
            return False
        elif not self.prepare_directory("result"):
            return False
        return True


if __name__ == "__main__":
    utc_launcher: UtcLauncher = UtcLauncher()
    utc_launcher.run()

