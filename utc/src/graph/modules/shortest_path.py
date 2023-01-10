from utc.src.graph.modules.graph_module import GraphModule
from utc.src.graph.components import Skeleton, Route
from utc.src.graph.modules.display import Display, plt
from queue import PriorityQueue
from typing import List, Tuple, Dict, Optional


class ShortestPath(GraphModule):
    """ Class containing shortest path algorithms """

    def __init__(self, skeleton: Skeleton = None):
        super().__init__(skeleton)

    # -------------------------------------- Shortest path --------------------------------------

    def top_k_a_star(self, start_junction_id: str, target_junction_id: str, c: float, plot: Display = None) -> List[Route]:
        """
        At start, performs A* search to find shortest route,
        uses unexplored junction remaining in queue from the initial call of A* to find K other routes.
        K in this case can be limited by parameter c, which sets the maximal length
        of new routes to be at maximum c * shortest_route_length

        :param start_junction_id: starting junction
        :param target_junction_id: target junction
        :param c: multiplier of shortest path length
        :param plot: Class Display, if process should be displayed (default None)
        :return: List of routes (shortest route is the first) satisfying (route_length < c * shortest_route_length),
        empty list if shortest route does not exists
        """
        # -------------------------------- checks --------------------------------
        if not self.check_junctions(start_junction_id, target_junction_id):
            return []
        elif not c > 1:
            print(f"Parameter 'c' has to be greater than 1, got: {c}")
            return []
        # -------------------------------- init --------------------------------
        # Perform initial search to find shortest route and return queue with unexplored junctions
        queue, shortest_route = self.a_star(start_junction_id, target_junction_id)
        if shortest_route is None:  # No path exists
            print(f"No path exists between junction {start_junction_id} and junction {target_junction_id}")
            return []
        destination_pos: Tuple[float, float] = self.skeleton.junctions[target_junction_id].get_position()
        limit: float = round(c * shortest_route.traverse()[0], 3)
        assert (limit > 0)
        print(f"Setting alternative route length limit: {limit}")
        other_routes: List[Route] = [shortest_route]
        # -------------------------------- Algorithm --------------------------------
        while not queue.empty():
            priority, length, in_route, path = queue.get()  # Removes and returns
            current_junction_id: str = path[-1]
            if priority > limit:  # Priority is current length + euclidean distance to target
                break  # End of search
            elif current_junction_id == target_junction_id:
                # Found other path (satisfying path_length < c * shortest_path_length), record it
                assert (length <= limit)
                other_routes.append(self.skeleton.construct_route(path))
                if len(other_routes) > 2999:
                    print(f"Reach limit of 5000 routes found, stopping search ...")
                    break
                continue
            for route in self.skeleton.junctions[current_junction_id].travel(in_route):
                distance, neigh_junction_id = route.traverse()
                current_distance: float = length + distance
                if neigh_junction_id not in path:  # Avoid loops
                    # Current position
                    pos: Tuple[float, float] = self.skeleton.junctions[neigh_junction_id].get_position()
                    queue.put((
                        (current_distance + self.coord_distance(destination_pos, pos)),
                        current_distance, route, path + [neigh_junction_id]
                    ))
        print(f"Finished finding routes, found another: {len(other_routes) - 1} routes")
        # -------------------------------- Plot --------------------------------
        if plot is not None:  # Show animation of routes
            fig, ax = plot.default_plot()
            for index, route in enumerate(other_routes):
                ax.clear()
                plot.plot_default_graph(ax)
                route.plot(ax, color="blue")
                plot.add_label("_", "blue", f"Route: {index}, length: {round(route.traverse()[0])}")
                plot.make_legend(1)
                plt.tight_layout()
                fig.canvas.draw()
                plt.pause(0.1)
            plot.show_plot()
        return other_routes

    def a_star(self, start_junction_id: str, target_junction_id: str) -> Tuple[PriorityQueue, Optional[Route]]:
        """
        Standard implementation of A* algorithm

        :param start_junction_id: start
        :param target_junction_id: goal
        :return: queue containing unexplored junctions, shortest route (None if it could not be found)
        """
        # print(f"Finding shortest route from: {start_junction_id}, to: {target_junction_id} using A* algorithm")
        # -------------------------- Init --------------------------
        destination_pos: Tuple[float, float] = self.skeleton.junctions[target_junction_id].get_position()
        # priority, distance, in_route, path (list of visited junctions)
        queue: PriorityQueue[Tuple[float, float, Route, List[str]]] = PriorityQueue()
        # For node n, gScore[n] is the cost of the cheapest path from start to n currently known
        g_score: Dict[str, float] = {junction_id: float("inf") for junction_id in self.skeleton.junctions.keys()}
        g_score[start_junction_id] = 0  # id of 0 for route is reserved!
        shortest_route: Optional[Route] = None
        if not self.check_junctions(start_junction_id, target_junction_id):
            return queue, shortest_route
        queue.put((0, 0, shortest_route, [start_junction_id]))
        # -------------------------- Algorithm --------------------------
        while not queue.empty():
            priority, length, in_route, path = queue.get()  # Removes and returns
            junction_id: str = path[-1]
            if junction_id == target_junction_id:  # Found shortest path
                shortest_route = self.skeleton.construct_route(path)
                break
            for route in self.skeleton.junctions[junction_id].travel(in_route):
                distance, neigh_junction_id = route.traverse()
                tentative_g_score = g_score[junction_id] + distance
                if tentative_g_score < g_score[neigh_junction_id]:
                    # Current position
                    pos: Tuple[float, float] = self.skeleton.junctions[neigh_junction_id].get_position()
                    g_score[neigh_junction_id] = tentative_g_score  # Update distances
                    queue.put((
                        (tentative_g_score + self.coord_distance(destination_pos, pos)),
                        tentative_g_score, route, path + [neigh_junction_id]
                    ))
        # print(f"Finished finding shortest route: {shortest_route} ")
        return queue, shortest_route

    def dijkstra(self, start_junction_id: str, target_junction_id: str = "") -> Optional[Route]:
        """
        Standard implementation of dijkstra's algorithm

        :param start_junction_id: where should search start
        :param target_junction_id: where should search end
        :return: Tuple containing two dictionaries, one contains junctions pointing to previous
        junctions, the other maps junction_id to distance
        """
        print(f"Finding shortest route from: {start_junction_id}, to: {target_junction_id} using Dijkstra's algorithm")
        # -------------------------- Init --------------------------
        # (priority, junction_id, in_route_id)
        queue: PriorityQueue[Tuple[float, str, Route]] = PriorityQueue()
        # {junction_id : distance(float), ...}
        dist: Dict[str, float] = {key: float("inf") for key in self.skeleton.junctions.keys()}
        # {junction_id : previous_junction_id, ...}
        prev: Dict[str, str] = {key: None for key in dist.keys()}
        if not self.check_junctions(start_junction_id, target_junction_id):
            return None
        # -------------------------- Algorithm --------------------------
        dist[start_junction_id] = 0
        queue.put((0, start_junction_id, None))
        while not queue.empty():
            priority, junction_id, in_route = queue.get()
            if junction_id == target_junction_id:
                print(f"Found goal, distance: {dist[junction_id]}")
                break
            # Visit only the current shortest path
            if priority == dist[junction_id]:
                for route in self.skeleton.junctions[junction_id].travel(in_route):
                    distance, to_junction_id = route.traverse()
                    current_distance: float = priority + distance
                    if current_distance < dist[to_junction_id]:  # Found shorter path, record and add to queue
                        dist[to_junction_id] = current_distance
                        prev[to_junction_id] = junction_id
                        queue.put((current_distance, to_junction_id, route))
        return self.reconstruct_path(target_junction_id, dist, prev)

    # -------------------------------------- Utils --------------------------------------

    def coord_distance(self, point_a: Tuple[float, float], point_b: Tuple[float, float]) -> float:
        """
        :param point_a: first point
        :param point_b: second point
        :return: absolute distance between points (3 decimal precision)
        """
        diff_x: float = abs(point_a[0] - point_b[0])
        diff_y: float = abs(point_a[1] - point_b[1])
        return round(((diff_x ** 2) + (diff_y ** 2)) ** 0.5, 3)

    def reconstruct_path(self, target_junction_id: str, dist: Dict[str, float], prev: Dict[str, str]) -> Optional[Route]:
        """
        :param target_junction_id: destination
        :param dist: distance of junctions
        :param prev: mapping pointing junction to previous one on path
        :return: Route, or None if there is no path or target_junction does not exist
        """
        if (target_junction_id in self.skeleton.junctions) and (dist[target_junction_id] != float("inf")):
            path: List[str] = []
            while target_junction_id:
                path.insert(0, target_junction_id)
                target_junction_id = prev[target_junction_id]
            return self.skeleton.construct_route(path)
        return None

    def check_junctions(self, start_junction_id: str, target_junction_id: str) -> bool:
        """
        :param start_junction_id: where should search start
        :param target_junction_id: where should search end
        :return: True if both junctions exist and are not equal, False otherwise
        """
        if start_junction_id not in self.skeleton.junctions.keys():
            print(f"Junction: {start_junction_id} does not exist!")
            return False
        elif target_junction_id not in self.skeleton.junctions.keys():
            print(f"Junction: {target_junction_id} does not exist!")
            return False
        elif start_junction_id == target_junction_id:
            print(f"No possible path between the same junctions!")
            return False
        return True
