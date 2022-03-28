from typing import List, Set
from Project.Simplify.Utils import Loader, RouteManager
from Project.Simplify.Components import Skeleton, Route
from Project.constants import CWD, file_exists, JUNCTION_DEFAULT_COLOR
from matplotlib import pyplot as plt
from copy import deepcopy


class Graph(Skeleton):
    """ Graph of road network made from SUMO's '.net.xml' file """

    def __init__(self, struct: Skeleton = None):
        super().__init__()
        self.load(struct)
        self.route_manager: RouteManager = RouteManager(self.get_skeleton())
        self.roundabouts: List[List[str]] = []
        self.map_name: str = "Unknown"
        self.route_count: int = 0

    # Imported methods
    from Project.Simplify.MyGraph._simplify_graph import simplify_roundabouts, simplify_junctions, junction_can_be_removed
    from Project.Simplify.MyGraph._plot_graph import plot, default_plot, add_label, show_plot, make_legend, plot_default_graph
    from Project.Simplify.MyGraph._path_finder import reconstruct_path, dijkstra, A_star, TopK_A_star

    # -------------------------- Sub-graph --------------------------
    def create_sub_graph(self, start_junction_id: str, target_junction_id: str, c: float, plot: bool):
        """
        Find all routes from TopK_A_start, that satisfy constraint,
        from which sub-graph will be created, removes all other routes.

        :param start_junction_id: start
        :param target_junction_id: destination
        :param c: parameter (> 1) that multiplies shortest distance, setting this value as maximal route length
        :param plot: bool, if plot should be displayed
        :return: Graph (sub-graph), None if shortest path does not exist
        """
        print(f"Creating sub-graph, from: {start_junction_id} to {target_junction_id}, c: {c}, plot: {plot}")
        # -------------------------------- checks --------------------------------
        assert (start_junction_id in self.junctions)
        assert (target_junction_id in self.junctions)
        assert (c > 1)
        # -------------------------------- Init --------------------------------
        sub_graph: Graph = Graph(self.get_skeleton())
        found_routes: List[Route] = self.TopK_A_star(start_junction_id, target_junction_id, c, plot)
        if len(found_routes) == 0:  # Shortest path between start and destination does not exist
            return None
        if plot:  # Show animation of routes
            fig, ax = self.default_plot()
            #
            for index, route in enumerate(found_routes):
                ax.clear()
                self.plot_default_graph(ax)
                length: int = round(sum([self.edges[edge_id].attributes["length"] for edge_id in route.edge_list]))
                self.route_manager.plot(ax, route, color="blue")
                self.add_label("_", "blue", f"Route: {index}, length: {length}")
                self.make_legend(1)
                plt.tight_layout()
                fig.canvas.draw()
                plt.pause(0.1)
            self.show_plot()
        # -------------------------- Cut graph --------------------------
        junctions: Set[str] = set()  # Junctions to be kept in graph
        edges: Set[str] = set()  # Edges to be kept in graph
        # Extract junctions and edges from routes
        for route in found_routes:
            edges |= set(route.edge_list)
            junctions |= set(self.route_manager.get_junctions(route))
        # Delete others edges, junctions
        for edge_id in (self.edges.keys() ^ edges):
            sub_graph.remove_edge(edge_id)
        for junction_id in (self.junctions.keys() ^ junctions):
            sub_graph.remove_junction(junction_id)
        print("Finished creating sub-graph")
        return sub_graph, found_routes

    # ----------------------------------- Utils -----------------------------------

    def merge(self, other, plot: bool) -> None:
        """
        Merges this graph with another graph.

        :param other: another graph current graph is merging with
        :param plot: bool, if plot should be displayed
        :return: None
        """
        assert (isinstance(other, Graph))
        print("Merging with another graph")
        # ------------------------ Plot ------------------------
        previous_junctions: Set[str] = set()
        previous_edges: Set[str] = set()
        colors: List[str] = ["mediumblue", "gold", "darkmagenta"]
        if plot:
            # Save previous junctions, edges to show merged graph
            previous_junctions = set(self.junctions.keys())
            previous_edges = set(self.edges.keys())
            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 8), sharex="all", sharey="all")
            ax[0].title.set_text("Graph A")
            ax[1].title.set_text("Graph B")
            ax[0].set(aspect='auto')
            ax[1].set(aspect='auto')
            self.plot_default_graph(ax[0], edge_color=colors[0])
            other.plot_default_graph(ax[1], edge_color=colors[1])
            self.show_plot()
        # ------------------------ Junctions ------------------------
        self.starting_junctions |= other.starting_junctions
        self.ending_junctions |= other.ending_junctions
        for junction_id, junction in other.junctions.items():
            if junction_id in self.junctions:
                self.junctions[junction_id] |= junction
            else:
                self.junctions[junction_id] = deepcopy(junction)
        # ------------------------ Routes ------------------------
        for route in other.routes.values():
            if route.id not in self.routes:
                self.routes[route.id] = deepcopy(route)
        # ------------------------ Edges ------------------------
        for edge_id, edge in other.edges.items():
            if edge_id not in self.edges:
                self.edges[edge_id] = deepcopy(edge)
        # ------------------------ Plot ------------------------
        if plot:
            assert (len(previous_edges) != 0)
            assert (len(previous_junctions) != 0)
            fig, ax = self.default_plot()
            # Junctions
            for junction_id, junction in self.junctions.items():
                junction.plot(ax, color=JUNCTION_DEFAULT_COLOR)
            # Edges
            for edge_id, edge in self.edges.items():
                color_index: int = 0  # Assuming edge is in original graph
                if edge_id in other.edges.keys():  # Edge is in other
                    color_index += 1
                    if edge_id in previous_edges:  # Edge is in both graphs
                        color_index += 1
                edge.plot(ax, color=colors[color_index])
            self.add_label("o", colors[0], "Subgraph A")
            self.add_label("o", colors[1], "Subgraph B")
            self.add_label("o", colors[2], "United")
            self.make_legend(len(colors))
            self.show_plot()

    def validate_graph(self) -> None:
        """
        Checks all junctions, edges, routes.
        Removes unused junctions, routes, edges,
        should be called on final sub-graph

        :return: None
        """
        print("Validating graph")
        routes_to_remove: List[int] = []
        # Check routes, find routes that have edge which is no longer in graph
        for route in self.routes.values():
            for edge_id in route.edge_list:
                if edge_id not in self.edges:
                    routes_to_remove.append(route.id)
                    break
        # Remove routes such routes
        for route_id in routes_to_remove:
            self.routes.pop(route_id)
        # Among junctions check routes, if route is not used, remove it
        for junction in self.junctions.values():
            in_routes: List[int] = junction.get_in_routes()
            for in_route_id in in_routes:
                if in_route_id not in self.routes:
                    junction.remove_in_route(in_route_id)
            out_routes: List[int] = junction.get_out_routes()
            for out_route_id in out_routes:
                if out_route_id not in self.routes:
                    junction.remove_out_route(out_route_id)
        print("Finished validating graph")

    def shortest_path(self, from_junction_id: str, to_junction_id: str, plot: bool) -> Route:
        """
        :param from_junction_id: start
        :param to_junction_id: destination
        :param plot: boolean, if route should be shown
        :return: Route, can be None if it does not exist
        """
        # ---------------------------- Checks ----------------------------
        if from_junction_id == to_junction_id:
            print(f"No path between the same junctions: {from_junction_id} and {to_junction_id}")
            return None
        if from_junction_id not in self.junctions:
            print(f"{from_junction_id} is not junction id!")
            return None
        elif to_junction_id not in self.junctions:
            print(f"{to_junction_id} is not junction id!")
            return None
        # Shortest route
        dist, prev = self.dijkstra(from_junction_id, to_junction_id)
        route: Route = self.reconstruct_path(to_junction_id, dist, prev)
        if plot and route is not None:
            fig, ax = self.default_plot()
            distance: int = round(dist[to_junction_id])
            self.add_label("_", "red", f"Shortest path, length: {distance}")
            self.make_legend(1)
            self.route_manager.plot(ax, route, color="red")
            self.show_plot()
        return route

    def load_from_file(self, map_name: str) -> bool:
        """
        :param map_name: from which graph should be loaded (expecting it to be
        located in /Maps/sumo/map_name.net.xml)
        :return: True on success, false otherwise
        """
        if not file_exists(f"{str(CWD)}/Maps/sumo/{map_name+'.net.xml'}"):
            return False
        self.map_name = map_name
        loader = Loader(map_name, self.get_skeleton(), self.route_manager)
        loader.load_junctions()  # Junctions must be loaded first!
        loader.load_edges()
        self.roundabouts = loader.load_roundabouts()
        return True
