from Project.Simplify.Graph_modules.graph_module import GraphModule
from Project.Simplify.Graph_modules.display import Display
from queue import PriorityQueue
from typing import List, Tuple, Dict
from Project.Simplify.Components import Route
from numpy import array
from numpy.linalg.linalg import norm
from time import sleep


class ShortestPath(GraphModule):
    """ Class containing shortest path algorithms """

    def __init__(self):
        super().__init__()
        print("Created 'ShortestPath' class")

    def top_k_a_star(self, start_junction_id: str, target_junction_id: str, c: float, plot: Display = None) -> List[Route]:
        """
        At start, performs A* search to find shortest route,
        uses unexplored junction remaining in queue from the initial call of A* to find K other routes.
        K in this case can be limited by parameter c, which sets the maximal length
        of new routes to be at maximum c * shortest_route_length

        :param start_junction_id: starting junction
        :param target_junction_id: target junction
        :param c: multiplier of shortest path length
        :param plot: Class Display, if plot should be displayed (default None)
        :return: List of routes (shortest route is the first) satisfying (route_length < c * shortest_route_length),
        empty list if shortest route does not exists
        """
        # -------------------------------- checks --------------------------------
        assert (start_junction_id in self.skeleton.junctions)
        assert (target_junction_id in self.skeleton.junctions)
        assert (c > 1)
        # -------------------------------- init --------------------------------
        # Perform initial search to find shortest route and return queue with unexplored junctions
        queue, shortest_route = self.a_star(start_junction_id, target_junction_id)
        if shortest_route is None:  # No path exists
            print(f"No path exists between {start_junction_id} and {target_junction_id}")
            return []
        print("Found shortest route")
        destination_pos: array = array(self.skeleton.junctions[target_junction_id].get_position())
        limit: float = c * sum([edge.attributes["length"] for edge in shortest_route.edge_list])
        assert (limit > 0)
        print(f"Setting route length limit: {limit}")
        other_routes: List[Route] = [shortest_route]
        # -------------------------------- Algorithm --------------------------------
        while not queue.empty():
            priority, length, in_route_id, path = queue.get()  # Removes and returns
            junction_id: str = path[-1]
            if priority > limit:  # Priority is current length + euclidean distance to target
                break  # End of search
            elif junction_id == target_junction_id:
                # Found other path (satisfying path_length < c * shortest_path_length), record it
                assert (length <= limit)
                other_routes.append(self.skeleton.construct_route(path))
                continue
            for route in self.skeleton.junctions[junction_id].travel(in_route_id):
                distance, neigh_junction_id = route.traverse()
                current_distance: float = length + distance
                if neigh_junction_id not in path:  # Avoid loops
                    pos: array = array(self.skeleton.junctions[neigh_junction_id].get_position())  # Current position
                    queue.put((
                        (current_distance + norm(destination_pos - pos)),
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
                fig.canvas.draw()
                sleep(0.1)
            plot.show_plot()
        return other_routes

    # *************************************  Shortest path *************************************

    def a_star(self, start_junction_id: str, target_junction_id: str) -> Tuple[PriorityQueue, Route]:
        """
        Standard implementation of A* algorithm

        :param start_junction_id: start
        :param target_junction_id: goal
        :return: queue containing unexplored junctions, shortest route (None if it could not be found)
        """
        print(f"Finding shortest route from: {start_junction_id}, to: {target_junction_id} using A* algorithm")
        # -------------------------- Init --------------------------
        destination_pos: array = array(self.skeleton.junctions[target_junction_id].get_position())
        # priority, distance, in_route, path (list of visited junctions)
        queue: PriorityQueue[Tuple[float, float, Route, List[str]]] = PriorityQueue()
        queue.put((0, 0, None, [start_junction_id]))
        # For node n, gScore[n] is the cost of the cheapest path from start to n currently known
        g_score: Dict[str, float] = {junction_id: float("inf") for junction_id in self.skeleton.junctions}
        g_score[start_junction_id] = 0  # id of 0 for route is reserved!
        shortest_route: Route = None
        if not self.check_junctions(start_junction_id, target_junction_id):
            return queue, shortest_route
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
                    pos: array = array(self.skeleton.junctions[neigh_junction_id].get_position())  # Current position
                    g_score[neigh_junction_id] = tentative_g_score  # Update distances
                    queue.put((
                        (tentative_g_score + norm(destination_pos - pos)),
                        tentative_g_score, route, path + [neigh_junction_id]
                    ))
        print(f"Finished finding route: {shortest_route} ")
        return queue, shortest_route

    def dijkstra(self, start_junction_id: str, target_junction_id: str = "") -> Tuple[Dict[str, float], Dict[str, str]]:
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
            return dist, prev
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
        # -------------------------- Finished --------------------------
        return dist, prev

    # ************************************* Utils *************************************

    def reconstruct_path(self, target_junction_id: str, dist: Dict[str, float], prev: Dict[str, str]) -> Route:
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
        if start_junction_id == target_junction_id:
            print(f"No possible path between the same junctions!")
            return False
        return True
