from utc.src.graph.components import Route, Graph
from utc.src.plan_qd.metrics.metric import Metric
from typing import List, Dict, Tuple, Iterator, Optional
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt


class SimilarityMetric(Metric):
    """
    Class clustering routes based on similarity,
    ordering routes based on diversity among clusters
    """

    def __init__(self):
        super().__init__("SimilarityMetric")

    def calculate(
            self, routes: List[Route], graph: Graph,
            eps: float = 0.26, min_samples: int = 4,
            sort_by: str = "", plot: bool = False,
            sim_matrix: np.array = None,
            *args, **kwargs
            ) -> None:
        """
        :param routes: to be ranked by algorithm
        :param graph: from which routes were extracted
        :param eps: minimal similarity between two routes for them to be added into same cluster
        :param min_samples: minimal amount of routes similar enough to be considered cluster
        :param sort_by: type of sort
        :param plot: if 'k' best routes should be shown
        :param sim_matrix: pre-computed similarity matrix
        :param args: additional args
        :param kwargs: additional args
        :return: None
        """
        # Compare based on edge id's using jaccard similarity, (with similarity boundary of 75% or higher)
        print(f"Computing similarity metric, received matrix: {sim_matrix is not None}")
        self.score.clear()
        similarity_matrix: Optional[np.array] = (
            self.create_jaccard_matrix(routes) if sim_matrix is None else sim_matrix
        )
        print(f"Finished computing similarity matrix")
        if similarity_matrix is None:
            print(f"Cannot continue with DBSCAN, error at creating similarity matrix")
            self.score = [i for i in range(len(routes))]
            return
        print(f"Running dbscan")
        reduced_dataset = DBSCAN(metric='precomputed', eps=eps, min_samples=min_samples).fit(
            self.get_jaccard_distance(similarity_matrix)
        )
        if reduced_dataset is None:
            print("Error in DBSCAN")
            return
        print(f"Creating clusters")
        temp_clusters: Dict[int, List[int]] = {
            # cluster_index : [route_index (relative to inputted routes)]
        }
        # Create clusters, assign routes to them
        for index, label in enumerate(reduced_dataset.labels_):
            if label not in temp_clusters:
                temp_clusters[label] = []
            temp_clusters[label].append(index)
        print(f"Sorting by: {sort_by}")
        # ----------------------- Sort -----------------------
        if sort_by in ["average_similarity", "average_dissimilarity"]:
            self.average_similarity_sort(similarity_matrix, temp_clusters, sort_by)
        elif sort_by in ["maximal_similarity", "minimal_similarity"]:
            self.maximal_similarity_sort(similarity_matrix, temp_clusters, sort_by)
        # Plot
        if plot:
            self.plot_ranking(routes, graph)

    # -------------------------------------------- Sort --------------------------------------------

    def average_similarity_sort(self, sim_matrix: np.array, clusters: Dict[int, List[int]], sort_type: str) -> None:
        """
        :param sim_matrix: similarity matrix of routes
        :param clusters: clusters made from routes by DBSCAN
        :param sort_type: either 'average_similarity' or 'average_dissimilarity'
        :return: None
        """
        similarity: bool = ("average_similarity" == sort_type)
        new_clusters: Dict[int, Tuple[float, List[Tuple[float, int]]]] = {
            # cluster_index: (average_similarity of all in-cluster
            # routes, [(average_similarity of this route, route index), ...]),
            # ...
        }
        print(f"Sorting cluster routes by '{sort_type}'")
        # Calculate avg. similarity of routes in clusters and avg. cluster similarity
        for cluster_id, routes_indexes in clusters.items():
            # For each route calculate its similarity compared to other routes in the same cluster
            cluster_size: int = min(len(routes_indexes), 2)  # Minimum 2 beucase we subtract by 1
            average_similarities: List[Tuple[float, int]] = []
            for route_index in routes_indexes:
                average_similarities.append((
                    # Average similarity compared to other
                    # routes (subtract itself -> similarity of 1) / (number of routes -1 -> itself)
                    round((sim_matrix[route_index][routes_indexes].sum() - 1) / (cluster_size - 1), 3),
                    route_index
                ))
            cluster_size = len(routes_indexes)
            new_clusters[cluster_id] = (
                # Average of averages -> cluster average similarity
                round(sum([pair[0] for pair in average_similarities]) / cluster_size, 3),
                # Sort routes by their average similarity (sort in reverse if dissimilarity)
                sorted(average_similarities, key=lambda tup: tup[0], reverse=similarity)
            )
        # Sort clusters by average similarity (in reverse if dissimilarity)
        print(f"Sorting clusters by '{sort_type}'")
        sorted_clusters_ids: list = sorted(
            list(new_clusters.items()), key=lambda tup: tup[1], reverse=similarity
        )
        # Rank routes
        sorted_clusters_ids: List[List[Tuple[float, int]]] = [cluster[1][1] for cluster in sorted_clusters_ids]
        print(f"Sorting routes to final score")
        index: int = 0
        while sorted_clusters_ids:
            if sorted_clusters_ids[index]:  # Pop route index from cluster
                cluster = sorted_clusters_ids[index].pop(0)
                self.score.append(cluster[1])
            else:  # Empty cluster, pop it
                sorted_clusters_ids.pop(index)
            index += 1
            if index >= len(sorted_clusters_ids):
                index = 0
        print(f"Finished sorting routes")

    def maximal_similarity_sort(self, sim_matrix: np.array, clusters: Dict[int, List[int]], sort_type: str) -> None:
        """
        Ranks routes in cluster based on average similarity to all other cluster routes

        :param sim_matrix: similarity matrix of routes
        :param clusters: clusters made from routes by DBSCAN
        :param sort_type: either 'minimal_similarity' or 'maximal_dissimilarity'
        :return:
        """
        ranked_routes: List[List[Tuple[int, float]]] = [[] for _ in clusters.keys()]
        # ranked_routes[cluster] -> [(route_index, similarity compared to other cluster routes), ..]
        print(f"Sorting cluster routes by '{sort_type}'")
        routes_count: int = sim_matrix.shape[0]
        for cluster, routes in clusters.items():
            for route in routes:
                all_sim: float = sim_matrix[route].sum()
                same_sim: float = sim_matrix[route][routes].sum()
                ranked_routes[cluster].append((route, round((all_sim-same_sim) / routes_count, 3)))
            ranked_routes[cluster].sort(key=lambda tup: tup[1], reverse=sort_type == "maximal_similarity")
        # Rank routes
        print(f"Sorting cluster routes by '{sort_type}'")
        index: int = 0
        while ranked_routes:
            if ranked_routes[index]:  # Pop route index from cluster
                cluster = ranked_routes[index].pop(0)
                self.score.append(cluster[0])
            else:  # Empty cluster, pop it
                ranked_routes.pop(index)
            index += 1
            if index >= len(ranked_routes):
                index = 0
        print(f"Finished sorting routes")

    # -------------------------------------------- Jaccard --------------------------------------------

    def get_jaccard_distance(self, matrix: np.array) -> np.array:
        """
        :param matrix: jaccard similarity matrix
        :return: jaccard distance matrix
        """
        return np.ones(matrix.shape) - matrix

    def jaccard_similarity(self, v1: List[int], v2: List[int]) -> float:
        """
        :param v1: list of edge id's
        :param v2: list of edge id's
        :return: jaccard similarity between two sets
        """
        return (len(np.intersect1d(v1, v2)) + 0.0) / len(np.union1d(v1, v2))

    def create_jaccard_matrix(self, routes: List[Route]) -> Optional[np.array]:
        """
        :param routes: list of routes
        :return: array containing similarity between each route (2D symmetric matrix),
        None if number of routes is less than '2'
        """
        print("Computing Jaccard similarity matrix")
        length: int = len(routes)
        if length < 2:
            # print("Cannot create similarity matrix, length of routes list must be at least 2")
            return None
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

    def plot_ranking(self, routes: List[Route], graph: Graph, *args, **kwargs) -> None:
        fig, ax = graph.display.default_plot()
        for index in self.get_score(4):
            route = routes[index]
            ax.clear()
            graph.display.plot_default_graph(ax)
            route.plot(ax, color="blue")
            graph.display.add_label("_", "blue", f"Route: {index}")
            graph.display.make_legend(1)
            plt.tight_layout()
            fig.canvas.draw()
            plt.pause(0.1)
        graph.display.show_plot()

