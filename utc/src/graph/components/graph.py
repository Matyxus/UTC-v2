from utc.src.graph.components.skeleton import Skeleton
from utc.src.graph.modules import Loader, Simplify, ShortestPath, Display, SubGraph


class Graph:
    """ Class holding skeleton of graph and all graph modules """

    def __init__(self, skeleton: Skeleton = None):
        self.skeleton: Skeleton = skeleton
        self.loader: Loader = Loader(self.skeleton)
        self.simplify: Simplify = Simplify(self.skeleton)
        self.shortest_path: ShortestPath = ShortestPath(self.skeleton)
        self.display: Display = Display(self.skeleton)
        self.sub_graph: SubGraph = SubGraph(self.skeleton)

    def set_skeleton(self, skeleton: Skeleton) -> None:
        """
        :param skeleton: to be set for graph modules
        :return: None
        """
        self.skeleton = skeleton
        self.loader.set_skeleton(skeleton)
        self.simplify.set_skeleton(skeleton)
        self.shortest_path.set_skeleton(skeleton)
        self.display.set_skeleton(skeleton)
        self.sub_graph.set_skeleton(skeleton)
