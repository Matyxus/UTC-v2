from utc.src.graph.components import Skeleton, Graph, Route
from utc.src.plan_qd.metrics import SimilarityMetric, BottleneckMetric
from typing import List


class PlanQDLauncher:
    """
    Class launching methods for plan quality & diversity testing
    """
    def __init__(self):
        super().__init__()
        self.graph: Graph = None
        self.similarity_metric: SimilarityMetric = SimilarityMetric()
        self.bottleneck_metric: BottleneckMetric = BottleneckMetric()

    def initialize_graphs(self, network_name: str) -> None:
        """
        :param network_name: name of network
        :return: None
        """
        #
        self.graph = Graph(Skeleton())
        self.graph.loader.load_map(network_name)
        self.graph.simplify.simplify_graph()

    def subgraph(self,
                 from_junction: str, to_junction: str,
                 c: float, k: float, plot: bool = False
                 ) -> None:
        """
        :param from_junction: starting junction of sub-graph
        :param to_junction: ending junction of sub-graph
        :param c: maximal route length (shortest_path * c), must be higher than 1
        :param k: number of best routes to be used for subgraph (if value between 0,1 -> percentage of total routes)
        :param plot:
        :return:
        """
        if self.graph is None:
            print("Graph is not initialized")
            return
        routes = self.graph.shortest_path.top_k_a_star(
            from_junction, to_junction, c, self.graph.display if plot else None
        )
        if not routes:
            print("Found no routes!")
            return
        print(f"Found {len(routes)} routes")

        self.bottleneck_metric.calculate(routes)
        self.bottleneck_metric.show_bottlenecks(self.graph)
        # self.similarity_metric.calculate(routes)
        # self.similarity_metric.show_clusters(self.graph)

        # -------------------------------- Init --------------------------------
        sub_graph: Skeleton = self.graph.sub_graph.create_sub_graph(routes)
        if sub_graph is None:
            print("Could not create subgraph")
            return
        # Plot the basic graph
        graph: Graph = Graph(sub_graph)
        graph.display.plot()
        # Plot graph made with metrics


if __name__ == "__main__":
    temp: PlanQDLauncher = PlanQDLauncher()
    temp.initialize_graphs("Rome")
    temp.subgraph("54", "75", 1.6, 0, False)

