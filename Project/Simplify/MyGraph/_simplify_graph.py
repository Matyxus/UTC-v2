from typing import List, Set, Tuple, Dict
from numpy import array, average
from Project.Simplify.Components import Route, Junction
# Do not import alone, methods of Graph defined in graph.py


def simplify_junctions(self, plot: bool) -> None:
    """
    Finds junctions, that may be removed, e.g.
    A ----> B ---- > C (B can be removed),
    A <---> B <----> C (B can be removed),
    Takes out_route from B and merges it with in_route to B,
    for all out_routes, in_routes,
    should be called before simplify_roundabouts

    :param plot: bool, if plot should be displayed
    :return: None
    """
    print("Simplifying junctions")
    # Junctions that cannot be removed
    non_removable: Set[str] = (self.starting_junctions | self.ending_junctions)
    for roundabout in self.roundabouts:
        non_removable |= set(roundabout)
    connections: Dict[str, List[int]] = {}
    assert ((self.junctions.keys() & non_removable) == non_removable)
    # Find junctions that can be removed
    for junction_id in (self.junctions.keys() ^ non_removable):
        if self.junction_can_be_removed(junction_id):
            connections[junction_id] = []
    # Among junctions to be removed, find in_routes that are from junction
    # which is not removable, those without such routes are connected to another
    # removable junction
    for junction_id in connections.keys():
        for in_route_id in self.junctions[junction_id].get_in_routes():
            from_junction_id: str = self.route_manager.get_start(in_route_id)
            if from_junction_id not in connections:
                connections[junction_id].append(in_route_id)
    print("Merging routes")
    for junction_id, in_routes in connections.items():
        for in_route_id in in_routes:
            replacing_junction_id: str = self.route_manager.get_start(in_route_id)
            # Find route from junction before this one
            route: Route = self.route_manager.find_route(replacing_junction_id, junction_id)
            current_route_id: int = route.id
            # print(f"Starting to merge route: {route}, starting at junction: {junction_id}")
            assert (route is not None)
            # While we are traversing among removable junctions, connect routes
            destination_junction_id: str = self.route_manager.get_destination(current_route_id)
            assert (destination_junction_id == junction_id)  # Sanity check
            while destination_junction_id in connections:
                # print(f"Checking junction: {destination_junction_id}")
                assert (len(self.junctions[destination_junction_id].travel(current_route_id)) == 1)
                # There can only be one route, that's why junction can be removed
                out_route_id: int = self.junctions[destination_junction_id].travel(current_route_id)[0]
                route |= self.routes.pop(out_route_id)  # Remove route, merge it
                current_route_id = out_route_id  # Move route id to last merged one
                destination_junction_id: str = self.route_manager.get_destination(route.id)
            # Change incoming route of last Junction of current route, to be the same as current route.id
            self.junctions[destination_junction_id].replace_in_route(current_route_id, route.id)
            # print(f"Final route: {route}")
    print("Finished merging routes")
    # Remove junctions
    removed_junctions: List[Junction] = [self.junctions.pop(junction_id) for junction_id in connections]
    # ------------------ Plot ------------------
    if plot:
        fig, ax = self.default_plot()
        for junction in removed_junctions:
            junction.plot(ax, color="red")
        self.add_label("o", "red", "Removed Junctions")
        self.make_legend(1)
        self.show_plot()
    print("Finished simplifying junctions")
    self.route_count = len(self.routes)


def simplify_roundabouts(self, plot: bool) -> None:
    """
    Removes junctions forming roundabout, replaces them
    with new node (at center of mass position), adds new routes,
    removes previous routes between roundabout nodes,
    should be called after simplify_junctions

    :param plot: bool, if plot should be displayed
    :return: None
    """
    print(f"Simplifying roundabouts: {self.roundabouts}")
    while len(self.roundabouts) != 0:
        # ---------------- Variable setup ----------------
        roundabout: List[str] = self.roundabouts.pop()
        roundabout_points: List[Tuple[float, float]] = []
        roundabout_routes: Set[int] = set()  # Routes on roundabout
        in_routes: Set[int] = set()  # Routes connection to roundabout
        out_routes: Set[int] = set()  # Routes coming out of roundabout
        for junction_id in roundabout:
            junction: Junction = self.junctions[junction_id]
            roundabout_points.append(junction.get_position())
            # Find all entry points to roundabout
            for in_route_id in junction.get_in_routes():
                # Get edges going to roundabout
                if not (self.route_manager.get_start(in_route_id) in roundabout):
                    in_routes.add(in_route_id)
            # Find all exit points of roundabout
            for out_route_id in junction.get_out_routes():
                # Get route going from roundabout
                if not (self.route_manager.get_destination(out_route_id) in roundabout):
                    out_routes.add(out_route_id)
                else:
                    roundabout_routes.add(out_route_id)
        # ---------------- Setup new junction ----------------
        new_point: tuple = get_center_of_mass(roundabout_points)
        new_junction_id: str = ("roundabout-replace-" + "-".join(roundabout))
        new_junction: Junction = Junction({"id": new_junction_id, "x": new_point[0], "y": new_point[1]})
        new_junction.marker_size = 10
        new_junction.color = "yellow"
        print(f"Creating new junction: {new_junction_id}")
        # ---------------- Add new routes from new junction ----------------
        for in_route_id in in_routes:
            starting_junction_id: str = self.route_manager.get_destination(in_route_id)
            current_junction: Junction = self.junctions[starting_junction_id]
            assert (starting_junction_id in roundabout)
            new_route: Route = self.route_manager.get_new_route()
            current_out_routes: Set[int] = set(current_junction.travel(in_route_id))
            # Since we entered roundabout now, the only route now leads to another roundabout junction
            assert (len(current_out_routes) == 1)  # Sanity check
            route_id: int = current_out_routes.pop()
            assert (self.route_manager.get_destination(route_id) in roundabout)  # Sanity check
            new_route |= self.routes[route_id]  # Modify current route
            current_junction_id: str = self.route_manager.get_destination(route_id)
            while current_junction_id != starting_junction_id:
                current_junction = self.junctions[current_junction_id]
                # print(f"Currently on junction: {current_junction_id}")
                # Get all out coming routes
                current_out_routes = set(current_junction.get_out_routes())
                # Routes going out of current roundabout junction
                routes_out_roundabout: Set[int] = (current_out_routes & out_routes)
                # Create new routes for each path leading out of roundabout
                for route_id in routes_out_roundabout:
                    new_route_out: Route = (self.route_manager.get_new_route() | new_route)
                    new_route_out |= self.routes[route_id]
                    # Add new route to junction
                    new_junction.add_connection(in_route_id, new_route_out.id)
                    self.route_manager.add_route(new_route_out)
                    # Add new incoming route to connected junction
                    destination: Junction = self.junctions[self.route_manager.get_destination(new_route_out.id)]
                    destination.neighbours[new_route_out.id] = destination.neighbours[route_id]
                assert (len(current_out_routes ^ routes_out_roundabout) == 1)
                route_id = (current_out_routes ^ routes_out_roundabout).pop()
                # print(f"Route: {self.routes[route_id]}")
                current_junction_id = self.route_manager.get_destination(route_id)
                new_route |= self.routes[route_id]  # Move to next roundabout junction
                # print(f"New route: {new_route}")
            current_junction = self.junctions[current_junction_id]
            assert (current_junction_id == starting_junction_id)
            # Now current_junction is equal to starting_junction
            # Check if starting junction has any out edges, add them as new route
            for route_id in (set(current_junction.get_out_routes()) & out_routes):
                new_route_out: Route = (self.route_manager.get_new_route() | new_route)
                new_route_out |= self.routes[route_id]
                # print(f"New route added to junction: {new_route_out}")
                new_junction.add_connection(in_route_id, new_route_out.id)
                self.route_manager.add_route(new_route_out)
                # Add new incoming route to connected junction
                destination: Junction = self.junctions[self.route_manager.get_destination(new_route_out.id)]
                destination.neighbours[new_route_out.id] = destination.neighbours[route_id]
        # ---------------- Remove ----------------
        # Remove routes on roundabout
        for route_id in roundabout_routes:
            self.routes.pop(route_id)
        # Remove routes out of roundabout, connection on junctions
        for route_id in out_routes:
            destination: Junction = self.junctions[self.route_manager.get_destination(route_id)]
            destination.remove_in_route(route_id)
            self.routes.pop(route_id)
        # Set each out coming route of roundabout attribute["from"] as new junction
        for route_id in new_junction.get_out_routes():
            self.edges[self.routes[route_id].first_edge()].attributes["from"] = new_junction_id
        # Set each incoming edge of roundabout, attribute["to"] as new junction
        for route_id in in_routes:
            self.edges[self.routes[route_id].last_edge()].attributes["to"] = new_junction_id
        # Remove junctions forming roundabout
        removed_junctions: List[Junction] = [self.junctions.pop(junction_id) for junction_id in roundabout]
        self.route_count -= len(removed_junctions)
        # ---------------- Plot ----------------
        if plot:
            fig, ax = self.default_plot()
            # Remove junctions from roundabout
            for junction in removed_junctions:
                junction.plot(ax, color="red")
            new_junction.plot(ax)
            self.add_label("o", "red", "Roundabout junctions")
            self.add_label("o", new_junction.color, "New junction")
            self.make_legend(2)
            self.show_plot()
        # Add new junction
        self.junctions[new_junction.attributes["id"]] = new_junction
    print("Done simplifying roundabouts")

# ----------------------------------- Utils -----------------------------------


def get_center_of_mass(points: list) -> tuple:
    """
    :param points: list of (x, y) coordinates
    :return: new (x, y) coordinate, which corresponds to center of mass
    """
    assert (len(points) > 0)
    return tuple(average(array(points), axis=0))


def junction_can_be_removed(self, junction_id: str) -> bool:
    """
    Only junctions with 2 in routes, 2 out routes or with 1 in route, 1 out route,
    can be removed from graph
    e.g. A ----> B ---> C, B can be removed
    e.g. A <----> B <---> C, B can be removed

    :param junction_id: to be checked
    :return: True if junction can be replaced, false otherwise
    """
    junction: Junction = self.junctions[junction_id]
    in_routes: Set[int] = set(junction.get_in_routes())
    out_routes: Set[int] = set(junction.get_out_routes())
    length_in: int = len(in_routes)
    length_out: int = len(out_routes)
    if (length_in == 2 == length_out) or (length_in == 1 == length_out):
        overlapping_edges: Set[str] = set()
        # Check if traveling on different in_routes goes trough same edges
        for in_route_id in in_routes:
            for out_route_id in junction.travel(in_route_id):
                edges: Set[str] = set(self.routes[out_route_id].edge_list)
                # Edges overlap, cannot be replaced
                if len(edges & overlapping_edges) != 0:
                    return False
                overlapping_edges |= edges
        return True
    return False
