from utc.src.graph.graph_main import GraphMain, Command, FilePaths
from utc.src.graph.components import Skeleton, Route
from utc.src.plan_qd.metrics import SimilarityMetric, BottleneckMetric
from utc.src.file_system import MyFile
from typing import List, Dict, Tuple, Optional, Union, Any


class PlanQDLauncher(GraphMain):
    """
    Class launching methods for plan quality & diversity testing, extends GraphMain
    """
    def __init__(self, log_commands: bool = True):
        super().__init__(log_commands)
        self.similarity_metric: SimilarityMetric = SimilarityMetric()
        self.bottleneck_metric: BottleneckMetric = BottleneckMetric()
        # Routes used to create graphs
        self.subgraph_routes: Dict[str, List[Route]] = {}
        # Similarity matrices mapped to sub-graphs
        self.subgraph_sim_matrices: Dict[str, Any] = {}

    def initialize_commands(self) -> None:
        super().initialize_commands()
        # Add commands for metrics
        self.user_input.add_command([
            Command("similarity_metric", self.similarity_metric_command),
            Command("bottleneck_metric", self.bottleneck_metric_command)
        ])

    # --------------------------------- Commands ---------------------------------

    def subgraph_command(
            self, subgraph_name: str, graph_name: str, from_junction: str,
            to_junction: str, c: float, plot: bool = False
         ) -> Optional[List[Route]]:
        ret_val = super().subgraph_command(subgraph_name, graph_name, from_junction, to_junction, c, plot)
        if ret_val is not None:
            self.subgraph_routes[subgraph_name] = ret_val
        return ret_val

    def similarity_factory(
            self, sort_by_list: List[str], file_name: str, param_k: Union[int, float]
            ) -> Optional[List[Tuple[bool, str]]]:
        """

        :param sort_by_list:
        :param file_name:
        :param param_k:
        :return:
        """

        print(f"Creating subgraph for similarity_metric ({sort_by_list}), k: {param_k}")
        if not self.subgraph_sim_matrices:
            print(f"Preparing sub_graph similarity matrices for all graphs")
            for index, (sub_graph_name, routes) in enumerate(self.subgraph_routes.items()):
                self.subgraph_sim_matrices[sub_graph_name] = self.similarity_metric.create_jaccard_matrix(routes)
                print(f"Finished computing similarity matrix: {index+1}/{len(self.subgraph_routes)}")
                print(f"Success: {self.subgraph_sim_matrices[sub_graph_name] is not None}")
            print(f"Finished computing similarity matrices")
        ret_val: Optional[List[Tuple[bool, str]]] = []
        # Create sub-graphs
        for sort_by in sort_by_list:
            curr_file_name = file_name.replace("_default", "_similarity_" + sort_by)
            # For each subgraph
            for i, subgraph in enumerate(self.subgraph_routes):
                print(f"Creating subgraph for {sort_by}, from: {subgraph}")
                self.graph.set_skeleton(self.graphs[subgraph])
                self.similarity_metric.calculate(
                    self.subgraph_routes[subgraph], self.graph,
                    sort_by=sort_by, sim_matrix=self.subgraph_sim_matrices[subgraph]
                )
                # TODO consider multiple "k" params
                ranking: List[int] = self.similarity_metric.get_score(param_k)
                if not ranking:
                    print(f"Invalid ranking, could not create subgraph ...")
                    return
                sub_graph: Skeleton = self.graph.sub_graph.create_sub_graph(
                    [self.subgraph_routes[subgraph][index] for index in ranking]
                )
                if sub_graph is None:
                    print("Could not create subgraph")
                    return None
                self.graphs[f"msg{i}"] = sub_graph
                print(f"Finished creating {sort_by} sub-graph: {i+1}/{len(self.subgraph_routes)}")
            # Merge
            for i in range(1, len(self.subgraph_routes)):
                self.merge_command(f"msg0", f"msg0", f"msg{i}")
            # Save
            self.save_graph_command("msg0", curr_file_name)
            # Remove
            for i in range(len(self.subgraph_routes)):
                self.graphs.pop(f"msg{i}", None)
            print(f"Finished creating subgraph for similarity_metric_{sort_by}: {curr_file_name}")
            ret_val.append((MyFile.file_exists(FilePaths.NETWORK_SUMO_MAPS.format(curr_file_name)), curr_file_name))
        self.subgraph_sim_matrices = None
        return ret_val

    def bottleneck_factory(self, file_name: str, k: float) -> Tuple[bool, str]:
        """

        :param file_name:
        :param k:
        :return:
        """
        print(f"Creating sub-graph for bottle_neck metric, k: {k}")
        file_name = file_name.replace("_default", "_bottleneck")
        # Create sub-graphs
        for i, subgraph in enumerate(self.subgraph_routes.keys()):
            self.bottleneck_metric_command(f"msg{i}", subgraph, k)
        # Merge
        for i in range(1, len(self.subgraph_routes.keys())):
            self.merge_command("msg0", "msg0", f"msg{i}")
        # Save
        self.save_graph_command("msg0", file_name)
        # Remove
        for i in range(len(self.subgraph_routes.keys())):
            self.graphs.pop(f"msg{i}")
        return MyFile.file_exists(FilePaths.NETWORK_SUMO_MAPS.format(file_name)), file_name

    @GraphMain.log_command
    def similarity_metric_command(
            self, new_subgraph: str, subgraph: str, k: float, eps: float = 0.26,
            min_samples: int = 4, order_by: str = "average_similarity", plot: bool = False
            ) -> None:
        """
        Cluster routes based on similarity, uses
        'order_by' parameter to sort them (from best to worst),
        sorted list is then used to construct new subgraph

        :param new_subgraph: name of newly created subgraph by metric
        :param subgraph: name created by 'sub_graph' command
        :param k: number of best routes to pick (if float, used as percentage)
        :param eps: minimal similarity between two routes for them to be added into same cluster
        :param min_samples: minimal amount of routes similar enough to be considered cluster
        :param order_by: method to use to order clusters by
        :param plot:
        :return: None
        """
        if not self.graph_exists(subgraph):
            return
        elif subgraph not in self.subgraph_routes:
            print(f"Missing subgraph: {subgraph} logged in subgraph routes!")
            return
        self.graph.set_skeleton(self.graphs[subgraph])
        self.similarity_metric.calculate(
            self.subgraph_routes[subgraph], self.graph, eps,
            min_samples, order_by, plot
        )
        ranking: List[int] = self.similarity_metric.get_score(k)
        if not ranking:
            print(f"Invalid ranking, could not create subgraph ...")
            return
        sub_graph: Skeleton = self.graph.sub_graph.create_sub_graph(
            [self.subgraph_routes[subgraph][index] for index in ranking]
        )
        if sub_graph is None:
            print("Could not create subgraph")
            return None
        self.graphs[new_subgraph] = sub_graph
        print(f"Finished creating sub-graph: {new_subgraph}")

    @GraphMain.log_command
    def bottleneck_metric_command(self, new_subgraph: str, subgraph: str, k: float, plot: bool = False) -> None:
        """
        :param new_subgraph: name of newly created subgraph by metric
        :param subgraph: name created by 'sub_graph' command
        :param k: number of best routes to pick (if float, used as percentage)
        :param plot:
        :return: None
        """
        if not self.graph_exists(subgraph) or subgraph not in self.subgraph_routes:
            return
        self.graph.set_skeleton(self.graphs[subgraph])
        self.bottleneck_metric.calculate(
            self.subgraph_routes[subgraph], self.graph, plot
        )
        ranking: List[int] = self.bottleneck_metric.get_score(k)
        # print(f"Ranking: {ranking}")
        if not ranking:
            print(f"Invalid ranking, could not create subgraph ...")
            return
        sub_graph: Skeleton = self.graph.sub_graph.create_sub_graph(
            [self.subgraph_routes[subgraph][index] for index in ranking]
        )
        if sub_graph is None:
            print("Could not create subgraph")
            return None
        self.graphs[new_subgraph] = sub_graph
        print(f"Finished creating sub-graph: {new_subgraph}")


if __name__ == "__main__":
    temp: PlanQDLauncher = PlanQDLauncher()
    temp.run()
