from utc.src.graph.components import Route
from typing import List, Dict


class Metrics:
    """
    Class containing methods which rank routes based on parameters
    """

    def __init__(self):
        self.metric_map: Dict[str, callable] = {
            # metric name : method_pointer
            # "length": self.length_metric, -> when created by subgraph module, routes are already sorted
            "common_edge": self.common_edge_metric
        }

    def rank_routes(self, routes: List[Route], metrics: List[str], amount: int) -> List[Route]:
        """

        :param routes: list of routes
        :param metrics: list of metrics names to be used
        :param amount: number of routes to be returned
        :return: new list of routes
        """
        if not len(metrics):
            return routes
        methods: List[callable] = [
            self.metric_map.values() if metrics[0] == "all" else
            self.metric_map[metric] for metric in self.metric_map
        ]
        for method in methods:
            method(routes)
        if amount >= len(routes):
            amount = len(routes) - 1
        return routes[:amount]

    # -------------------------------- Diversity --------------------------------

    def common_edge_metric(self, routes: List[Route]) -> None:
        """
        Requires the list to be already sorted, compares common edges
        against recorded edges, the less common edges route has, the better

        :param routes:
        :return:
        """
        pass

    # -------------------------------- Quality --------------------------------

    def length_metric(self, routes: List[Route]) -> None:
        """
        :param routes:
        :return:
        """
        # If is already sorted, return
        if all(routes[i] <= routes[i + 1] for i in range(len(routes) - 1)):
            return
        routes.sort()

    def capacity_metric(self,  routes: List[Route]) -> None:
        """
        Compares routes based on their capacity,
        the more capacity route has, the better

        :param routes:
        :return:
        """
        pass

    def bottleneck_metric(self, routes: List[Route]) -> None:
        """
        Compares routes based on how many 'bottleneck' junctions
        route goes, the less the better

        :param routes:
        :return:
        """
        pass

    def straightness_metric(self, route: List[Route]) -> None:
        """
        Compares routes based on junctions distance from final junction, \n
        penalizes routes if their junctions distance from destination increases \n
        (multiplied for repeated occurrence), \n
        e.g.: Route 5 goes trough junctions: [A, B, C, D, ......., Z] \n
        *1) B is closer to Z than A (no penalization), \n
        *2) C is farther from Z than B (penalization) \n
        *3) D is farther from Z than C (penalization x 2 -> repeated) \n
        *4) .... \n

        Does so by making edges into vectors and comparing them against destination.

        :param route:
        :return:
        """

    def eta_metric(self, route: List[Route]) -> None:
        """
        Estimated time of arrival metric (defined by
        maximal speed on edges and route length), the
        shorter the better

        :param route:
        :return:
        """
        pass




