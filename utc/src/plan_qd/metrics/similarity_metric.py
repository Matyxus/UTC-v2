from utc.src.graph.components import Route
from typing import List, Dict
import numpy as np
import kmedoids
from sklearn.cluster import DBSCAN
from pyclustering.cluster import cluster_visualizer_multidim
from pyclustering.cluster.optics import optics, ordering_analyser, ordering_visualizer


class SimilarityMetric:
    """
    Class containing methods which rank routes based on parameters
    """

    def __init__(self):
        print("Initializing SimilarityMetric class")

    def rank(self, routes: List[Route], k: int) -> Dict[int, List[Route]]:
        """
        :param routes: list of routes
        :param k: number of medoids
        :return: dictionary mapping index of route to its group of Routes (including itself)
        """
        ret_val: Dict[int, List[Route]] = {}
        similarity_matrix: np.array = self.create_similarity_matrix(routes)
        if not len(similarity_matrix):
            return ret_val
        result: kmedoids.KMedoidsResult = self.create_medoids(similarity_matrix, k)
        if result is None:
            return ret_val
        # Initialize array
        ret_val = {medoid: [] for medoid in result.medoids}
        # Append routes
        print(ret_val)
        print(result)
        for index, route in enumerate(routes):
            ret_val[result.medoids[result.labels[index]]].append(route)
        return ret_val

    def jaccard(self, v1: List[int], v2: List[int]) -> float:
        """

        :param v1: list of edge id's
        :param v2: list of edge id's
        :return: jaccard distance
        """
        return 1 - (len(np.intersect1d(v1, v2)) + 0.0) / len(np.union1d(v1, v2))

    def create_similarity_matrix(self, routes: List[Route]) -> np.array:
        """
        :param routes: List of routes
        :return: Array containing similarity between each route (2D symmetric matrix)
        """
        print("Computing similarity matrix")
        length: int = len(routes)
        if length < 2:
            print("Cannot create similarity matrix, length of routes list must be at least 2")
            return np.array([[]])
        similarity_matrix: np.array = np.zeros([length, length])
        # -1, since we want to skip diagonal (route has similarity of "1" to itself)
        for i in range(length-1):
            for j in range(i+1, length):
                similarity_matrix[i, j] = self.jaccard(
                    routes[i].get_edge_ids(as_int=True), routes[j].get_edge_ids(as_int=True)
                )
        print("Finished computing similarity matrix")
        return similarity_matrix + similarity_matrix.T  # + np.identity(length)

    def pretty_print(self, similarity_matrix: np.array):
        for row in similarity_matrix:
            for col in row:
                print("{:8.3f}".format(col).lstrip(), end="  ")
            print("")

    def create_medoids(self, similarity_matrix: np.array, k: int) -> kmedoids.KMedoidsResult:
        """
        :param k:
        :param similarity_matrix:
        :return: Array containing similarity between each route (2D symmetric matrix)
        """
        return kmedoids.fasterpam(similarity_matrix, k)

    def create_optics(self, routes: List[Route]) -> List[List[Route]]:
        """

        :param routes:
        :return:
        """
        similarity_matrix = self.create_similarity_matrix(routes)
        # Run cluster analysis where connectivity radius is bigger than real
        radius = 2.0
        neighbors = 5
        amount_of_clusters = 5
        optics_instance = optics(similarity_matrix, radius, neighbors, amount_of_clusters)

        # Performs cluster analysis
        optics_instance.process()

        # Obtain results of clustering
        clusters = optics_instance.get_clusters()
        noise = optics_instance.get_noise()
        ordering = optics_instance.get_ordering()
        print(f"Clusters: {clusters}")
        print(f"Ordering: {ordering}")
        return [[routes[index] for index in cluster] for cluster in clusters]

    def create_dbscan(self, routes: List[Route]) -> List[List[Route]]:
        """
        :param routes:
        :return:
        """
        self.pretty_print(self.create_similarity_matrix(routes))
        reduced_dataset = DBSCAN(metric='precomputed', eps=0.26, min_samples=4).fit(
            self.create_similarity_matrix(routes)
        )
        label_map: Dict[int, List[Route]] = {}
        print(reduced_dataset.labels_)
        for index, label in enumerate(reduced_dataset.labels_):
            if label not in label_map:
                label_map[label] = []
            label_map[label].append(routes[index])
        return [route_list for route_list in label_map.values()]

