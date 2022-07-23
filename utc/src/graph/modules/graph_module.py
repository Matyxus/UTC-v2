from utc.src.graph.components import Skeleton


class GraphModule:
    """ Super class for classes which modify graph """

    def __init__(self, skeleton: Skeleton = None):
        self.skeleton: Skeleton = skeleton

    def set_skeleton(self, skeleton: Skeleton) -> None:
        """
        Setter for graph, has to be called for each
        child class before using their methods

        :param skeleton: of graph
        :return: None
        """
        self.skeleton = skeleton
        assert (self.skeleton is not None)

    def get_skeleton(self) -> Skeleton:
        """

        :return: current skeleton of graph, may be None
        """
        return self.skeleton
