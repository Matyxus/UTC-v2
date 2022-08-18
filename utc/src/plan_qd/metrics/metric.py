from utc.src.graph.components import Graph, Route
from typing import List, Dict, Tuple


class Metric:
    """
    General class providing framework for metric-type classes
    """

    def __init__(self, metric_name: str):
        """
        :param metric_name: name of metric
        """
        # Score given to routes (the higher the worse), mapped by route id
        self.score: Dict[int, float] = {}
        self.name = metric_name
        print(f"Initializing metric: {self.name} class")

    def calculate(self, routes: List[Route], *args, **kwargs) -> None:
        """
        :param routes: list of routes to be ordered based on current metric
        :param args: additional args
        :param kwargs: additional args
        :return: None
        """
        raise NotImplementedError("Method 'calculate' must be implemented by children of Metric!")

    # -------------------------------------------- Utils --------------------------------------------

    def plot_ranking(self, graph: Graph) -> None:
        """
        Shows classification / ranking of routes done by algorithm

        :param graph: of ranked routes
        :return: None
        """
        raise NotImplementedError("Error: method 'plot_ranking' must be implemented by children of Metric class!")

    def get_score(self) -> Tuple[str, Dict[int, float]]:
        """
        :return: name of metric and score given to routes
        """
        return self.name, self.score


