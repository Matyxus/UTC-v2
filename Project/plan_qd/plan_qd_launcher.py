from Project.UI import UserInterface
from Project.Simplify.components import Skeleton, Graph


class PlanQDLauncher(UserInterface):
    """
    Class launching methods for plan quality & diversity testing
    """
    def __init__(self):
        super().__init__()
        self.original: Graph = None
        self.improved: Graph = None

    def initialite_graphs(self, network_name: str) -> None:
        """
        :param network_name:
        :return:
        """
        #
        self.original = Graph(Skeleton())
        self.original.loader.load_map(network_name)
        self.original.simplify.simplify_graph()
        #
        self.improved = Graph(Skeleton())
        self.improved.loader.load_map(network_name)
        self.improved.simplify.simplify_graph()







if __name__ == "__main__":
    temp: PlanQDLauncher = PlanQDLauncher()
