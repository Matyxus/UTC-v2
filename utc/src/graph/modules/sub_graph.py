from utc.src.graph.modules.graph_module import GraphModule
from utc.src.graph.components import Skeleton, Route, Edge
from utc.src.graph.modules.display import Display, plt
from typing import List, Set, Optional
from copy import deepcopy


class SubGraph(GraphModule):
    """ Class containing methods which create graphs """

    def __init__(self, skeleton: Skeleton = None):
        super().__init__(skeleton)

    def create_sub_graph(self, routes: List[Route]) -> Optional[Skeleton]:
        """
        Creates sub-graph from this graph.

        :param routes: List of routes from which sub-graph will be created
        :return: Skeleton (sub-graph), None if routes are empty
        """
        assert (self.skeleton is not None)
        sub_graph: Skeleton = Skeleton()
        sub_graph.map_name = deepcopy(self.skeleton.map_name)
        if len(routes) == 0 or not sub_graph.load(self.skeleton):
            return None
        # -------------------------- Cut graph --------------------------
        junctions: Set[str] = set()  # Junctions to be kept in graph
        edges: Set[Edge] = set()  # Edges to be kept in graph
        # Extract junctions and edges from routes
        for route in routes:
            edges |= set(route.edge_list)
            junctions |= set(route.get_junctions())
        # Delete others edges, junctions
        for edge in (set(self.skeleton.edges.values()) ^ edges):
            sub_graph.remove_edge(edge.attributes["id"])
        for junction_id in (self.skeleton.junctions.keys() ^ junctions):
            sub_graph.remove_junction(junction_id)
        return sub_graph

    def merge(self, other: Skeleton, display: Display = None) -> Optional[Skeleton]:
        """
        Merges graph currently set SubGraph class with another graph.

        :param other: another graph current graph is merging with
        :param display: Class Display, if process should be displayed (default None)
        :return: New graph made from both graphs
        """
        assert (self.skeleton is not None)
        if self.skeleton.map_name != other.map_name:
            print(f"Only graphs of the same network may be merged {self.skeleton.map_name} != {other.map_name}")
            return None
        print("Merging with another graph")
        new_graph: Skeleton = Skeleton()
        new_graph.load(self.skeleton)  # Copy graph A
        # ------------------------ Plot -----------------------
        colors: List[str] = ["mediumblue", "gold", "darkmagenta"]
        if display is not None:  # Plot both graphs next to each other (differently colored)
            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 8), sharex="all", sharey="all")
            ax[0].title.set_text("Graph A")
            ax[1].title.set_text("Graph B")
            for index, skeleton in enumerate([self.skeleton, other]):
                ax[index].set(aspect='auto')
                display.set_skeleton(skeleton)
                display.plot_default_graph(ax[index], edge_color=colors[index])
            display.show_plot()
        # ------------------------ Junctions ------------------------
        new_graph.starting_junctions |= other.starting_junctions
        new_graph.ending_junctions |= other.ending_junctions
        for junction_id, junction in other.junctions.items():
            if junction_id in new_graph.junctions:
                new_graph.junctions[junction_id] |= junction
            else:
                new_graph.junctions[junction_id] = deepcopy(junction)
        # ------------------------ Routes ------------------------
        for route_id, route in other.routes.items():
            if route_id not in new_graph.routes:
                new_graph.routes[route.id] = deepcopy(route)
        # ------------------------ Edges ------------------------
        for edge_id, edge in other.edges.items():
            if edge_id not in new_graph.edges:
                new_graph.edges[edge_id] = deepcopy(edge)
        # ------------------------ Plot ------------------------
        if display is not None:
            display.set_skeleton(new_graph)
            fig, ax = display.default_plot()
            # Common edges
            common: Set[str] = self.skeleton.edges.keys() & other.edges.keys()
            colored_edges: List[Set[str]] = [
                (self.skeleton.edges.keys() ^ common) & new_graph.edges.keys(),  # Edges only present in graph "a"
                (other.edges.keys() ^ common) & new_graph.edges.keys(),  # Edges only present in graph "b"
                common  # Edges present in both graphs
            ]
            # Plot colored edges
            for index, edges in enumerate(colored_edges):
                for edge_id in edges:
                    new_graph.edges[edge_id].plot(ax, color=colors[index])
            display.add_label("o", colors[0], "Subgraph A")
            display.add_label("o", colors[1], "Subgraph B")
            display.add_label("o", colors[2], "United")
            display.make_legend(len(colors))
            display.show_plot()
        return new_graph
