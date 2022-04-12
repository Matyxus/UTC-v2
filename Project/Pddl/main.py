from typing import List
from Project.Utils import UserInterface
from Project.Simplify.Graph_modules import Display, ShortestPath, Simplify, Loader
from Project.Simplify.Components import Skeleton
from Project.constants import file_exists
from Project.Pddl.Domain import Utc


class Launcher(UserInterface):
    """ """

    def __init__(self):
        super().__init__()
        self.graph: Skeleton = None
        # Graph modules
        self.display: Display = Display()
        self.shortest_path: ShortestPath = ShortestPath()
        self.simplify: Simplify = Simplify()
        self.loader: Loader = Loader()
        self.functions["generate-baseline"] = [self.baseline_command, 1, 1]
        self.functions["generate-problem"] = [self.problem_command, 1, 1]
        self.functions["add-cars"] = [self.cars_command, 1, 1]
        self.functions["generate-result"] = [self.result_command, 1, 2]

    def dynamic_input(self) -> None:
        print("Starting program, for help type 'help', expecting white space between command arguments.")
        while self.running:
            # ------------ Input ------------
            text: str = input("Type command: ")
            user_input: List[str] = []
            # Check input
            if text:
                user_input = text.split()
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

    def baseline_command(self, args: List[str]) -> None:
        pass

    def problem_command(self, args: List[str]) -> None:
        if not file_exists(args[0]):
            pass
        elif not file_exists(args[2]):
            pass
        creating_problem = True
        print("Generating problem")
        while creating_problem:
            pass

    def cars_command(self, args: List[str]) -> None:
        pass

    def result_command(self, args: List[str]) -> None:
        pass

    def help_command(self, args: List[str]) -> None:
        help_string: str = ("""
        1) generate-problem domain_name, problem_name, network_name
            1.1) map_name -> name of map to be loaded, has to be in /Maps/sumo/map_name.net.xml
            1.2) 
        2*) finish -> finishes generating problem

        3) generate-baseline problem_name -> generates shortest path for cars (only for utc domain)
            3.1) problem_name -> name of problem  (/Problems/generated/problem_name.pddl)

        4) generate-result planner_name, domain_name, problem_name, result_name -> calls planner to generate solution
            4.1) planner_name -> name of planner (/Planers/planner_name)
            4.2) domain_name  -> name of domain (/Domain/Domains/domain_name.pddl)
            4.2) problem_name -> name of problem file (will be save in /Problems/generated/problem_name.pddl)
            4.3) result_name  -> name of solution file (will be save in /Problems/solved/result_name.pddl)

        5*) add-cars amount, from_junction_id, to_junction_id
            5.1) amount -> name of graph from which sub_graph will be made
            5.2) from_junction_id -> name of created sub_graph, can be used to call Plot afterwards
            5.3) to_junction_id -> starting point of sub-graph
            

        6) ------ Utils ------
            6.1) quit -> quits the program
            6.2) help -> prints what commands do, their arguments etc.
            * Only works when generating problem

        !) Do not use file extension/file_path when typing name of file! 
        """)
        print(help_string)


if __name__ == "__main__":
    skeleton: Skeleton = Skeleton()
    loader: Loader = Loader()
    loader.set_skeleton(skeleton)
    display: Display = Display()
    display.set_skeleton(skeleton)
    simplify: Simplify = Simplify()
    simplify.set_skeleton(skeleton)
    loader.load_map("test")
    simplify.simplify_junctions(plot=False)
    display.plot()
    skeleton.validate_graph()
    temp: Utc = Utc()
    temp.set_problem_name("utc-test")
    temp.add_network(skeleton)
    for i in range(10):
        temp.add_car("6816134641", "67843610")
    temp.save("test")






