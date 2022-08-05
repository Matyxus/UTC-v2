from utc.src.graph.components import Route, Graph
from utc.src.plan_qd.metrics.metric import Metric
from typing import List, Dict, Callable
import numpy as np
from sklearn.cluster import DBSCAN


class SimilarityMetric(Metric):
    """
    Class clustering routes based on similarity,
    ordering routes based on diversity among clusters
    """

    def __init__(self):
        super().__init__("SimilarityMetric")
        self.clusters: Dict[int, List[Route]] = {}

    def calculate(self, routes: List[Route], *args, **kwargs) -> None:
        reduced_dataset = DBSCAN(metric='precomputed', eps=0.26, min_samples=4).fit(
            self.create_jaccard_matrix(routes, self.jaccard_distance)
        )
        if reduced_dataset is None:
            print("Error in DBSCAN")
            return
        for index, label in enumerate(reduced_dataset.labels_):
            if label not in self.clusters:
                self.clusters[label] = []
            self.clusters[label].append(routes[index])

    # -------------------------------------------- Utils --------------------------------------------

    def jaccard_distance(self, v1: List[int], v2: List[int]) -> float:
        """

        :param v1: list of edge id's
        :param v2: list of edge id's
        :return: jaccard distance
        """
        return 1 - (len(np.intersect1d(v1, v2)) + 0.0) / len(np.union1d(v1, v2))

    def jaccard_similarity(self, v1: List[int], v2: List[int]) -> float:
        """

        :param v1: list of edge id's
        :param v2: list of edge id's
        :return: jaccard distance
        """
        return (len(np.intersect1d(v1, v2)) + 0.0) / len(np.union1d(v1, v2))

    def create_jaccard_matrix(self, routes: List[Route], func: Callable[[List[int], List[int]], float]) -> np.array:
        """
        :param routes: List of routes
        :param func: method to be used (similarity or distance)
        :return: Array containing similarity between each route (2D symmetric matrix)
        """
        print("Computing similarity matrix")
        length: int = len(routes)
        if length < 2:
            print("Cannot create similarity matrix, length of routes list must be at least 2")
            return np.array([[]])
        jaccard_matrix: np.array = np.zeros([length, length])
        # -1, since we want to skip diagonal (route has similarity of "1" to itself)
        for i in range(length-1):
            for j in range(i+1, length):
                jaccard_matrix[i, j] = func(
                    routes[i].get_edge_ids(as_int=True), routes[j].get_edge_ids(as_int=True)
                )
        print("Finished computing Jaccard matrix")
        return jaccard_matrix + jaccard_matrix.T  # + np.identity(length)

    def pretty_print(self, similarity_matrix: np.array):
        for row in similarity_matrix:
            for col in row:
                print("{:8.3f}".format(col).lstrip(), end="  ")
            print("")

    def show_clusters(self, graph: Graph) -> None:
        """
        Plots clusters of routes

        :param graph: to which routes belong
        :return: None
        """
        for route_group, grouped_routes in self.clusters.items():
            fig, ax = graph.display.default_plot()
            print(f"Route group: {route_group}")
            for route in grouped_routes:
                route.plot(ax, color="red")
            graph.display.show_plot()

