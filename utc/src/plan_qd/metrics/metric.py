from utc.src.graph.components import Graph, Route
from typing import List, Union, Optional


class Metric:
    """
    General class providing framework for metric-type classes
    """

    def __init__(self, metric_name: str):
        """
        :param metric_name: name of metric
        """
        # Sorted routes id's (ranked by algorithm)
        self.score: List[int] = []
        self.name = metric_name
        print(f"Initializing metric: '{self.name}' class")

    def get_score(self, k: Union[int, float]) -> Optional[List[int]]:
        """
        :param k: number of best routes to pick (if float, used as percentage)
        :return: list of route indexes to be picked
        """
        if isinstance(k, float) and not k.is_integer():
            if not (0 < k <= 1):
                print(f"Expected float parameter 'k' to be between 0 and 1, got: '{k}' !")
                return None
            return self.score[0: max(int(len(self.score) * k), 1)]
        elif k > len(self.score):
            print(f"Received 'k': '{k}', which is greater than number of ordered routes: '{len(self.score)}'")
        k = int(k)
        return self.score[0:min(int(k), len(self.score))]

    def calculate(self, routes: List[Route], graph: Graph, plot: bool = False, *args, **kwargs) -> None:
        """
        :param routes: list of routes to rank
        :param graph: to which routes belong
        :param plot: bool, if metric ordering should be plotted, default false
        :param args: additional args
        :param kwargs: additional args
        :return: None
        """
        raise NotImplementedError("Method 'calculate' must be implemented by children of Metric!")

    # -------------------------------------------- Utils --------------------------------------------

    def plot_ranking(self, routes: List[Route], graph: Graph, *args, **kwargs) -> None:
        """
        Shows classification / ranking of routes done by algorithm

        :param routes: list of routes to rank
        :param graph: to which routes belong
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Error: method 'plot_ranking' must be implemented by children of Metric class!")

    def clear(self) -> None:
        """
        Clears the previously created score

        :return: None
        """
        self.score.clear()

