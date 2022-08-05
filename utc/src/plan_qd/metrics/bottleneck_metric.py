from utc.src.plan_qd.metrics.metric import Metric
from utc.src.graph.components import Route, Graph
from typing import List, Dict


class BottleneckMetric(Metric):
    """
    Class finding bottleneck junctions in routes
    (bottleneck junction is junction which
    has many routes passing trough it
    from many different directions),
    and penalizing routes passing trough such junctions
    """
    def __init__(self):
        super().__init__("BottleneckMetric")
        self.bottlenecks: Dict[str, Dict[str, List[str]]] = {
            # junction_id : { incoming_edge : [route_id ? -> number of occurrences]
            #
            # }
        }

    def calculate(self, routes: List[Route], *args, **kwargs) -> None:
        """
        :param routes: list of routes to be ordered based on current metric
        :param args: additional args
        :param kwargs: additional args
        :return: None
        """
        # Find bottlenecks
        for route in routes:
            for edge in route.edge_list:
                junction_id: str = edge.attributes["to"]
                edge_id: str = edge.attributes["id"]
                if junction_id not in self.bottlenecks:
                    self.bottlenecks[junction_id] = {}
                if edge_id not in self.bottlenecks[junction_id]:
                    self.bottlenecks[junction_id][edge_id] = []
                self.bottlenecks[junction_id][edge_id].append(route.attributes["id"])
        # Remove bottlenecks, which are unavoidable (all routes pass trough them)
        for junction_id in list(self.bottlenecks.keys()):
            # Junction has only one unique incoming edge
            if len(self.bottlenecks[junction_id].keys()) == 1:
                # edge_id = next(iter(self.bottlenecks[junction_id]))
                del self.bottlenecks[junction_id]
        for junction_id in self.bottlenecks.keys():
            print(f"Junction: {junction_id}")
            for edge_id in self.bottlenecks[junction_id].keys():
                print(f"From edge: {edge_id}, incoming routes: {len(self.bottlenecks[junction_id][edge_id])}")
        print(self.bottlenecks)

    def show_bottlenecks(self, graph: Graph) -> None:
        """
        :param graph:
        :return:
        """
        fig, ax = graph.display.default_plot()
        for junction_id in self.bottlenecks:
            graph.skeleton.junctions[junction_id].plot(ax, color="red")
        graph.display.show_plot()
