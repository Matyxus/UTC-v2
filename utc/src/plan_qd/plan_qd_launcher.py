from utc.src.graph.components import Skeleton, Graph
from utc.src.plan_qd.metrics import Metrics
from typing import List


class PlanQDLauncher:
    """
    Class launching methods for plan quality & diversity testing
    """
    def __init__(self):
        super().__init__()
        self.graph: Graph = None
        self.metrics: Metrics = Metrics()

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
                 c: float, metrics: List[str], plot: bool = False
                 ) -> None:
        """
        :param from_junction: starting junction of sub-graph
        :param to_junction: ending junction of sub-graph
        :param c: maximal route length (shortest_path * c), must be higher than 1
        :param metrics: list of metrics names, to be used to create sub_graph
        :param plot:
        :return:
        """
        if self.graph is None:
            print("Graph is not initialized")
            return
        routes = self.graph.shortest_path.top_k_a_star(
            from_junction, to_junction, c, self.graph.display if plot else None
        )
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
