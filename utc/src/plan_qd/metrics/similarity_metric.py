from utc.src.graph.components import Route, Graph
from utc.src.plan_qd.metrics.metric import Metric
from typing import List, Dict, Tuple, Callable
import numpy as np
from sklearn.cluster import DBSCAN


class SimilarityMetric(Metric):
    """
    Class clustering routes based on similarity,
    ordering routes based on diversity among clusters
    """

    def __init__(self):
        super().__init__("SimilarityMetric")
        self.clusters: Dict[int, Tuple[float, List[Tuple[float, int]]]] = {
            # cluster_index: (average_similarity of all routes, [average_similarity of this route, route index]),
            # ...
        }

    def calculate(self, routes: List[Route], eps: float = 0.26, min_samples: int = 4, *args, **kwargs) -> None:
        """
        :param routes: list of routes to be ordered based on current metric
        :param eps: minimal similarity between two routes for them to be added into same cluster
        :param min_samples: minimal amount of routes similar enough to be considered cluster
        :param args: additional args
        :param kwargs: additional args
        :return: None
        """
        # Compare based on edge id's using jaccard similarity, (with similarity boundary of 75% or higher)
        similarity_matrix: np.array = self.create_jaccard_matrix(routes)
        # self.pretty_print(similarity_matrix)
        reduced_dataset = DBSCAN(metric='precomputed', eps=eps, min_samples=min_samples).fit(
            self.get_jaccard_distance(similarity_matrix)
        )
        if reduced_dataset is None:
            print("Error in DBSCAN")
            return
        temp_clusters: Dict[int, List[int]] = {
            # cluster_index : [route_index (relative to inputted routes)]
        }
        # Create clusters, assign routes to them
        print(reduced_dataset.labels_)
        for index, label in enumerate(reduced_dataset.labels_):
            if label not in temp_clusters:
                temp_clusters[label] = []
            temp_clusters[label].append(index)
        # Calculate avg. similarity of routes in clusters and avg. cluster similarity
        for cluster_id, routes_indexes in temp_clusters.items():
            # For each route calculate its similarity compared to other routes in the same cluster
            cluster_size: int = len(routes_indexes)
            average_similarities: List[float] = []
            for route_index in routes_indexes:
                average_similarities.append(
                    # Average similarity of other routes (subtract itself -> similarity of 1) / number of routes
                    round((similarity_matrix[route_index][routes_indexes].sum() - 1) / cluster_size, 3)
                )
            self.clusters[cluster_id] = (
                # Average of averages
                round(sum(average_similarities), 3),
                # Assign similarity to all routes
                [(avg_similarity, route_index) for avg_similarity, route_index
                 in zip(average_similarities, routes_indexes)]
            )
        # print
        for cluster_id, values in self.clusters.items():
            print(f"Cluster: {cluster_id} has average similarity of: {values[0]}")
            for average_similarity, route_index in values[1]:
                print(f"Route: {routes[route_index].attributes['id']} has similarity of {average_similarity}")

    # -------------------------------------------- Utils --------------------------------------------

    def get_jaccard_distance(self, matrix: np.array) -> np.array:
        """
        :param matrix: jaccard similarity matrix
        :return: jaccard distance matrix
        """
        return np.ones(matrix.shape) - matrix

    def jaccard_similarity(self, v1: List[int], v2: List[int], min_size: bool = True) -> float:
        """
        :param v1: list of edge id's
        :param v2: list of edge id's
        :param min_size: true if lists should be compared using minimal size of each
        :return: jaccard similarity between two sets
        """
        # Change size to minimal
        # if min_size:
        #     size: int = min(len(v1), len(v2))
        #     v1 = v1[:size]
        #    v2 = v2[:size]
        return (len(np.intersect1d(v1, v2)) + 0.0) / len(np.union1d(v1, v2))

    def create_jaccard_matrix(self, routes: List[Route]) -> np.array:
        """
        :param routes: List of routes
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
                jaccard_matrix[i, j] = self.jaccard_similarity(
                    routes[i].get_edge_ids(as_int=True), routes[j].get_edge_ids(as_int=True)
                )
        print("Finished computing Jaccard similarity matrix")
        return jaccard_matrix + jaccard_matrix.T + np.identity(length)

    def pretty_print(self, similarity_matrix: np.array):
        for row in similarity_matrix:
            for col in row:
                print("{:8.3f}".format(col).lstrip(), end="  ")
            print("")

    def plot_ranking(self, graph: Graph) -> None:
        pass

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


class SimilarityMetric2(Metric):
    """
    Class clustering routes based on similarity,
    ordering routes based on diversity among clusters
    """

    def __init__(self):
        super().__init__("SimilarityMetric")
        self.clusters: Dict[int, List[Route]] = {}

    def calculate(self, routes: List[Route], *args, **kwargs) -> None:
        # self.pretty_print(self.create_jaccard_matrix(routes, self.jaccard_distance))
        reduced_dataset = DBSCAN(metric='precomputed', eps=0.26, min_samples=4).fit(
            self.create_jaccard_matrix(routes, self.jaccard_distance)
        )
        if reduced_dataset is None:
            print("Error in DBSCAN")
            return
        print(reduced_dataset.labels_)
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