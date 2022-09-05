from utc.src.graph.components import Route, Graph
from typing import List


class RoutesStruct:
    """

    """
    def __init__(self, routes: List[Route] = None, graph: Graph = None):
        self.routes: List[Route] = routes
        self.graph: Graph = graph

    def set_graph(self, graph: Graph) -> None:
        """
        :param graph:
        :return:
        """
        if graph is None:
            print(f"Cannot set graph of type 'None' !")
            return
        self.graph = graph

    def set_routess(self, routes: List[Route]) -> None:
        """
        :param routes:
        :return:
        """
        if not routes:
            print(f"Cannot set routes which are empty!")
            return
        self.routes = routes

