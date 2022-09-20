from utc.src.graph.components import Skeleton, Graph, Route
from utc.src.plan_qd.metrics import SimilarityMetric, BottleneckMetric, RoutesStruct
from utc.src.plan_qd.factories import FlowFactory, GraphFactory, ScenarioFactory
from utc.src.file_system import MyFile, InfoFile, FilePaths, ProbabilityFile
from utc.src.ui import UserInterface
from typing import List, Dict, Tuple


class PlanQDLauncher(UserInterface):
    """
    Class launching methods for plan quality & diversity testing
    """
    def __init__(self):
        super().__init__("user_interface")
        self.routes_struct: RoutesStruct = None
        self.similarity_metric: SimilarityMetric = SimilarityMetric()
        self.bottleneck_metric: BottleneckMetric = BottleneckMetric()
        # Factories
        self.flow_factory: FlowFactory = FlowFactory()
        self.graph_factory: GraphFactory = GraphFactory()
        self.scenario_factory: ScenarioFactory = ScenarioFactory()
        self.graphs: Dict[str, Skeleton] = {}
        self.info_file = InfoFile("")

    def initialize_commands(self) -> None:
        super().initialize_commands()


if __name__ == "__main__":
    scenario_name: str = "dejvice_test"
    network_name: str = "Dejvice"
    probability_file: str = "dejvice"
    # Scenario
    # scenario_factory: ScenarioFactory = ScenarioFactory()
    # scenario_factory.initialize(scenario_name, network_name)
    # Graph
    graph_factory: GraphFactory = GraphFactory()
    graph_factory.initialize(network_name)
    # Flows
    flow_factory: FlowFactory = FlowFactory(
        Graph(graph_factory.graph_main.graphs[network_name]),
        ProbabilityFile(probability_file)
    )
    flows: List[Tuple[str, str]] = flow_factory.generate_flows(0, 0, 300)

    # scenario_factory.add_flows(flows)
    # Create scenario

    # Create sub-graph
    similarity_metric: SimilarityMetric = SimilarityMetric()
    bottleneck_metric: BottleneckMetric = BottleneckMetric()
    graph: Graph = Graph(graph_factory.graph_main.graphs[network_name])
    for index, (flow_name, flow_args) in enumerate(flows):
        curr_args: Dict[str, str] = {
            i.split("=")[0]: i.split("=")[1] for i in flow_args.replace("\"", "").split()
        }
        print(flow_name, curr_args)
        graph_factory.generate_sub_graph(
            f"sg{index}", network_name, curr_args["from_junction_id"],
            curr_args["to_junction_id"], 1.5, "f"
        )
        routes: List[Route] = graph_factory.graph_main.current_ret_val
        if routes is None:
            print(f"Routes is of type: 'None'")
            break
        print(f"Found: {len(routes)} routes for sub-graph: {index}")
        routes_struct: RoutesStruct = RoutesStruct(routes, graph)
        similarity_metric.calculate(routes_struct, sort_by="average")
        print(f"Creating sub-graph from: {len([routes[i] for i in similarity_metric.get_score(0.5)])}")
        graph_factory.graph_main.graphs[f"msg{index}"] = graph.sub_graph.create_sub_graph(
            [routes[i] for i in similarity_metric.get_score(0.35)]
        )
        if graph_factory.graph_main.graphs[f"msg{index}"] is None:
            print(f"Error when generating subgraph")
            exit(0)
        similarity_metric.clear()
        # bottleneck_metric.calculate(routes_struct)
        # Take routes from generated sub-graph, pass it to Metrics

    for i in range(1, len(flows)):
        graph_factory.merge_command(
           "msg0", f"msg0", f"msg{i}", "f"
        )
        # Delete subgraph ?
    graph_factory.graph_main.process_input(
        "save-graph", f'graph_name="msg0" file_name="{scenario_name}_similarity_subgraph"'
    )

"""
uniform-flow ['from_junction_id', '"83" to_junction_id', '"73" vehicle_count', '"65" start_time', '"0" end_time', '"300"']
random-flow ['from_junction_id', '"15" to_junction_id', '"73" minimal', '"1" maximal', '"3" period', '"20" start_time', '"0" end_time', '"300"']
uniform-flow ['from_junction_id', '"70" to_junction_id', '"73" vehicle_count', '"63" start_time', '"0" end_time', '"300"']
exponential-flow ['from_junction_id', '"69" to_junction_id', '"15" start_time', '"0" end_time', '"300" mode', '"random"']
exponential-flow ['from_junction_id', '"78" to_junction_id', '"8" start_time', '"0" end_time', '"300" mode', '"random"']
"""
