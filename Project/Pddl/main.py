from typing import List
from Project.Utils import UserInterface
from Project.Simplify.Graph_modules import Display, ShortestPath, Simplify, Loader
from Project.Simplify.Components import Skeleton
from Project.constants import file_exists, dir_exist, Path
from Project.Pddl.Domain import UtcProblem
import subprocess


class Launcher(UserInterface):
    """ Class that launches program for UTC problem.pddl generation, ask user for input """

    def __init__(self):
        super().__init__()
        # -------------- Graph --------------
        self.graph: Skeleton = None
        # Graph modules
        self.display: Display = Display()
        self.shortest_path: ShortestPath = ShortestPath()
        self.simplify: Simplify = Simplify()
        self.loader: Loader = Loader()
        # -------------- Domain --------------
        self.generator: UtcProblem = UtcProblem()
        # -------------- Commands --------------
        self.functions["generate-baseline"] = [self.baseline_command, 1, 1]
        self.functions["generate-problem"] = [self.problem_command, 3, 3]
        self.functions["add-cars"] = [self.cars_command, 3, 3]
        self.functions["generate-result"] = [self.result_command, 4, 4]
        self.functions["plot"] = [self.plot_command, 0, 0]
        self.functions["save"] = [self.save_command, 0, 0]
        # -------------- Utils --------------
        self.generating_problem: bool = False
        self.TIME_OUT: int = 30  # Seconds

    def dynamic_input(self) -> None:
        print("Starting program, for help type 'help', expecting white space between command arguments.")
        while self.running:
            # ------------ Input ------------
            text: str = input("Type command: ")
            user_input: List[str] = text.split()
            if not len(user_input):
                print(f"{text} is invalid input!")
                continue
            print(f"Interpreting: {user_input}")
            command_name: str = self.get_function_name(user_input.pop(0))
            if not self.check_function_args(command_name, user_input):
                continue
            # Execute function
            print(f"Function args: {user_input}")
            command: List[callable, int, int] = self.functions[command_name]
            command[0](user_input)
        print("Exiting...")

    # ---------------------------------- Commands ----------------------------------

    def problem_command(self, args: List[str]) -> None:
        # Check for planner existence
        if not file_exists(Path.PDDL_DOMAINS + args[0] + ".pddl"):
            print(f"Domain file: {args[0]}.pddl does not exist, check folder: {Path.PDDL_DOMAINS} for domains")
            return
        # Check for network existence
        elif not file_exists(Path.NETWORK_SUMO_MAPS + args[2] + ".net.xml"):
            return
        # Create Graph, load it, simplify
        self.graph = Skeleton()
        self.display.set_skeleton(self.graph)
        self.shortest_path.set_skeleton(self.graph)
        self.simplify.set_skeleton(self.graph)
        self.loader.set_skeleton(self.graph)
        self.loader.load_map(args[2])
        self.simplify.simplify_junctions(False)
        self.graph.validate_graph()  # Get rid of unused objects
        # Add graph to pddl problem
        self.generator.add_network(self.graph)
        self.generator.set_problem_name(args[1])  # Set problem name
        self.generator.set_domain(args[0])  # Set domain name
        # Generating problem
        self.generating_problem = True

    def save_command(self, args: List[str]) -> None:
        if not self.check_generation("save"):
            return
        self.generator.save()

    def cars_command(self, args: List[str]) -> None:
        if not self.check_generation("add-cars"):
            return
        elif not args[0].isdigit():
            print(f"Argument 'amount' has to be whole positive number, received: {args[0]}")
            return
        elif not (int(args[0]) > 0):
            print(f"Argument 'amount' has to be greater than 0, received: {args[0]} < 0")
            return
        elif self.shortest_path.a_star(args[1], args[2])[1] is None:
            print(f"Shortest path between {args[1]} and {args[2]} does not exist!")
            return
        if isinstance(self.generator, UtcProblem):
            self.generator.add_car(int(args[0]), args[1], args[2])
        else:
            print(f"Select 'utc' domain for adding cars!")

    def baseline_command(self, args: List[str]) -> None:
        if not file_exists(args[0]):
            return
        # Parse file until (:goal ..) to get initial and goal position of vehicles

    def result_command(self, args: List[str]) -> None:
        if not dir_exist(Path.PDDL_PLANERS + args[0]):
            print(f"Planner: {args[0]} does not exist, check folder: {Path.PDDL_PLANERS} for planners")
            return
        elif not file_exists(Path.PDDL_DOMAINS + args[1] + ".pddl"):
            print(f"Domain: {args[1]}.pddl does not exist, check folder: {Path.PDDL_DOMAINS} for domains")
            return
        elif not file_exists(Path.PDDL_GENERATED_PROBLEMS + args[2] + ".pddl"):
            print(f"Problem: {args[2]}.pddl does not exist, check folder: {Path.PDDL_GENERATED_PROBLEMS} for pddl problems")
            return
        elif args[0] not in Path.PLANNERS:
            print(f"Planner: {args[0]} is not defined in /Project/constants.py!")
            return
        # Call planner
        planner_args: List[str] = [
            Path.PDDL_DOMAINS + args[1] + ".pddl",  # Domain
            Path.PDDL_GENERATED_PROBLEMS + args[2] + ".pddl",  # Problem
            Path.PDDL_SOLVED_PROBLEMS + args[3] + ".txt"  # Result
        ]
        print(f"Calling command: {Path.PLANNERS[args[0]].format(*planner_args)}")
        print(f"With {self.TIME_OUT} second timeout")
        success, output = self.run_commmand(Path.PLANNERS[args[0]].format(*planner_args), self.TIME_OUT)
        if success:
            print("Successfully created result file, printing planner output:")
            print(output)

    def plot_command(self, args: List[str]) -> None:
        if not self.check_generation("plot") or self.graph is None:
            return
        self.display.plot()

    def help_command(self, args: List[str]) -> None:
        help_string: str = ("""
        1) generate-problem domain_name, problem_name, network_name
            1.1) domain_name  -> name of pddl domain, has to be in /Domain/domains/domain_name.pddl
            1.2) problem_name -> name of problem (under which it will be saved)
            1.3) network_name -> name of road network file (must be in /Project/Maps/sumo/network_name.net.xml)
        
        2*) save -> saves problem file into /Problems/generated/problem_name.pddl (does not discard of current problem)
        
        3*) add-cars amount, from_junction_id, to_junction_id
            3.1) amount -> name of graph from which sub_graph will be made
            3.2) from_junction_id -> name of created sub_graph, can be used to call Plot afterwards
            3.3) to_junction_id -> starting point of sub-graph
        
        4*) plot -> plots the network file 
        
        5) generate-baseline problem_name -> generates shortest path for cars (only for utc domain)
            3.1) problem_name -> name of problem in (/Problems/generated/problem_name.pddl)

        6) generate-result planner_name, domain_name, problem_name, result_name -> calls planner to generate solution
            6.1) planner_name -> name of planner (/Planers/planner_name)
            6.2) domain_name  -> name of domain (/Domain/Domains/domain_name.pddl)
            6.2) problem_name -> name of problem file (will be save in /Problems/generated/problem_name.pddl)
            6.3) result_name  -> name of solution file (will be save in /Problems/solved/result_name.pddl)
            6.4) string version of command can be found in /Project/constants
            
        7) ------ Utils ------
            7.1) exit -> quits the program
            7.2) help -> prints what commands do, their arguments etc.

        !) Do not use file extension/path when typing name of file, all paths can be found in /Project/constants.py! 
        *) Commands with Astrix (*) next to number only work, while generating problem!
        """)
        print(help_string)

    #  ----------------------------------  Utils  ----------------------------------

    def check_generation(self, command_name: str) -> bool:
        if not self.generating_problem:
            print(f"Command: '{command_name}' can only be used while generating problem!")
            return False
        return True

    def run_commmand(self, command: str, timeout: int, encoding="utf-8"):
        """
        https://stackoverflow.com/questions/41094707/setting-timeout-when-using-os-system-function

        :param command: console/terminal command string
        :param timeout: wait max timeout (seconds) for run console command
        :param encoding: console output encoding, default is utf-8
        :return: True/False on success/failure, console output
        """
        success: bool = False
        console_output: str = ""
        try:
            console_output_byte = subprocess.check_output(command, shell=True, timeout=timeout)
            console_output = console_output_byte.decode(encoding)  # '640x360\n'
            console_output = console_output.strip()  # '640x360'
            success = True
        except subprocess.CalledProcessError as callProcessErr:
            print(f"Error {str(callProcessErr)} for run command {command}\n\n")
        return success, console_output


if __name__ == "__main__":
    launcher: Launcher = Launcher()
    launcher.dynamic_input()
