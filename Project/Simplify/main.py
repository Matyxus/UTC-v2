from typing import Dict, List, Set
from Project.Simplify.Graph_modules import Display, ShortestPath, Simplify, Loader
from Project.Simplify.Components import Skeleton
from Project.Utils import UserInterface
from Project.constants import CWD
import os


class Launcher(UserInterface):
    """ Class that launches program, ask user for input """

    def __init__(self):
        super().__init__()
        # Graph modules
        self.display: Display = Display()
        self.shortest_path: ShortestPath = ShortestPath()
        self.simplify: Simplify = Simplify()
        self.loader: Loader = Loader()
        # Maps names of graphs to Graph class
        self.graphs: Dict[str, Skeleton] = {}
        # Set functions to commands (inherited from parent class)
        self.functions["load"] = [self.load_command, 1, 1]
        self.functions["plot"] = [self.plot_command, 1, 1]
        self.functions["simplify"] = [self.simplify_command, 1, 2]
        self.functions["subgraph"] = [self.sub_graph_command, 5, 6]
        self.functions["merge"] = [self.merge_command, 2, 3]
        self.functions["save"] = [self.save_command, 2, 2]
        self.functions["graphs"] = [self.graphs_command, 0, 0]
        self.functions["delete"] = [self.delete_command, 1, 1]

    def dynamic_input(self) -> None:
        print("Starting program, for help type 'help', expecting white space between command arguments.")
        while self.running:
            # ------------ Input ------------
            text: str = input("Type command: ")
            user_input: List[str] = text.split()
            # Check input
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

    # ----------------------------------------- Commands -----------------------------------------

    def load_command(self, args: List[str]) -> None:
        temp: Skeleton = Skeleton()
        self.loader.set_skeleton(temp)
        # Error while loading
        if not self.loader.load_map(args[0]):
            return
        self.graphs[args[0]] = temp

    def plot_command(self, args: List[str]) -> None:
        if args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        self.display.set_skeleton(self.graphs[args[0]])
        self.display.plot()

    def simplify_command(self, args: List[str]) -> None:
        if args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        display: Display = None
        if len(args) == 2 and args[1].lower() == "true":
            display = self.display
        self.simplify.set_skeleton(self.graphs[args[0]])
        self.simplify.simplify(False)

    def sub_graph_command(self, args: List[str]) -> None:
        if args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        # Check args
        try:
            float(args[4])
        except ValueError:
            print(f"Expecting number as 4th argument, got: {args[4]}!")
            return
        # Check path
        graph: Skeleton = self.graphs[args[0]]
        self.shortest_path.set_skeleton(graph)
        queue, route = self.shortest_path.a_star(args[2], args[3])
        if route is None:
            print(f"No path exists between: {args[2]} and {args[3]}")
            return
        plot: bool = False
        if len(args) == 6 and args[-1].lower() == "true":
            plot = True
        routes = self.shortest_path.top_k_a_star(args[2], args[3], float(args[4]), plot)
        # -------------------------------- Init --------------------------------
        sub_graph: Skeleton = self.graphs[args[0]].create_sub_graph(routes)
        if sub_graph is None:
            print("Could not create subgraph")
            return
        self.graphs[args[1]] = sub_graph
        print(f"Finished creating sub-graph: {args[1]}")
    
    def merge_command(self, args: List[str]) -> None:
        if args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        elif args[1] not in self.graphs:
            print(f"Graph with name: {args[1]} does not exist")
            return
        plot: bool = False
        if len(args) == 3 and args[-1].lower() == "true":
            plot = True
        self.graphs[args[0]].merge(self.graphs[args[1]], plot)
        print(f"Finished merging graphs: {args[0]} with {args[1]}")

    def graphs_command(self, args: List[str]) -> None:
        print("Printing all graphs names:")
        for graph_name in self.graphs:
            print(graph_name)

    def delete_command(self, args: List[str]) -> None:
        if args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        self.graphs.pop(args[0])

    def save_command(self, args: List[str]) -> None:
        if args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        path: str = (CWD + "/Maps/sumo/" + args[1] + ".net.xml")
        graph: Skeleton = self.graphs[args[0]]
        graph.validate_graph()
        command: str = f"netconvert --sumo-net-file {CWD + '/Maps/sumo/' + graph.map_name}.net.xml "
        edges: Set[str] = set()
        for route in graph.routes.values():
            for edge in route.edge_list:
                edges.add(edge.attributes["id"])
        command += f"--keep-edges.explicit \"{', '.join(edges)}\" -o {path}"
        print(f"Executing command: {command}")
        try:
            os.system(command)
        except Exception as e:
            print(f"Error occurred: {e}")

    def help_command(self, args: List[str]) -> None:
        help_string: str = ("""
        1) load map_name -> creates graph named map_name (map_name is used to plot, merge with others)
            1.1) map_name -> name of map to be loaded, has to be in /Maps/sumo/map_name.net.xml

        2) plot graph_name -> plots graph using matplotlib
            2.1) graph_name -> name of graph to be shown

        3) simplify graph_name, plot* -> simplifies junctions and roundabouts in graph
            3.1) graph_name ->  name of graph to simplify
            3.2) plot -> bool (true/false), if process should be displayed

        4) subgraph graph_name, subgraph_name, junction_1, junction_2, c, plot*
            4.1) graph_name -> name of graph from which sub_graph will be made
            4.2) sub_graph_name -> name of created sub_graph, can be used to call Plot afterwards
            4.3) junction_1 -> starting point of sub-graph
            4.4) junction_2 -> ending point of sub-graph
            4.5) c -> maximal route length (shortest_path * c), must be higher than 1
            4.6) plot -> bool (true, false), if process should be displayed

        5) merge graph_name_1, graph_name_2, plot* -> merges graphs together, result will be in graph_name_1
            5.1) graph_name_1 -> name of first graph
            5.2) graph_name_2 -> name of second graph
            5.3) plot -> bool (true, false), if process should be displayed

        6) validate sub_graph_name -> Removes all unused junctions, edges, routes from subgraph
        
        7) save graph_name file_name -> Saves graph into network file as '.net.xml'

        7) ------ Utils ------
            7.1) graphs -> prints names of all created sub-graphs
            7.2) delete graph_name -> deletes graph named graph_name
            7.3) exit -> quits the program
            7.4) help -> prints what commands do, their arguments etc.
        
        !) Do not use file extension when typing name of file! 
        *) Astrix (*) is for optional arguments
        """)
        print(help_string)


# Program start
if __name__ == "__main__":
    launcher: Launcher = Launcher()
    launcher.dynamic_input()





