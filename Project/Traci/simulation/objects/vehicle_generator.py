from Project.Traci.simulation.objects.vehicle import Vehicle
from Project.Traci.simulation.objects.bst import BST
from Project.Simplify.Components import Graph, Route
from typing import Dict, List
import random


class VehicleGenerator:
    """ """
    def __init__(self, graph: Graph):
        # -------------- Random --------------
        self.SEED: int = 42
        random.seed(self.SEED)
        # -------------- Graph --------------
        self.graph: Graph = graph
        # Recording found shortest paths
        self.road_paths: Dict[str, Dict[str, str]] = {
            # from_junction_id : {to_junction_id : route_id, ...}, ...
        }
        # -------------- Routes & vehicles --------------
        self.routes: List[Route] = []
        self.vehicles_bst: BST = BST()

    # -------------------------------------------- Vehicles --------------------------------------------

    def add_vehicles(self, from_junction_id: str, to_junction_id: str, amount: int, depart_time: int) -> None:
        """
        Creates cars and appends them to binary search tree (sorted by depart time),
        which will later get saved into '.ruo.xml' file.

        :param from_junction_id: starting junction of cars
        :param to_junction_id: destination junction of cars
        :param amount: number of cars to create (>0)
        :param depart_time: time of departure (>=0)
        :return: None
        """
        if not amount > 0:
            print(f"Argument 'amount' must be greater than 0, got: {amount}!")
            return
        elif from_junction_id not in self.graph.skeleton.junctions:
            print(f"Argument 'from_junction_id' must be existing junction id, got: {from_junction_id}!")
            return
        elif to_junction_id not in self.graph.skeleton.junctions:
            print(f"Argument 'to_junction_id' must be existing junction id, got: {to_junction_id}!")
            return
        elif not depart_time >= 0:
            print(f"Argument 'depart' must be non-negative number, got: {depart_time}!")
            return
        # Find route
        route_id: str = self.get_path(from_junction_id, to_junction_id)
        if not route_id:
            return
        # Add vehicles
        for i in range(amount):
            temp: Vehicle = Vehicle()
            temp.set_route(route_id)
            temp.set_depart(depart_time)
            self.vehicles_bst.binary_insert(temp)

    # -------------------------------------------- Flows --------------------------------------------

    # Types of Flows, uniform, random, exponential, ....
    # Improve with numpy for performance!

    def random_flow(
            self, from_junction_id: str, to_junction_id: str, minimal: int,
            maximal: int, period: int, start_time: int, end_time: int
            ) -> None:
        """
        Randomly generates between minimal and maximal cars every period, starting
        from start_time and ending at end_time.

        :param from_junction_id:  starting junction of cars
        :param to_junction_id: destination junction of cars
        :param minimal: amount of cars to be sent
        :param maximal: maximal amount of cars to be sent
        :param period: time (seconds) over which vehicles are sent
        :param start_time: of flow (seconds)
        :param end_time: of flow (seconds)
        :return: None
        """
        print("Adding random flow")
        assert (end_time > start_time >= 0)
        assert (maximal >= minimal >= 1)
        duration: int = (end_time - start_time)
        if ((maximal + minimal) / 2) * int(duration / period) > 10000:
            print("Generating over 10 000 vehicles, returning ....!")
            return
        route_id: str = self.get_path(from_junction_id, to_junction_id)
        if not route_id:
            return
        # For every period add cars to vehicle list
        for i in range(int(duration / period)):
            current_time: int = start_time + (i * period)
            end_time: int = current_time + period
            # Add randomly chosen number of cars to list
            for car in range(random.randint(minimal, maximal)):
                vehicle: Vehicle = Vehicle()
                vehicle.set_route(route_id)
                # Randomly select departure time
                vehicle.set_depart(random.randint(current_time, end_time))
                self.vehicles_bst.binary_insert(vehicle)
        # print(f"Random flow generated: {len(vehicles)} vehicles")

    # ------------------------------------------ Utils  ------------------------------------------

    def get_path(self, from_junction_id: str, to_junction_id: str) -> str:
        """
        :param from_junction_id: starting junction
        :param to_junction_id: destination junction
        :return: id of route, None if it does not exist
        """
        assert (self.graph is not None)
        if from_junction_id in self.road_paths and to_junction_id in self.road_paths[from_junction_id]:
            return self.road_paths[from_junction_id][to_junction_id]  # Get route from already found routes
        path: Route = self.graph.shortest_path.a_star(from_junction_id, to_junction_id)[1]
        if path is None:
            print(f"Path between {from_junction_id} and {to_junction_id} does not exist!")
            return ""
        # Record path
        if from_junction_id not in self.road_paths:
            self.road_paths[from_junction_id] = {}
        self.road_paths[from_junction_id][to_junction_id] = path.attributes["id"]
        self.routes.append(path)
        return path.attributes["id"]

    def set_graph(self, graph: Graph) -> None:
        """

        :param graph: Graph Class to be set as current
        :return: None
        """
        self.graph = graph


