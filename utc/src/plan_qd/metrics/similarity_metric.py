from utc.src.graph.components import Route, Graph
from utc.src.plan_qd.metrics.metric import Metric
from utc.src.utils import check_process_count
from typing import List, Dict, Tuple, Optional, Union, Any
import numpy as np
from sklearn.cluster import DBSCAN
from multiprocessing import Pool


class SimilarityMetric(Metric):
    """
    Class clustering routes based on similarity,
    ordering routes based on diversity among clusters
    """

    def __init__(self):
        super().__init__("SimilarityMetric")

    def calculate(
            self, routes: List[Route], graph: Graph = None,
            eps: float = 0.26, min_samples: int = 4,
            sort_by: str = "", plot: bool = False,
            sim_matrix: np.array = None,
            reduced_dataset=None,
            k: Union[int, float, None] = None,
            *args, **kwargs
            ) -> Optional[List[int]]:
        """
        :param routes: to be ranked by algorithm
        :param graph: from which routes were extracted (default None)
        :param eps: minimal similarity between two routes for them to be added into same cluster
        :param min_samples: minimal amount of routes similar enough to be considered cluster
        :param sort_by: type of sort
        :param plot: if 'k' best routes should be shown
        :param sim_matrix: pre-computed similarity matrix
        :param reduced_dataset: pre-compute result of DBSCAN
        :param k: number of best routes to be picked, if None
        only one best per cluster gets picked
        :param args: additional args
        :param kwargs: additional args
        :return: list of sorted route indexes, None if error occurred
        """
        # Can be pre-computed
        if sim_matrix is None:
            sim_matrix = self.create_jaccard_matrix(routes)
        # Check matrix
        if sim_matrix is None:
            print(f"Cannot continue with DBSCAN, error at creating similarity matrix")
            return None
        # Can be pre-computed
        if reduced_dataset is None:
            print(f"Running DBSCAN")
            reduced_dataset = self.run_dbscan(sim_matrix, eps, min_samples)
        # Check data set
        if reduced_dataset is None:
            print("Output of dbscan is of type 'None', cannot continue !")
            return None
        # ----------------------- Sort -----------------------
        return self.pick_best(sim_matrix, self.cluster_routes(reduced_dataset), sort_by, self.convert_k(k, len(routes)))

    # noinspection PyMethodMayBeStatic
    def run_dbscan(
            self, similarity_matrix: np.array,
            eps: float = 0.26, min_samples: int = 4
            ) -> Optional[Any]:
        """
        :param similarity_matrix: similarity matrix of routes
        :param eps: minimal similarity between two routes for them to be added into same cluster
        :param min_samples: minimal amount of routes similar enough to be considered cluster
        :return: list of labels, None if arguments are invalid
        """
        if similarity_matrix is None:
            print(f"Invalid similarity matrix and/or routes received, cannot run DBSCAN!")
            return None
        elif similarity_matrix.shape[0] != similarity_matrix.shape[1]:
            print(f"Expected similarity matrix to be of the same size, got: {similarity_matrix.shape} !")
            return None
        return (
            DBSCAN(metric='precomputed', eps=eps, min_samples=min_samples).fit(
                self.get_jaccard_distance(similarity_matrix)
            )
        )

    # -------------------------------------------- Sort --------------------------------------------

    def pick_best(
            self, sim_matrix: np.array, clusters: Dict[int, List[int]],
            sort_type: str, k: int = None
            ) -> List[int]:
        """
        Picks best routes depending on k

        :param sim_matrix: similarity matrix of routes
        :param clusters: clusters made from routes by DBSCAN
        :param sort_type: one of: 'average_similarity', 'average_dissimilarity',
        'shortest_path', 'minimal_similarity', 'maximal_dissimilarity'
        :param k: number of best routes to be picked, if None
        only one best per cluster gets picked
        :return: list of routed indexes
        """
        print(f"Sorting cluster routes by '{sort_type}'")
        sorted_clusters: List[List[int]] = [
            # position of inner list acst as cluster id (-1 is on position 0, 0 on 1st, etc..)
            # values are route indexes (sorted)
        ]
        if sort_type in {"average_similarity", "average_dissimilarity"}:
            sorted_clusters = self.average_similarity_sort(sim_matrix, clusters, sort_type)
        elif sort_type in {"minimal_similarity", "maximal_similarity"}:
            sorted_clusters = self.maximal_similarity_sort(sim_matrix, clusters, sort_type)
        elif sort_type in {"shortest_length"}:
            sorted_clusters = self.length_sort(clusters)
        print(f"Sorting routes to final score")
        # Pick only one route (best) per cluster
        if k is None:
            return [route_indexes[0] for route_indexes in sorted_clusters]
        # If we want to pick all routes, pick best each iteration in one cluster,
        # until all are empty (this makes it so, that all clusters routes are represented)
        ret_val: List[int] = []
        index: int = 0
        while sorted_clusters:
            if sorted_clusters[index]:  # Pop route index from cluster
                ret_val.append(sorted_clusters[index].pop(0))
            else:  # Empty cluster, pop it
                sorted_clusters.pop(index)
            index += 1
            if index >= len(sorted_clusters):
                index = 0
        print(f"Finished sorting routes")
        return ret_val[0:min(len(ret_val), k)]

    # noinspection PyMethodMayBeStatic
    def average_similarity_sort(
            self, sim_matrix: np.array,
            clusters: Dict[int, List[int]], sort_type: str
            ) -> List[List[int]]:
        """
        Sorts routes based on intra-cluster average similarity,
        sorts clusters based on their routes averages

        :param sim_matrix: similarity matrix of routes
        :param clusters: clusters made from routes by DBSCAN
        :param sort_type: either 'average_similarity' or 'average_dissimilarity'
        :return: Sorted list of clusters containing indexes of their routes (also sorted)
        """
        similarity: bool = ("average_similarity" == sort_type)
        new_clusters: Dict[int, Tuple[float, List[Tuple[float, int]]]] = {
            # cluster_index: (average_similarity of all in-cluster
            # routes, [(average_similarity of this route, route index), ...]),
            # ...
        }
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
        sorted_clusters_ids: list = sorted(
            list(new_clusters.items()), key=lambda tup: tup[1], reverse=similarity
        )
        # Return sorted routes
        return [[tup[1] for tup in lst] for lst in [cluster[1][1] for cluster in sorted_clusters_ids]]

    # noinspection PyMethodMayBeStatic
    def maximal_similarity_sort(
            self, sim_matrix: np.array,
            clusters: Dict[int, List[int]], sort_type: str
            ) -> List[List[int]]:
        """
        Ranks routes in cluster based on average similarity to all other cluster routes

        :param sim_matrix: similarity matrix of routes
        :param clusters: clusters made from routes by DBSCAN
        :param sort_type: either 'minimal_similarity' or 'maximal_similarity'
        :return: Sorted list of clusters containing indexes of their routes (also sorted)
        """
        ranked_routes: List[List[Tuple[float, int]]] = [[] for _ in clusters.keys()]
        # ranked_routes[cluster] -> [(similarity compared to other cluster routes, route_index), ..]
        routes_count: int = sim_matrix.shape[0]
        for cluster, routes in clusters.items():
            for route in routes:
                all_sim: float = sim_matrix[route].sum()
                same_sim: float = sim_matrix[route][routes].sum()
                ranked_routes[cluster].append((round((all_sim-same_sim) / routes_count, 3), route))
            ranked_routes[cluster].sort(key=lambda tup: tup[0], reverse=(sort_type == "maximal_similarity"))
        # Return sorted routes
        return [[tup[1] for tup in cluster] for cluster in ranked_routes]

    # noinspection PyMethodMayBeStatic
    def length_sort(
            self, clusters: Dict[int, List[int]],
            ) -> List[List[int]]:
        """
        Sorts routes from clusters based on shortest length inside cluster,
        since we used TopK_A* to create routes, they are already sorted

        :param clusters: clusters made from routes by DBSCAN
        :return: Routes sorted from clusters by length
        """
        # Return sorted routes
        return [cluster_routes for cluster_routes in clusters.values()]

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

    def create_jaccard_matrix_parallel(self, routes: List[Route], processes: int = 1) -> Optional[np.array]:
        """
        :param routes: list of routes
        :param processes: number of processes to be run on matrix creation
        (advantageous for larger amount of routes)
        :return: array containing similarity between each route (2D symmetric matrix),
        None if number of routes is less than '2'
        """
        print(f"Computing Jaccard similarity matrix with {processes} processes")
        # This has to be done to pickle 'create_matrix_row', multiprocessing throws error otherwise
        global create_matrix_row
        # -------------- Check args --------------
        length: int = len(routes)
        if length < 2:
            print("Cannot create similarity matrix, length of routes list must be at least 2")
            return None
        elif not check_process_count(processes):
            print(f"Limiting processes to 1 from: {processes}")
            processes = 1
        elif processes > 1 and len(routes) < 500:
            print(f"Limiting threads: '{processes}' to 1, because amount of routes is: {len(routes)} < 500")
            processes = 1

        # Single thread
        if processes == 1:
            print(f"Computing matrix on single process")
            if "create_matrix_row" in globals():
                del globals()['create_matrix_row']
            return self.create_jaccard_matrix(routes)

        def create_matrix_row(row: int, size: int) -> List[float]:
            """
            Creates row for similarity matrix, used
            for parallel processing

            :param row: index of matrix row
            :param size: size of matrix
            :return: matrix row of similarity values
            """
            return [
                self.jaccard_similarity(routes[row].get_edge_ids(as_int=True), routes[col].get_edge_ids(as_int=True))
                for col in range(row+1, size)
            ]

        # Create pool
        print(f"Starting process pool with: {processes} processes")
        pool: Pool = Pool(processes=processes)
        # -1, since we want to skip diagonal (route has similarity of "1" to itself)
        results = [pool.apply_async(create_matrix_row, [row, length]) for row in range(length-1)]
        pool.close()
        pool.join()
        # Generate matrix
        jaccard_matrix: np.array = np.zeros([length, length])
        for idx in range(len(results)):
            jaccard_matrix[idx][idx + 1:length] = results.pop(0).get()
        if "create_matrix_row" in globals():
            del globals()['create_matrix_row']
        return jaccard_matrix + jaccard_matrix.T + np.identity(length)

    # -------------------------------------------- Utils --------------------------------------------

    def plot_ranking(self, routes: List[Route], graph: Graph, *args, **kwargs) -> None:
        pass

    # noinspection PyMethodMayBeStatic
    def cluster_routes(self, labels) -> Optional[Dict[int, List[int]]]:
        """
        :param labels: computed by DBSCAN
        :return: mapping of cluster id to routes indexes, None if
        error occurred
        """
        if labels is None:
            print(f"Cannot cluster routes from labels of type 'None'")
            return None
        temp_clusters: Dict[int, List[int]] = {
            # cluster_index : [route_index (relative to inputted routes)]
        }
        # Create clusters, assign routes to them
        for index, label in enumerate(labels.labels_):
            if label not in temp_clusters:
                temp_clusters[label] = []
            temp_clusters[label].append(index)
        return temp_clusters

