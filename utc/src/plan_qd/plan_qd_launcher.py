from utc.src.graph.components import Skeleton, Graph, Route
from utc.src.plan_qd.metrics import SimilarityMetric, BottleneckMetric, RoutesStruct
from utc.src.file_system import MyFile, InfoFile, FilePaths
from utc.src.ui import UserInterface
from typing import List, Dict


class PlanQDLauncher(UserInterface):
    """
    Class launching methods for plan quality & diversity testing
    """
    def __init__(self):
        super().__init__("user_interface")
        self.routes_struct: RoutesStruct = None
        self.similarity_metric: SimilarityMetric = SimilarityMetric()
        self.bottleneck_metric: BottleneckMetric = BottleneckMetric()
        self.graphs: Dict[str, Skeleton] = {}
        self.info_file = InfoFile("")

    def initialize_commands(self) -> None:
        super().initialize_commands()

    # -------------------------------------------- Commands --------------------------------------------

    def load_graph(self, network_name: str) -> None:
        """
        :param network_name: name of network
        :return: None
        """
        if not MyFile.file_exists(FilePaths.NETWORK_SUMO_MAPS.format(network_name)):
            return
        self.routes_struct: RoutesStruct = RoutesStruct([], None)
        graph = Graph(Skeleton())
        graph.loader.load_map(network_name)
        graph.simplify.simplify_graph()
        self.routes_struct.set_graph(graph)

    def subgraph(
            self, name: str, from_junction: str, to_junction: str,
            c: float, k: float, plot: bool = False, metrics=None
            ) -> None:
        """
        :param name:
        :param from_junction: starting junction of sub-graph
        :param to_junction: ending junction of sub-graph
        :param c: maximal route length (shortest_path * c), must be higher than 1
        :param k: number of best routes to be used for subgraph (if value between 0-1 -> percentage of total routes)
        :param metrics:
        :param plot:
        :return:
        """
        if metrics is None:
            metrics = ["all"]
        if self.routes_struct.graph is None:
            print("Graph is not initialized")
            return
        routes = self.routes_struct.graph.shortest_path.top_k_a_star(
            from_junction, to_junction, c, self.routes_struct.graph.display if plot else None
        )
        if not routes:
            print("Found no routes!")
            return
        self.routes_struct.set_routes(routes)
        # Metrics
        # self.bottleneck_metric.calculate(self.routes_struct)
        # self.bottleneck_metric.plot_ranking(self.routes_struct)
        self.similarity_metric.calculate(self.routes_struct)
        self.similarity_metric.plot_ranking(self.routes_struct)
        # -------------------------------- Sub-graphs --------------------------------
        sub_graph: Skeleton = self.routes_struct.graph.sub_graph.create_sub_graph(routes)
        if sub_graph is None:
            print("Could not create subgraph")
            return
        self.graphs[name] = sub_graph
        # Plot the basic graph
        graph: Graph = Graph(sub_graph)
        print("Plotting default sub-graph")
        graph.display.plot()
        # Plot graph\s made with metrics




    def merge(self, graph_name: str, graph_a: str, graph_b: str, plot: bool = False) -> None:
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


if __name__ == "__main__":
    temp: PlanQDLauncher = PlanQDLauncher()
    temp.initialize_graphs("Rome")
    temp.subgraph("54", "75", 1.6, 0, False)

