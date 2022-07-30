from utc.src.graph.components import Skeleton, Graph, Route
from utc.src.plan_qd.metrics import SimilarityMetric
from typing import List


class PlanQDLauncher:
    """
    Class launching methods for plan quality & diversity testing
    """
    def __init__(self):
        super().__init__()
        self.graph: Graph = None
        self.metrics: SimilarityMetric = SimilarityMetric()

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
                 c: float, plot: bool = False
                 ) -> None:
        """
        :param from_junction: starting junction of sub-graph
        :param to_junction: ending junction of sub-graph
        :param c: maximal route length (shortest_path * c), must be higher than 1
        :param plot:
        :return:
        """
        if self.graph is None:
            print("Graph is not initialized")
            return
        routes = self.graph.shortest_path.top_k_a_star(
            from_junction, to_junction, c, self.graph.display if plot else None
        )
        print(f"Found {len(routes)} routes")
        print("Groups found by DBSCAN")
        for route_group, grouped_routes in enumerate(self.metrics.create_dbscan(routes)):
            fig, ax = self.graph.display.default_plot()
            print(f"Route group: {route_group}")
            for route in grouped_routes:
                # print(f"\t{route}")
                route.plot(ax, color="red")
            self.graph.display.show_plot()
        """
        print("Groups found by kmedoids: ")
        for route_group, grouped_routes in self.metrics.rank(routes, 4).items():
            fig, ax = self.graph.display.default_plot()
            print(f"Route group: {routes[route_group]}")
            for route in grouped_routes:
                # print(f"\t{route}")
                route.plot(ax, color="blue")
            self.graph.display.show_plot()
        print("Groups found by OPTICS: ")
        for route_group, grouped_routes in enumerate(self.metrics.create_optics(routes)):
            fig, ax = self.graph.display.default_plot()
            print(f"Route group: {route_group}")
            for route in grouped_routes:
                # print(f"\t{route}")
                route.plot(ax, color="red")
            self.graph.display.show_plot()
        """
        quit()
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
    temp.subgraph("54", "75", 1.6, False)

