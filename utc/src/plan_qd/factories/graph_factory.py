from utc.src.graph.components import Skeleton, Graph, Route
from utc.src.graph import GraphMain
from typing import List


class GraphFactory:
    """

    """
    def __init__(self):
        self.graph_main: GraphMain = GraphMain()
        self.graph_main.initialize_input()

    def initialize(self, network_name: str) -> None:
        self.graph_main.process_input(
            "load-graph", f'map_name="{network_name}"'
        )
        # Plot is false by default
        self.graph_main.process_input(
            "simplify", f'graph_name="{network_name}" plot="f"'
        )

    def generate_sub_graph(
            self, subgraph_name: str, graph_name: str, from_junction: str,
            to_junction: str, c: float, plot: str = "f"
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
        if self.graph_main is None:
            return
        self.graph_main.process_input(
            "subgraph",
            f'subgraph_name="{subgraph_name}" graph_name="{graph_name}" from_junction="{from_junction}" '
            f'to_junction="{to_junction}" c="{c}" plot="{plot}"'
        )

    def merge_command(self, graph_name: str, graph_a: str, graph_b: str, plot: str = "f") -> None:
        """
        :param graph_name: new name of created graph
        :param graph_a: name of first graph (which will be merged)
        :param graph_b: name of second graph (which will be merged)
        :param plot: bool (true, false), if process should be displayed
        :return: None
        """
        if self.graph_main is None:
            return
        self.graph_main.process_input(
            "merge",
            f'graph_name="{graph_name}" graph_a="{graph_a}" graph_b="{graph_b}" plot="{plot}"'
        )


# For testing purposes
if __name__ == "__main__":
    graph_factory: GraphFactory = GraphFactory()
    graph_factory.initialize("Dejvice")




