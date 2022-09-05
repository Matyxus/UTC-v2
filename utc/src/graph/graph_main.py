from typing import Dict, Set
from utc.src.graph.components import Skeleton, Graph
from utc.src.ui import UserInterface, Command
from utc.src.file_system import FilePaths, InfoFile


class GraphMain(UserInterface):
    """ Class that launches program, ask user for input """

    def __init__(self):
        super().__init__("graph")
        # Graph modules
        self.graph: Graph = Graph()
        # Maps names of graphs to Graph class
        self.graphs: Dict[str, Skeleton] = {}
        # Info file
        self.info_file = InfoFile("")
        self.info_file.add_allowed_commands(["load-graph", "simplify", "subgraph", "merge", "save-graph"])

    def initialize_commands(self) -> None:
        super().initialize_commands()
        self.user_input.add_command([
            ("load-graph", Command("load-graph", self.load_command)),
            ("plot-graph", Command("plot-graph", self.plot_command)),
            ("simplify", Command("simplify", self.simplify_command)),
            ("subgraph", Command("subgraph", self.sub_graph_command)),
            ("merge", Command("merge", self.merge_command)),
            ("save-graph", Command("save-graph", self.save_command)),
            ("graphs", Command("graphs", self.graphs_command)),
            ("delete-graph", Command("delete-graph", self.delete_command)),
        ])

    # ----------------------------------------- Commands -----------------------------------------

    def load_command(self, map_name: str) -> None:
        """
        :param map_name: load map from /Maps/sumo/map_name.net.xml and creates graph named map_name
        :return: None
        """
        temp: Skeleton = Skeleton()
        self.graph.set_skeleton(temp)
        # Error while loading
        if not self.graph.loader.load_map(map_name):
            return
        self.graphs[map_name] = temp

    def plot_command(self, graph_name: str) -> None:
        """
        :param graph_name: name of graph to be displayed
        :return: None
        """
        if not self.graph_exists(graph_name):
            return
        self.graph.set_skeleton(self.graphs[graph_name])
        self.graph.display.plot()

    def simplify_command(self, graph_name: str, plot: bool = False) -> None:
        """
        Replaces junctions forming roundabouts with single junction,
        removes junctions that do not need to be in graph

        :param graph_name: name of graph to simplify
        :param plot: bool (true/false), if process should be displayed
        :return: None
        """
        if not self.graph_exists(graph_name):
            return
        self.graph.set_skeleton(self.graphs[graph_name])
        self.graph.simplify.simplify_graph(self.graph.display if plot else None)

    def sub_graph_command(
            self, subgraph_name: str, graph_name: str, from_junction: str,
            to_junction: str, c: float, plot: bool = False
         ) -> None:
        """
        :param subgraph_name: new name of created sub-graph
        :param graph_name: name of graph from which sub-graph will be made
        :param from_junction: starting junction of sub-graph
        :param to_junction: ending junction of sub-graph
        :param c: maximal route length (shortest_path * c), must be higher than 1
        :param plot: bool (true, false), if process should be displayed
        :return: None
        """
        if not self.graph_exists(graph_name):
            return
        self.graph.set_skeleton(self.graphs[graph_name])
        routes = self.graph.shortest_path.top_k_a_star(
            from_junction, to_junction, c, self.graph.display if plot else None
        )
        # -------------------------------- Init --------------------------------
        sub_graph: Skeleton = self.graph.sub_graph.create_sub_graph(routes)
        if sub_graph is None:
            print("Could not create subgraph")
            return
        self.graphs[subgraph_name] = sub_graph
        print(f"Finished creating sub-graph: {subgraph_name}")
    
    def merge_command(self, graph_name: str, graph_a: str, graph_b: str, plot: bool = False) -> None:
        """
        :param graph_name: new name of created graph
        :param graph_a: name of first graph (which will be merged)
        :param graph_b: name of second graph (which will be merged)
        :param plot: bool (true, false), if process should be displayed
        :return: None
        """
        # Checks
        if not self.graph_exists(graph_b):
            return
        elif not self.graph_exists(graph_b):
            return
        # Merge
        self.graph.set_skeleton(self.graphs[graph_a])
        new_graph: Skeleton = self.graph.sub_graph.merge(self.graphs[graph_b], self.graph.display if plot else None)
        if new_graph is None:
            print("Could not merge graphs")
            return
        self.graphs[graph_name] = new_graph
        print(f"Finished merging graphs: {graph_a} with {graph_b}, created graph: {graph_name}")

    def graphs_command(self) -> None:
        """
        Prints names of all created sub-graphs

        :return: None
        """
        print("Printing all graphs names:")
        for graph_name in self.graphs:
            print("\t" + graph_name)

    def delete_command(self, graph_name: str) -> None:
        """
        :param graph_name: name of graph to be deleted
        :return: None
        """
        if not self.graph_exists(graph_name):
            return
        self.graphs.pop(graph_name)

    def save_command(self, graph_name: str, file_name: str) -> None:
        """
        Saves graph into /Maps/sumo/file_name.net.xml

        :param graph_name: to be saved
        :param file_name: name of file containing new road network
        :return: None
        """
        if not self.graph_exists(graph_name):
            return
        path: str = FilePaths.NETWORK_SUMO_MAPS.format(file_name)
        graph: Skeleton = self.graphs[graph_name]
        graph.validate_graph()
        command: str = f"netconvert --sumo-net-file {FilePaths.NETWORK_SUMO_MAPS.format(graph.map_name)} "
        edges: Set[str] = set()
        for route in graph.routes.values():
            for edge in route.edge_list:
                edges.add(edge.attributes["id"])
        command += f"--keep-edges.explicit \"{', '.join(edges)}\" -o {path}"
        self.run_command(command)
        # Save info file
        self.info_file.save(FilePaths.MAPS_INFO.format(file_name))

    # ----------------------------------------- Utils -----------------------------------------

    def graph_exists(self, graph_name: str, message: bool = True) -> bool:
        """
        :param graph_name: to be checked for existence
        :param message: if message about graph not existing should be printed (default true)
        :return: true if graph exists, false otherwise
        """
        if graph_name not in self.graphs:
            if message:
                print(f"Graph: '{graph_name}' does not exist!")
            return False
        return True


# Program start
if __name__ == "__main__":
    launcher: GraphMain = GraphMain()
    launcher.run()
