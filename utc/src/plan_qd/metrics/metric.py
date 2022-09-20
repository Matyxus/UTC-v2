from utc.src.graph.components import Graph, Route
from utc.src.plan_qd.metrics.routes_struct import RoutesStruct
from typing import List, Dict, Tuple, Union


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
        print(f"Initializing metric: {self.name} class")

    def get_score(self, k: Union[int, float]) -> List[int]:
        """
        :param k:
        :return:
        """
        if type(k) == float:
            return self.score[0: max(int(len(self.score) * k), 1)]
        return self.score[0:min(k, len(self.score))]

    def calculate(self, struct: RoutesStruct, *args, **kwargs) -> None:
        """
        :param struct: object holding routes to be ranked and graph from which they were created
        :param args: additional args
        :param kwargs: additional args
        :return: None
        """
        raise NotImplementedError("Method 'calculate' must be implemented by children of Metric!")

    # -------------------------------------------- Utils --------------------------------------------

    def plot_ranking(self, struct: RoutesStruct, *args, **kwargs) -> None:
        """
        Shows classification / ranking of routes done by algorithm

        :param struct: object holding routes to be ranked and graph from which they were created
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("Error: method 'plot_ranking' must be implemented by children of Metric class!")



