from Project.Simplify.Components.skeleton import Skeleton
from Project.Simplify.Graph_modules import Loader, Simplify, ShortestPath, Display


class Graph:
    """ Class holding skeleton of graph and all graph modules """
    def __init__(self):
        self.skeleton: Skeleton = Skeleton()
        self.loader: Loader = Loader()
        self.loader.set_skeleton(self.skeleton)
        self.simplify: Simplify = Simplify()
        self.simplify.set_skeleton(self.skeleton)
        self.shortest_path: ShortestPath = ShortestPath()
        self.shortest_path.set_skeleton(self.skeleton)
        self.display: Display = Display()
        self.display.set_skeleton(self.skeleton)


if __name__ == "__main__":
    print("works")
