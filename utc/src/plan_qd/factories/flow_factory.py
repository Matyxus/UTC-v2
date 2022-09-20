from utc.src.graph.components import Skeleton, Graph, Route
from utc.src.file_system import MyFile, InfoFile, FilePaths, ProbabilityFile
from numpy.random import choice, seed
from typing import Dict, Tuple, List, Set, Optional


class FlowFactory:
    """

    """
    def __init__(self, graph: Graph, prob_file: ProbabilityFile):
        self.graph: Graph = graph
        seed(42)
        # Flows and their arguments, format strings
        self.flows: List[Tuple[str, str]] = [
            (
                "random-flow",
                'from_junction_id="{0}" to_junction_id="{1}" '
                'minimal="{2}" maximal="{3}" period="{4}" '
                'start_time="{5}" end_time="{6}"'
            ),
            (
                "uniform-flow",
                'from_junction_id="{0}" to_junction_id="{1}" '
                'vehicle_count="{2}" '
                'start_time="{3}" end_time="{4}"'
            ),
            (
                "exponential-flow",
                'from_junction_id="{0}" to_junction_id="{1}" '
                'start_time="{2}" end_time="{3}" '
                'mode="{4}"'

            )
        ]
        # Probability matrix of flows
        self.prob_matrix: Dict[str, Dict[str, int]] = prob_file.read_file()
        self.flow_range: Tuple[int, int] = (2, 8)  # Min, Max amount of flows
        self.junctions: Set[str] = set()  # Junctions of currently selected flows
        self.routes: Dict[str, Dict[str, Route]] = {
            # from_junction : {to_junction : Route, ...}, ..
        }
        # Maximal amount of tries to choose destination junction
        self.max_tries: int = 20

    def generate_flows(self, amount: int, start_time: int, end_time: int) -> List[Tuple[str, str]]:
        """

        :param amount: number of flows to be generated
        :param start_time: starting time of flows
        :param end_time: ending time of flows
        :return: List of tuples (flow_type, flow_arguments) in
        format passed from command line
        """
        if not self.check_prob_matrix():
            return []

        def generate_flow(path: Tuple[str, str], time_interval: Tuple[int, int]) -> Tuple[str, str]:
            """
            :param path: tuple (from_junction, to_junction)
            :param time_interval: tuple (starting_time, ending_time)
            :param flow_type: type of flow
            :return: arguments (in command line input format)
            """
            flow: Tuple[str, str] = self.flows[choice(range(len(self.flows)))]
            flow_type: str = flow[0]
            formatted_args: str = flow[1]
            if flow_type == "random-flow":
                formatted_args = formatted_args.format(
                    *[*path, *sorted(choice(range(0, 15), size=2)), 20, *time_interval]
                )
            elif flow_type == "uniform-flow":
                duration: int = end_time-start_time
                formatted_args = formatted_args.format(
                    *[*path, choice(range(duration//7, duration//3)), *time_interval]
                )
            elif flow_type == "exponential-flow":
                formatted_args = formatted_args.format(*[*path, *time_interval, "random"])
            return flow_type, formatted_args

        # Random assigned
        if amount == 0:
            amount = choice(range(*self.flow_range))
        ret_val: List[Tuple[str, str]] = []
        for route in self.generate_paths(amount):
            ret_val.append(generate_flow(
                (route.get_start(), route.get_destination()),
                (start_time, end_time)
            ))
        return ret_val

    def generate_paths(self, amount: int) -> List[Route]:
        """
        Generates routes which all have
        at least one 'conflict' with another,
        uses probability matrix from '.prob' file to
        perform weighted random choice between starting and
        ending junctions of routes

        :param amount: number of routes to be generated
        :return: list of routes
        """
        if amount < 1:
            print(f"Amount has to be at least '1', got: '{amount}'")
            return []
        # ------------- Init -------------
        routes: List[Route] = []
        starting_junctions: List[str] = list(self.prob_matrix.keys())
        probabilities: Dict[str, List[float]] = {
            # from_junction : [chance to pick, .... ]
        }
        for junction_id in starting_junctions:
            prob_sum: int = sum([i for i in self.prob_matrix[junction_id].values()])
            probabilities[junction_id] = [prob/prob_sum for prob in self.prob_matrix[junction_id].values()]
        # Junctions of currently found paths
        discovered: Set[str] = set()

        def generate_path() -> Optional[Route]:
            """
            Generates single route which has
            conflict with previously found routes

            :return: Route, or None if route could not have been found
            """
            route: Optional[Route] = None
            # Choose random starting junction (try only certain amount of times
            for starting_junction in choice(starting_junctions, size=self.max_tries):
                # print(f"Starting search from: {starting_junction}")
                # Flow already exists from this junction
                if starting_junction in self.routes:
                    continue
                self.routes[starting_junction] = {}
                to_junctions: List[str] = list(self.prob_matrix[starting_junction].keys())
                # Choose random ending junction (try only certain amount of times)
                for to_junction in choice(to_junctions, p=probabilities[starting_junction], size=self.max_tries):
                    # print(f"Considering: {to_junction}")
                    # Already explored
                    if to_junction in self.routes[starting_junction]:
                        continue
                    route = self.graph.shortest_path.a_star(starting_junction, to_junction)[1]
                    self.routes[starting_junction][to_junction] = route
                    # No path or no "conflict" found between junctions of previous flows, search again
                    if route is None or not (set(route.get_junctions()) & discovered):
                        # print(f"Route is 'None': {route is None}")
                        continue
                    return route
            return route
        # Find first route
        discovered = set(self.graph.skeleton.junctions.keys())
        # print(f"Generating random first route: ")
        routes.append(generate_path())
        if routes[0] is None:
            print(f"Unable to find route, increase 'max_tries' variable or check probability file !")
            return []
        discovered = set(routes[0].get_junctions())
        for i in range(amount-1):
            # print(f"Generating {i}-th path")
            result: Route = generate_path()
            if result is None:
                print(f"Unable to find route, increase 'max_tries' variable or check probability file !")
                return routes
            routes.append(result)
            # print(f"Found route: {result}")
            # print(f"Has conflict: {(set(result.get_junctions()) & discovered)}")
            discovered |= set(result.get_junctions())
            # print(f"Discovered: {discovered}")
        return routes

    # -------------------------------------- Utils --------------------------------------

    def check_prob_matrix(self) -> bool:
        """
        :return:
        """
        if self.graph is None:
            print(f"Graph is None, cannot check probability matrix!")
            return False
        elif not self.prob_matrix:
            print(f"Invalid probability matrix, either of type 'None' or empty!")
            return False
        for starting_junction in self.prob_matrix.keys():
            # Check starting junctions
            if starting_junction not in self.graph.skeleton.starting_junctions:
                print(f"Invalid starting junction: '{starting_junction}' for network: '{self.graph.skeleton.map_name}'")
                return False
            # Check destination junctions
            for destination_junction in self.prob_matrix[starting_junction].keys():
                if destination_junction not in self.graph.skeleton.ending_junctions:
                    print(
                        f"Invalid ending junction: '{destination_junction}' "
                        f"for network: '{self.graph.skeleton.map_name}'"
                    )
                    return False
        return True


# For testing purposes
if __name__ == "__main__":
    graph: Graph = Graph(Skeleton())
    graph.loader.load_map("Dejvice")
    graph.simplify.simplify_graph()
    temp: FlowFactory = FlowFactory(graph, ProbabilityFile("dejvice"))
    for flow_name, flow_args in temp.generate_flows(0, 0, 300):
        print(flow_name, flow_args)


