from utc.src.plan_qd.metrics.metric import Metric
from utc.src.plan_qd.metrics.routes_struct import RoutesStruct
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
        self.bottlenecks: Dict[str, Dict[str, List[int]]] = {
            # junction_id : { incoming_edge : [route_id ? -> number of occurrences]
            #
            # }
        }

    def calculate(self, routes_struct: RoutesStruct, *args, **kwargs) -> None:
        """
        :param routes_struct:
        :param args: additional args
        :param kwargs: additional args
        :return: None
        """
        # Find bottlenecks
        for index, route in enumerate(routes_struct.routes):
            for edge in route.edge_list:
                junction_id: str = edge.get_attribute("to")
                edge_id: str = edge.get_id()
                if junction_id not in self.bottlenecks:
                    self.bottlenecks[junction_id] = {}
                if edge_id not in self.bottlenecks[junction_id]:
                    self.bottlenecks[junction_id][edge_id] = []
                self.bottlenecks[junction_id][edge_id].append(index)
        # Remove bottlenecks, which are unavoidable (all routes pass trough them)
        for junction_id in list(self.bottlenecks.keys()):
            # Junction has only one unique incoming edge
            if len(self.bottlenecks[junction_id].keys()) == 1:
                del self.bottlenecks[junction_id]
        # print
        for junction_id in self.bottlenecks.keys():
            print(f"Junction: {junction_id}")
            for edge_id in self.bottlenecks[junction_id].keys():
                print(f"From edge: {edge_id}, incoming routes: {len(self.bottlenecks[junction_id][edge_id])}")
        # penalize


    def plot_ranking(self, routes_struct: RoutesStruct, *args, **kwargs) -> None:
        pass
