from utc.src.graph.components import Route, Graph
from utc.src.plan_qd.metrics.metric import Metric
from utc.src.plan_qd.metrics.routes_struct import RoutesStruct
from typing import List, Dict, Tuple, Iterator
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

    def calculate(self, struct: RoutesStruct, eps: float = 0.26, min_samples: int = 4, *args, **kwargs) -> None:
        """
        :param struct:
        :param eps: minimal similarity between two routes for them to be added into same cluster
        :param min_samples: minimal amount of routes similar enough to be considered cluster
        :param args: additional args
        :param kwargs: additional args
        :return: None
        """
        # Compare based on edge id's using jaccard similarity, (with similarity boundary of 75% or higher)
        similarity_matrix: np.array = self.create_jaccard_matrix(struct.routes)
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
        print(reduced_dataset.labels_)
        # Create clusters, assign routes to them
        for index, label in enumerate(reduced_dataset.labels_):
            if label not in temp_clusters:
                temp_clusters[label] = []
            temp_clusters[label].append(index)
        # Calculate avg. similarity of routes in clusters and avg. cluster similarity
        for cluster_id, routes_indexes in temp_clusters.items():
            # For each route calculate its similarity compared to other routes in the same cluster
            cluster_size: int = len(routes_indexes)
            average_similarities: List[Tuple[float, int]] = []
            for route_index in routes_indexes:
                average_similarities.append((
                    # Average similarity of other routes (subtract itself -> similarity of 1) / number of routes
                    round((similarity_matrix[route_index][routes_indexes].sum() - 1) / cluster_size, 3),
                    route_index
                ))
            self.clusters[cluster_id] = (
                # Average of averages
                round(sum([pair[0] for pair in average_similarities]) / cluster_size, 3),
                # Assign similarity to all routes
                sorted(average_similarities, key=lambda tup: tup[0])
            )
        for cluster_id, value in self.clusters.items():
            print(f"Cluster: {cluster_id} has average similarity of: {value[0]}")
            for average_similarity, route_id in value[1]:
                print(f"Route: {route_id} has similarity of {average_similarity}")
        print(f"Clusters number: {len(self.clusters)}")
        temp_clusters.clear()
        # Sort clusters by average similarity
        sorted_clusters_ids: list = sorted(list(self.clusters.items()), key=lambda tup: tup[1])
        # Rank by most diverse
        sorted_clusters_ids: List[List[Tuple[float, int]]] = [cluster[1][1] for cluster in sorted_clusters_ids]
        index: int = 0
        while sorted_clusters_ids:
            if sorted_clusters_ids[index]:
                cluster = sorted_clusters_ids[index].pop(0)
                self.score.append(cluster[1])
            else:
                sorted_clusters_ids.pop(index)
            index += 1
            if index >= len(sorted_clusters_ids):
                index = 0
        # print
        # for cluster_id, value in self.clusters.items():
        #    print(f"Cluster: {cluster_id} has average similarity of: {value[0]}")
        #    for average_similarity, route_id in value[1]:
        #        print(f"Route: {route_id} has similarity of {average_similarity}")
    # -------------------------------------------- Jaccard --------------------------------------------

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
        """
        if min_size:
            size: int = min(len(v1), len(v2))
            v1 = v1[:size]
            v2 = v2[:size]
        """
        return (len(np.intersect1d(v1, v2)) + 0.0) / len(np.union1d(v1, v2))

    def create_jaccard_matrix(self, routes: List[Route]) -> np.array:
        """
        :param routes: list of routes
        :return: array containing similarity between each route (2D symmetric matrix)
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

    # -------------------------------------------- Utils --------------------------------------------

    def pretty_print(self, similarity_matrix: np.array):
        for row in similarity_matrix:
            for col in row:
                print("{:8.3f}".format(col).lstrip(), end="  ")
            print("")

    def plot_ranking(self, struct: RoutesStruct, most_similar: bool = True, *args, **kwargs) -> None:
        temp_colors: List[str] = ["red", "blue", "purple", "green", "yellow", "pink", "brown"]
        if len(self.clusters) > len(temp_colors):
            print(f"Not enough colors: {len(temp_colors)} for all clusters: {len(self.clusters)}")
            return
        fig, ax = struct.graph.display.default_plot()
        for i in range(7):
            struct.graph.display.add_label("o", temp_colors[i], f"C{i}")
            struct.routes[self.score[i]].plot(ax, color=temp_colors[i])
        struct.graph.display.make_legend(7)
        struct.graph.display.show_plot()
        """
        # Plot most similar/di-similar routes in clusters
        for index, cluster_id in enumerate(self.clusters.keys()):
            fig, ax = struct.graph.display.default_plot()
         
            if most_similar:
                highest_avg_similarity, route_index = max(self.clusters[cluster_id][1], key=lambda item: item[0])
            else:
                highest_avg_similarity, route_index = min(self.clusters[cluster_id][1], key=lambda item: item[0])
            struct.routes[route_index].plot(ax, color=temp_colors[index])
            struct.graph.display.make_legend(len(self.clusters))
            struct.graph.display.show_plot()
        """

