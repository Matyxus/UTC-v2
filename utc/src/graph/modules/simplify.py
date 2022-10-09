from utc.src.graph.modules.graph_module import GraphModule
from utc.src.graph.modules.display import Display
from utc.src.graph.components import Skeleton
from utc.src.graph.components import Route, Junction
from typing import List, Set, Tuple, Dict


class Simplify(GraphModule):
    """ Class which contains methods for simplifying graph """

    def __init__(self, skeleton: Skeleton = None):
        super().__init__(skeleton)

    def simplify_graph(self, plot: Display = None) -> None:
        """
        Simplifies graph by removing junctions forming roundabout, or those
        added by SUMO which are only for rendering/graphical reasons (they
        do not exist in '.osm' maps).

        :param plot: Class Display, if plot should be displayed (default None)
        :return: None
        """
        assert (self.skeleton is not None)
        # Check for valid roundabouts
        self.skeleton.roundabouts = [
            roundabout for roundabout in self.skeleton.roundabouts if self.check_roundabout(roundabout)
        ]
        self.simplify_junctions(plot)
        self.simplify_roundabouts(plot)

    def simplify_junctions(self, plot: Display = None) -> None:
        """
        Finds junctions, that may be removed, e.g.
        A ----> B ---- > C (B can be removed),
        A <---> B <----> C (B can be removed),
        Takes out_route from B and merges it with in_route to B,
        for all out_routes, in_routes,
        should be called before simplify_roundabouts

        :param plot: Class Display, if plot should be displayed (default None)
        :return: None
        """
        print("Simplifying junctions")
        # Junctions that cannot be removed
        non_removable: Set[str] = (self.skeleton.starting_junctions | self.skeleton.ending_junctions)
        for roundabout in self.skeleton.roundabouts:
            non_removable |= set(roundabout)
        connections: Dict[str, List[Route]] = {}
        assert ((self.skeleton.junctions.keys() & non_removable) == non_removable)
        # Find junctions that can be removed
        for junction_id in (self.skeleton.junctions.keys() ^ non_removable):
            if self.junction_can_be_removed(junction_id):
                connections[junction_id] = []
        # Among junctions to be removed, find in_routes that are from junction
        # which is not removable, those without such routes are connected to another removable junction
        for junction_id in connections.keys():
            for in_route in self.skeleton.junctions[junction_id].get_in_routes():
                if in_route.get_start() not in connections:
                    connections[junction_id].append(in_route)
        print("Merging routes")
        for junction_id, in_routes in connections.items():
            for in_route in in_routes:
                replacing_junction_id: str = in_route.get_start()
                # Find route from junction before this one
                route: Route = self.skeleton.find_route(replacing_junction_id, junction_id)
                current_route: Route = route
                # print(f"Starting to merge route: {route}, starting at junction: {junction_id}")
                assert (route is not None)
                # While we are traversing among removable junctions, connect routes
                destination_junction_id: str = current_route.get_destination()
                assert (destination_junction_id == junction_id)  # Sanity check
                while destination_junction_id in connections:
                    # print(f"Checking junction: {destination_junction_id}")
                    assert (len(self.skeleton.junctions[destination_junction_id].travel(current_route)) == 1)
                    # There can only be one route, that's why junction can be removed
                    out_route: Route = self.skeleton.junctions[destination_junction_id].travel(current_route)[0]
                    route |= self.skeleton.remove_route(out_route.get_id())
                    current_route = out_route  # Move route id to last merged one
                    destination_junction_id: str = current_route.get_destination()
                # Change incoming route of last Junction of current route, to be the same as current route.id
                self.skeleton.junctions[destination_junction_id].replace_in_route(current_route, route)
                # print(f"Final route: {route}")
        print("Finished merging routes")
        # Remove junctions
        removed_junctions: List[Junction] = [self.skeleton.remove_junction(junction_id) for junction_id in connections]
        # ------------------ Plot ------------------
        if plot is not None:
            fig, ax = plot.default_plot()
            for junction in removed_junctions:
                junction.plot(ax, color="red")
            plot.add_label("o", "red", "Removed Junctions")
            plot.make_legend(1)
            plot.show_plot()
        print("Finished simplifying junctions")

    def simplify_roundabouts(self, plot: Display = None) -> None:
        """
        Removes junctions forming roundabout, replaces them
        with new node (at center of mass position), adds new routes,
        removes previous routes between roundabout nodes,
        should be called after simplify_junctions

        :param plot: Class Display, if plot should be displayed (default None)
        :return: None
        """
        print(f"Simplifying roundabouts: {self.skeleton.roundabouts}")
        for index, roundabout in enumerate(self.skeleton.roundabouts):
            # ---------------- Variable setup ----------------
            roundabout_points: List[Tuple[float, float]] = []  # Position of each junction (x, y)
            roundabout_routes: Set[Route] = set()  # Routes on roundabout
            in_routes: Set[Route] = set()  # Routes connection to roundabout
            out_routes: Set[Route] = set()  # Routes coming out of roundabout
            for junction_id in roundabout:
                junction: Junction = self.skeleton.junctions[junction_id]
                roundabout_points.append(junction.get_position())
                # Find all entry points to roundabout
                for in_route in junction.get_in_routes():
                    # Get edges going to roundabout
                    if not (in_route.get_start() in roundabout):
                        in_routes.add(in_route)
                # Find all exit points of roundabout
                for out_route in junction.get_out_routes():
                    # Get route going from roundabout
                    if not (out_route.get_destination() in roundabout):
                        out_routes.add(out_route)
                    else:  # Route leads to another roundabout junction
                        roundabout_routes.add(out_route)
            # ---------------- Setup new junction ----------------
            new_point: tuple = self.get_center_of_mass(roundabout_points)
            new_junction_id: str = f"r{index}"  # "r" for roundabout to not confuse with normal junctions
            new_junction: Junction = Junction(
                {"id": new_junction_id, "x": new_point[0], "y": new_point[1], "type": "roundabout"}
            )
            new_junction.marker_size = 10
            new_junction.color = "yellow"
            print(f"Creating new junction: {new_junction_id} representing roundabout: {roundabout}")
            # ---------------- From all entrances of roundabout form new routes ----------------
            for in_route in in_routes:
                starting_junction_id: str = in_route.get_destination()
                current_junction: Junction = self.skeleton.junctions[starting_junction_id]
                assert (starting_junction_id in roundabout)  # Sanity check
                new_route: Route = Route([])  # New route for new junction
                # Since we entered roundabout now, the only (possible) route now leads to another roundabout junction
                current_out_routes: Set[Route] = set(current_junction.travel(in_route))
                assert (len(current_out_routes) == 1)  # Sanity check
                route: Route = current_out_routes.pop()
                assert (route.get_destination() in roundabout)  # Sanity check
                new_route |= route  # Modify current route
                current_junction_id: str = route.get_destination()
                while current_junction_id != starting_junction_id:
                    current_junction = self.skeleton.junctions[current_junction_id]
                    # print(f"Currently on junction: {current_junction_id}")
                    # Get all out coming routes
                    current_out_routes = set(current_junction.get_out_routes())
                    # Routes going out of current roundabout junction
                    routes_out_roundabout: Set[Route] = (current_out_routes & out_routes)
                    # Create new routes for each path leading out of roundabout
                    for out_route in routes_out_roundabout:
                        new_route_out: Route = (Route([]) | new_route | out_route)
                        self.skeleton.add_route(new_route_out)  # Add new route to skeleton of graph
                        new_junction.add_connection(in_route, new_route_out)  # Add new route to junction
                        # Add new incoming route to connected junction
                        destination: Junction = self.skeleton.junctions[new_route_out.get_destination()]
                        destination.neighbours[new_route_out] = destination.neighbours[out_route]
                        # destination.replace_in_route(out_route, new_route_out)
                    assert (len(current_out_routes ^ routes_out_roundabout) == 1)
                    route = (current_out_routes ^ routes_out_roundabout).pop()
                    # print(f"Route: {self.routes[route_id]}")
                    current_junction_id = route.get_destination()
                    new_route |= route  # Move to next roundabout junction
                    # print(f"New route: {new_route}")
                current_junction = self.skeleton.junctions[current_junction_id]
                assert (current_junction_id == starting_junction_id)
                # Now current_junction is equal to starting_junction
                # Check if starting junction has any out edges, add them as new route
                for out_route in (set(current_junction.get_out_routes()) & out_routes):
                    new_route_out: Route = (Route([]) | new_route | out_route)
                    # print(f"New route added to junction: {new_route_out}")
                    self.skeleton.add_route(new_route_out)  # Add new route to skeleton of graph
                    new_junction.add_connection(in_route, new_route_out)  # Add new route to junction
                    # Add new incoming route to connected junction
                    destination: Junction = self.skeleton.junctions[new_route_out.get_destination()]
                    destination.neighbours[new_route_out] = destination.neighbours[out_route]
                    # destination.replace_in_route(out_route, new_route_out)
            self.skeleton.roundabouts = []  # Empty list
            # ---------------- Remove ----------------
            # Remove routes on roundabout
            for route in roundabout_routes:
                self.skeleton.remove_route(route)
            # Remove routes out of roundabout, connection on junctions
            for route in out_routes:
                destination: Junction = self.skeleton.junctions[route.get_destination()]
                destination.remove_in_route(route)
                self.skeleton.remove_route(route)
            # Set each out coming route of roundabout attribute["from"] as new junction
            for route in new_junction.get_out_routes():
                route.first_edge().attributes["from"] = new_junction_id
            # Set each incoming edge of roundabout, attribute["to"] as new junction
            for route in in_routes:
                route.last_edge().attributes["to"] = new_junction_id
            # Remove junctions forming roundabout
            removed_junctions: List[Junction] = [
                self.skeleton.remove_junction(junction_id) for junction_id in roundabout
            ]
            # Add new junction
            self.skeleton.junctions[new_junction.attributes["id"]] = new_junction
            # ---------------- Plot ----------------
            if plot is not None:
                fig, ax = plot.default_plot()
                # Remove junctions from roundabout
                for junction in removed_junctions:
                    junction.plot(ax, color="red")
                new_junction.plot(ax)
                plot.add_label("o", "red", "Roundabout junctions")
                plot.add_label("o", new_junction.color, "Roundabout")
                plot.make_legend(2)
                plot.show_plot()
        print("Done simplifying roundabouts")

    # ----------------------------------- Utils -----------------------------------

    def check_roundabout(self, roundabout: List[str]) -> bool:
        """
        :param roundabout: list of junction id's forming roundabout
        :return: True if roundabout is truly a roundabout
        """
        if not len(roundabout):  # Empty roundabout
            return False
        # For every junction, check if it is connected to another roundabout junction
        for junction_id in roundabout:
            found = False
            for route in self.skeleton.junctions[junction_id].get_out_routes():
                # Found connection, check for other junction
                if route.get_destination() in roundabout:
                    found = True
                    break
            # No connection found, this is not roundabout
            if not found:
                return False
        return True

    def get_center_of_mass(self, points: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        :param points: list of (x, y) coordinates
        :return: new (x, y) coordinate, which corresponds to center of mass
        """
        count: int = len(points)
        assert (count > 0)
        x: float = 0
        y: float = 0
        for i, j in points:
            x += i
            y += j
        return (x / count), (y / count)

    def junction_can_be_removed(self, junction_id: str) -> bool:
        """
        Only junctions with 2 in routes, 2 out routes or with 1 in route, 1 out route,
        can be removed from graph
        e.g. A ----> B ---> C, B can be removed
        e.g. A <----> B <---> C, B can be removed

        :param junction_id: to be checked
        :return: True if junction can be replaced, false otherwise
        """
        junction: Junction = self.skeleton.junctions[junction_id]
        in_routes: Set[Route] = set(junction.get_in_routes())
        out_routes: Set[Route] = set(junction.get_out_routes())
        length_in: int = len(in_routes)
        length_out: int = len(out_routes)
        if (length_in == 2 == length_out) or (length_in == 1 == length_out):
            overlapping_edges: Set[str] = set()
            # Check if traveling on different in_routes goes trough same edges
            for in_route in in_routes:
                for out_route in junction.travel(in_route):
                    edges: Set[str] = set(edge.attributes["id"] for edge in out_route.edge_list)
                    # Edges overlap, cannot be replaced
                    if len(edges & overlapping_edges) != 0:
                        return False
                    overlapping_edges |= edges
            return True
        return False
