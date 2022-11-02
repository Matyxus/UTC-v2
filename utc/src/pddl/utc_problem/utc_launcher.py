from utc.src.pddl.pddl_problem import PddlLauncher
from utc.src.pddl.utc_problem.utc_problem import UtcProblem
from utc.src.pddl.utc_problem.utc_result import UtcResult
from utc.src.file_system import (
     MyDirectory, DefaultDir,
     MyFile, FilePaths, PLANNERS, FileExtension
)
from utc.src.utils import check_process_count
from multiprocessing import Pool
from typing import List, Optional, Set


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
        # Checks
        if not self.check_args("problem", domain):
            return
        elif window < 0:
            print(f"Parameter window: '{window}' must be higher than 0!")
            return
        # Initialize PddlProblem
        self.pddl_problem = UtcProblem()
        self.pddl_problem.pddl_network.process_graph(self.graph.skeleton)
        self.pddl_problem.set_domain(domain)
        # Start generating problem files
        last_vehicle_depart: float = self.scenario.routes_file.get_end_time()
        interval: int = max(int(round(last_vehicle_depart / window)), 1)
        problem_files: Set[str] = set(self.scenario.problems_dir.get_files())
        print(f"Generating {interval - len(problem_files)} problem files for scenario: {self.scenario.name}")
        if len(problem_files) != 0:
            if len(problem_files) >= interval:
                print(f"Pddl problem directory already has: '{interval}/{interval}' problem files!")
                return
            print(f"Pddl problem directory already has: '{len(problem_files)}/{interval}' files, missing files..")
        start_time: int = 0
        end_time: int = window
        for i in range(interval):
            problem_name: str = f"{self.scenario.name}_problem_{start_time}_{end_time}"
            # Already exists
            if problem_name in problem_files:
                continue
            self.pddl_problem.set_problem_name(problem_name)
            self.pddl_problem.pddl_vehicle.add_vehicles(self.scenario.routes_file.get_vehicles(start_time, end_time))
            # Error at saving file
            if not self.pddl_problem.save(self.scenario.problems_dir.get_file_path(self.pddl_problem.problem_name)):
                print(
                    f"Error at generating: '{i+1}/{interval}' "
                    f"problem file: {problem_name}, exiting .."
                )
                return
            # Reset cars
            self.pddl_problem.pddl_vehicle.clear()
            print(f"Finished generating '{i+1}/{interval}' problem file")
            start_time = end_time
            end_time += window
        # Discard class
        self.pddl_problem = None
        print("Finished generating problem files")

    @PddlLauncher.log_command
    def generate_results_command(
            self, planner: str, domain: str,
            timeout: int = 30, processes: int = 1,
            *args, **kwargs
            ) -> bool:
        # Checks
        if not self.check_args("result", domain):
            return False
        elif not PLANNERS.get_planner(planner):
            return False
        elif not self.scenario_dir.planner_out_dir.initialize_dir():
            return False
        elif not check_process_count(processes):
            processes = 1
        problem_files: Optional[List[str]] = self.scenario.problems_dir.get_files()
        if problem_files is None or not problem_files:  # Checks against None and empty list
            print(f"Pddl problem files must be generated before calling 'generate_results'!")
            return False
        result_files: Set[str] = set(self.scenario.results_dir.get_files())
        # Count of already generated result files (dir exists, since we used prepare_directory method)
        result_count: int = len(result_files)
        if result_count != 0:
            if result_count >= len(problem_files):
                print(f"Result directory has more or equal to number of files in problem directory, exiting ..")
                return False
        print(f"Generating '{len(problem_files) - result_count}' pddl result files")
        print(f"ETA: {round((len(problem_files) * timeout) / (60 * processes), 1)} minutes")
        if processes > 1:
            # Create pool
            print(f"Starting process pool with: {processes} processes")
            pool: Pool = Pool(processes)
            for index, pddl_problem in enumerate(problem_files):
                if pddl_problem.replace("problem", "result") in result_files:
                    continue
                pool.apply_async(
                    self.generate_result_command, args=(
                        pddl_problem, planner,
                        domain, self.scenario_dir.planner_out_dir.create_sub_dir(f"out_{index}"),
                        timeout
                    )
                )
            pool.close()
            pool.join()
            # Remove planner output directories generated by threads
            for i in range(len(problem_files)):
                sub_dir: DefaultDir = self.scenario_dir.planner_out_dir.get_sub_dir(f"out_{i}")
                if sub_dir is not None:
                    MyDirectory.delete_directory(sub_dir.path)
        else:  # Single thread
            for index, pddl_problem in enumerate(problem_files):
                if pddl_problem.replace("problem", "result") in result_files:
                    continue
                self.generate_result_command(
                    pddl_problem, planner,
                    domain, self.scenario_dir.planner_out_dir, timeout
                )
        # Check result directory, Merwin planner adds its own extension at the end of file
        self.check_pddl_extension(self.scenario.results_dir.path)
        # Remove planner outputs
        MyDirectory.delete_directory(self.scenario_dir.planner_out_dir.path)
        print("Finished generating result files")
        return True

    def generate_result_command(
            self, problem: str, planner: str,
            domain: str, out_dir: DefaultDir,
            timeout: int = 30, *args, **kwargs
         ) -> bool:
        # ------------------- Init -------------------
        if out_dir is None:
            print(f"Invalid output directory, got type: 'None'")
            return False
        result_name: str = problem.replace("problem", "result")
        print(f"Generating '{FileExtension.PDDL}' result: '{result_name}' from: '{problem}'")
        planner_call: str = PLANNERS.get_planner(planner).format(
            FilePaths.PDDL_DOMAIN.format(domain),
            FilePaths.PDDL_PROBLEM.format(self.scenario.scenario_folder, self.scenario.name, problem),
            FilePaths.PDDL_RESULT.format(self.scenario.scenario_folder, self.scenario.name, result_name)
        )
        # ------------------- Generate -------------------
        success, output = self.call_shell(planner_call, timeout, message=False, working_dir=out_dir.path)
        # If file was not generated, return (possibly low timeout)
        if not success:
            print(f"Error at generating result file: '{result_name}', try to increase timeout: '{timeout}'")
            return False
        # elif not (MyFile.file_exists(planner_call[3], message=False) or
        #          MyFile.file_exists(planner_call[3] + ".1", message=False)):
        #    print(f"Unable to generate result file: '{result_name}', not enough time, increase timeout: '{timeout}'")
        #    return False
        print(f"Finished generating result file: '{result_name}'")
        return True

    @PddlLauncher.log_command
    def generate_scenario_command(self, generate_best: bool = True, keep_files: bool = True, *args, **kwargs) -> bool:
        # Checks
        if not self.is_initialized():
            print("UtcLauncher must be initialized with method: 'initialize' !")
            return False
        pddl_result = UtcResult(self.scenario, self.graph.skeleton)
        success: bool = pddl_result.results_to_scenario(generate_best=generate_best)
        if self.logging_enabled:
            self.save_log(FilePaths.SCENARIO_INFO.format(self.scenario.scenario_folder, self.scenario.name))
            self.clear_log()
        if not success:
            return False
        if self.user_input is not None:
            # Reset commands
            self.user_input.remove_command(
                list(self.user_input.commands.keys() ^ {"help", "exit", "initialize_pddl"})
            )
        if not keep_files:
            print(f"Deleting pddl problem and result files")
            MyDirectory.delete_directory(self.scenario.problems_dir.path)
            MyDirectory.delete_directory(self.scenario.results_dir.path)
        # Reset
        self.scenario = None
        self.scenario_dir = None
        self.graph = None
        return True

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
        pass
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
        """
    # --------------------------------------------- Utils ---------------------------------------------

    def check_args(self, pddl_type: str, domain: str) -> bool:
        """
        :param pddl_type: either problem or result
        :param domain: name of domain file
        :return: true if correct directory was initialized, domain exists, false otherwise
        """
        if not self.is_initialized():
            print(f"UtcLauncher must first be initialized by method 'initialize_command' !")
            return False
        elif not MyFile.file_exists(FilePaths.PDDL_DOMAIN.format(domain)):
            return False
        elif pddl_type not in {"problem", "result"}:
            print(f"Invalid pddl_type: {pddl_type}, expected one of: [problem, result]")
            return False
        parent_dir: DefaultDir = (
            self.scenario_dir.problems_dir if
            pddl_type == "problem" else
            self.scenario_dir.results_dir
        )
        # Initialize /scenario/problems or /scenario/results + sub-directories named after scenario's name
        if not parent_dir.initialize_dir() or parent_dir.create_sub_dir(self.scenario.name) is None:
            print(
                f"Error at initializing "
                f"pddl '{pddl_type}' directory: '{self.scenario.scenario_folder}' "
                f"for scenario: '{self.scenario.name}' !"
            )
            return False
        return True


if __name__ == "__main__":
    utc_launcher: UtcLauncher = UtcLauncher()
    utc_launcher.run()

