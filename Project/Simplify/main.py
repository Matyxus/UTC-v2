from typing import Dict, List
from MyGraph import Graph
from Utils.Converter import Converter


class Launcher:
    """ Class that launches program, can be run dynamically, or from command line argument """
    def __init__(self):
        # Maps names of graphs to Graph class
        self.graphs: Dict[str, Graph] = {}
        self.running: bool = True
        self.commands: dict = {
            # command_name : function
            "quit": self.handle_exit,
            "exit": self.handle_exit,
            "convert": self.handle_convert,
            "load": self.load_map,
            "plot": self.plot_map,
            "simplify": self.simplify,
            "subgraph": self.sub_graph,
            "merge": self.merge,
            "validate": self.validate,
            "graphs": self.show_graphs,
            "restart": self.clear_memory,
            "delete": self.remove_graph,
            "help": self.help
        }

    def dynamic_input(self):
        """
        Handles input dynamically passed during runtime:

        0) convert map_name (.osm)
            0.1) map_name -> name of map to be converted, has to be in //maps//osm//original//map_name.osm

        1) load map_name -> creates graph named map_name (map_name is used to plot, merge with others)
            1.1) map_name -> name of map to be loaded, has to be in //maps//sumo//map_name.net.xml

        2) Plot graph_name
            2.1) graph_name -> name of graph to be shown

        3) Simplify graph_name plot -> simplifies junctions and roundabouts in graph
            3.1) graph_name ->  name of graph to simplify\n
            3.2) plot -> bool (true, false), if process should be displayed

        4) Subgraph graph_name, subgraph_name, junction_1, junction_2, c, plot
            4.1) graph_name -> name of graph from which sub_graph will be made\n
            4.2) sub_graph_name -> name of created sub_graph, can be used to call Plot afterwards\n
            4.3) junction_1 -> starting point of sub-graph\n
            4.4) junction_2 -> ending point of sub-graph\n
            4.5) c -> maximal route length (shortest_path * c), must be higher than 1\n
            4.6) plot -> bool (true, false), if process should be displayed

        5) Merge graph_name_1 graph_name_2 plot -> merges graphs together, result will be in graph_name_1
            5.1) graph_name_1 -> name of first graph\n
            5.2) graph_name_2 -> name of second graph\n
            5.3) plot -> bool (true, false), if process should be displayed

        6) Validate sub_graph_name -> Removes all unused junctions, edges, routes from subgraph

        6) ------ Utils ------
            6.1) Graphs -> prints names of all created sub-graphs\n
            6.2) Delete graph_name -> deletes graph named graph_name\n
            6.3) Restart -> restarts the program\n
            6.4) Quit/Exit -> quits the program\n
            6.5) Help -> prints what commands do, their arguments etc.
        :return: None
        """
        print("Starting program, for help type 'help', expecting white space between command arguments.")
        while self.running:
            # ------------ Input ------------
            text: str = input("Type command: ")
            command: List[str] = []
            # Check input
            if text:
                command = text.split()
            if not len(command):
                print(f"{text} is invalid input!")
                continue
            print(f"Interpreting: {command}")
            # ------------ Command Name ------------
            command_name: str = self.get_command_name(command[0])
            # Check command name
            if not command_name:
                print(f"Invalid command name: {command[0]}")
                continue
            command.pop(0)  # Remove command name
            self.commands[command_name](command)  # Execute command
        print("Exiting...")

    # ----------------------------- Commands -----------------------------

    def handle_exit(self, args: List[str]) -> None:
        """

        :param args: arguments of exit command (expecting none)
        :return: None
        """
        self.running = False

    def handle_convert(self, args: List[str]) -> None:
        """

        :param args: arguments of convert command (expecting map_name)
        :return: None
        """
        if not len(args):
            print(f"Incorrect arguments: {args} passed to convert command, expecting map_name!")
            return
        converter: Converter = Converter(args[0])
        if converter.osm_filter():  # Filter first
            # Call net-convert if filtering was successful
            converter.net_convert()
            print()  # Print new line, net convert can output lot of text on command line

    def load_map(self, args: List[str]):
        if len(args) < 1 or len(args) > 2:
            print(f"Incorrect arguments: {args} passed to load command, expecting map_name and/or plot!")
            return
        temp: Graph = Graph()
        if not temp.load_from_file(args[0]):
            return
        self.graphs[args[0]] = temp

    def validate(self, args: List[str]):
        if len(args) != 1:
            print(f"Incorrect arguments: {args} passed to load command, expecting subgraph_name!")
            return
        elif args[0] not in self.graphs:
            print(f"Subgraph with name: {args[0]} does not exist")
            return
        self.graphs[args[0]].validate_graph()


    def simplify(self, args: List[str]):
        if len(args) < 1 or len(args) > 2:
            print(f"Incorrect arguments: {args} passed to plot simplify, expecting map_name and/or plot!")
        elif args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        plot: bool = False
        if len(args) == 2 and args[1].lower() == "true":
            plot = True
        self.graphs[args[0]].simplify_junctions(plot)
        self.graphs[args[0]].simplify_roundabouts(plot)

    def plot_map(self, args: List[str]):
        if len(args) != 1:
            print(f"Incorrect arguments: {args} passed to plot command, expecting map_name!")
            return
        elif args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        self.graphs[args[0]].plot()

    def sub_graph(self, args: List[str]):
        if len(args) < 5 or len(args) > 6:
            print(f"Incorrect arguments: {args} passed to subgraph command, expecting 5 or 6!")
            return
        elif args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        try:
            float(args[4])
        except Exception as e:
            print(f"Expecting number as 4th argument, got: {args[4]}!")
            return
        if self.graphs[args[0]].shortest_path(args[2], args[3], False) is None:
            print(f"No path exists between: {args[2]} and {args[3]}")
            return
        plot: bool = False
        if len(args) == 6 and args[-1].lower() == "true":
            plot = True
        result: Graph = self.graphs[args[0]].create_sub_graph(args[2], args[3], float(args[4]), plot)
        self.graphs[args[1]] = result
    
    def merge(self, args: List[str]):
        #  graph_name_1 graph_name_2 plot
        if len(args) < 2 or len(args) > 3:
            print(f"Incorrect arguments: {args} passed to merge command, expecting 3 or 4!")
            return
        plot: bool = False
        if len(args) == 3 and args[-1].lower() == "true":
            plot = True
        if args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        elif args[1] not in self.graphs:
            print(f"Graph with name: {args[1]} does not exist")
            return
        self.graphs[args[0]].merge(self.graphs[args[1]], plot)

    def show_graphs(self, args: List[str]):
        for graph_name in self.graphs:
            print(graph_name)

    def clear_memory(self, args: List[str]):
        self.graphs.clear()

    def remove_graph(self, args: List[str]):
        if len(args) != 1:
            print(f"Incorrect arguments: {args} passed to delete command, expecting 1!")
            return
        elif args[0] not in self.graphs:
            print(f"Graph with name: {args[0]} does not exist")
            return
        self.graphs.pop(args[0])

    def help(self, args: List[str]):
        help_string: str = ("""
        0) convert map_name (.osm)
            0.1) map_name -> name of map to be converted, has to be in //maps//osm//original//map_name.osm

        1) load map_name -> creates graph named map_name (map_name is used to plot, merge with others)
            1.1) map_name -> name of map to be loaded, has to be in //maps//sumo//map_name.net.xml

        2) Plot graph_name
            2.1) graph_name -> name of graph to be shown

        3) Simplify graph_name plot -> simplifies junctions and roundabouts in graph
            3.1) graph_name ->  name of graph to simplify
            3.2) plot -> bool (true, false), if process should be displayed

        4) Subgraph graph_name, subgraph_name, junction_1, junction_2, c, plot
            4.1) graph_name -> name of graph from which sub_graph will be made
            4.2) sub_graph_name -> name of created sub_graph, can be used to call Plot afterwards
            4.3) junction_1 -> starting point of sub-graph
            4.4) junction_2 -> ending point of sub-graph
            4.5) c -> maximal route length (shortest_path * c), must be higher than 1
            4.6) plot -> bool (true, false), if process should be displayed

        5) Merge graph_name_1 graph_name_2 plot -> merges graphs together, result will be in graph_name_1
            5.1) graph_name_1 -> name of first graph
            5.2) graph_name_2 -> name of second graph
            5.3) plot -> bool (true, false), if process should be displayed

        6) Validate sub_graph_name -> Removes all unused junctions, edges, routes from subgraph

        6) ------ Utils ------
            6.1) Graphs -> prints names of all created sub-graphs
            6.2) Delete graph_name -> deletes graph named graph_name
            6.3) Restart -> restarts the program
            6.4) Quit/Exit -> quits the program
            6.5) Help -> prints what commands do, their arguments etc.
        """)
        print(help_string)

    # ----------------------------- Utils -----------------------------

    def get_command_name(self, command_name: str) -> str:
        """
        :param command_name: name of command from command line
        :return: command name in commands dictionary, empty string if it does not exist
        """
        command_name = command_name.lower()
        if command_name in self.commands:
            return command_name
        return ""


# Program start
if __name__ == "__main__":
    launcher: Launcher = Launcher()
    launcher.dynamic_input()
