from utc.src.simulator.simulation.objects.vehicle import Vehicle
from utc.src.simulator.simulation.objects.bst import BST, Element
from utc.src.graph.components import Graph, Route
from typing import Dict, List, Tuple, Iterator
import numpy as np


class VehicleGenerator:
    """ Class serving for generating vehicles """
    
    def __init__(self, graph: Graph):
        # -------------- Random --------------
        self.SEED: int = 42
        np.random.seed(self.SEED)
        # -------------- Graph --------------
        self.graph: Graph = graph
        # Recording found shortest paths
        self.road_paths: Dict[str, Dict[str, str]] = {
            # from_junction_id : {to_junction_id : route_id, ...}, ...
        }
        # -------------- Routes & vehicles --------------
        self.routes: List[Route] = []
        self.vehicles_bst: BST = BST()
        self.generators: List[Iterator[Vehicle]] = []

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
        self.generators.append((Vehicle(depart_time, route_id) for _ in range(amount)))

    # -------------------------------------------- Flows --------------------------------------------

    def random_flow(
            self, from_junction_id: str, to_junction_id: str, minimal: int,
            maximal: int, period: int, start_time: int, end_time: int
            ) -> None:
        """
        Randomly generates between minimal and maximal cars every period, starting
        from start_time and ending at end_time.

        :param from_junction_id: starting junction of cars
        :param to_junction_id: destination junction of cars
        :param minimal: minimal amount of cars to be sent
        :param maximal: maximal amount of cars to be sent
        :param period: time (seconds) over which vehicles are sent
        :param start_time: of flow (seconds)
        :param end_time: of flow (seconds)
        :return: None
        """
        print("Generating random flow..")
        # ---------------------- Checks ----------------------
        assert (end_time > start_time >= 0)
        assert (maximal >= minimal >= 1)
        route_id: str = self.get_path(from_junction_id, to_junction_id)
        if not route_id:
            return

        def generate_random_flow(
                vehicle_interval: Tuple[int, int], _period: int,
                _route_id: str, time_interval: Tuple[int, int]
                ) -> Iterator[Vehicle]:
            """
            :param vehicle_interval: minimal and maximal value of vehicles
            :param _period: how often should vehicles be generated
            :param _route_id: id of route used by vehicles
            :param time_interval: of vehicles arrival time (start_time, end_time)
            :return: Iterator of vehicles
            """
            starting_time: int = time_interval[0] - _period
            ending_time: int = time_interval[0]
            # Generate random vehicle_counts N times (generating_time / period)
            episodes: int = int((time_interval[0] + time_interval[1]) / _period)
            for vehicle_count in np.random.randint(vehicle_interval[0], vehicle_interval[1]+1, episodes):
                starting_time += _period
                ending_time += _period
                # Generate random departing times for vehicles
                for depart_time in np.random.randint(starting_time, ending_time, vehicle_count):
                    yield Vehicle(depart_time, _route_id)
        self.generators.append(generate_random_flow((minimal, maximal), period, route_id, (start_time, end_time)))

    def uniform_flow(
            self, from_junction_id: str, to_junction_id: str,
            vehicle_count: int, start_time: int, end_time: int
            ) -> None:
        """
        :param from_junction_id: starting junction of cars
        :param to_junction_id: destination junction of cars
        :param vehicle_count: number of vehicles (equally spaced)
        :param start_time: of flow (seconds)
        :param end_time: of flow (seconds)
        :return: None
        """
        assert (end_time > start_time >= 0)
        assert (vehicle_count > 0)
        route_id: str = self.get_path(from_junction_id, to_junction_id)
        if not route_id:
            return
        print("Generating uniform flow..")

        def generate_uniform_flow(
                time_interval: Tuple[int, int], _route_id: str, _vehicle_count: int
                ) -> Iterator[Vehicle]:
            """
            :param time_interval: of vehicles arrival time (start_time, end_time)
            :param _route_id: id of route that cars will use
            :param _vehicle_count: number of vehicles (equally spaced)
            :return: Iterator of vehicles
            """
            for depart_time in np.linspace(time_interval[0], time_interval[1], _vehicle_count):
                yield Vehicle(round(depart_time), _route_id)
        self.generators.append(generate_uniform_flow((start_time, end_time), route_id, vehicle_count))

    # -------------------------------------------- Trips --------------------------------------------

    def random_trips(self, vehicle_count: int, start_time: int, end_time: int) -> None:
        """
        Calculates period (vehicles entering network per period) according to formula:
        period = (end_time-start_time) / (network_length / 1000) / vehicle_count,
        randomly selects starting/ending junction to create path vehicles will take.
        ! May take a while, depending on the network size (to find shortest paths) and
        the duration (end_time - start_time) -> number of generate vehicles = (end_time - start_time) / period

        :param vehicle_count: Number of vehicles used in formula to calculate period (vehicles/second)
        :param start_time: starting time of trips
        :param end_time: ending time of trips
        :return: None
        """
        assert (end_time > start_time >= 0)
        assert (vehicle_count > 0)
        print("Generating random trips ...")

        def generate_random_trips(time_interval: Tuple[int, int], _vehicle_count: int) -> Iterator[Vehicle]:
            """
            :param time_interval: of vehicles arrival time (start_time, end_time)
            :param _vehicle_count: number of vehicles
            :return: Iterator of vehicles
            """
            network_length: int = int(sum([
                edge.get_length() * edge.get_lane_count() for edge in self.graph.skeleton.edges.values()
            ]))
            duration: int = (time_interval[1] - time_interval[0])
            period: float = round(duration / (network_length / 1000) / _vehicle_count, 3)
            # Pointers for random.choice (must be a list!)
            starting_junctions_ptr: List[str] = list(self.graph.skeleton.starting_junctions)
            ending_junctions_ptr: List[str] = list(self.graph.skeleton.ending_junctions)
            for i in range(int(duration / period)):
                # Randomly choose route
                route_id: str = ""
                while not route_id:
                    route_id = self.get_path(
                        np.random.choice(starting_junctions_ptr),
                        np.random.choice(ending_junctions_ptr),
                        message=False
                    )
                yield Vehicle(i*period, route_id)
        self.generators.append(generate_random_trips((start_time, end_time), vehicle_count))

    # ------------------------------------------ Utils  ------------------------------------------

    def save(self, root: Element) -> None:
        """
        Appends routes, vehicles from created generators to BST for sorting,
        afterwards to root of xml file

        :param root: of '.ruo.xml' file
        :return: None
        """
        # Generate vehicles and sort them in BST
        print(f"Sorting vehicles by depart time using BinarySearchTree...")
        for generator in self.generators:
            for vehicle in generator:
                self.vehicles_bst.binary_insert(vehicle)
        # Add routes before vehicle!
        for route in self.routes:
            root.append(route.to_xml())
        # Add vehicles to xml root
        self.vehicles_bst.sorted_append(self.vehicles_bst.root, root)
        print(f"Added: {len(root.findall('vehicle'))} vehicles")

    def get_path(self, from_junction_id: str, to_junction_id: str, message: bool = True) -> str:
        """
        :param from_junction_id: starting junction
        :param to_junction_id: destination junction
        :param message: bool (true/false) to print "invalid route" if route is not found
        :return: id of route, None if it does not exist
        """
        assert (self.graph is not None)
        if from_junction_id in self.road_paths and to_junction_id in self.road_paths[from_junction_id]:
            return self.road_paths[from_junction_id][to_junction_id]  # Get route from already found routes
        path: Route = self.graph.shortest_path.a_star(from_junction_id, to_junction_id)[1]
        # Record path
        if from_junction_id not in self.road_paths:
            self.road_paths[from_junction_id] = {}
        # Path doesnt exist, record its non existence with empty string
        if path is None:
            if message:
                print(f"Path between {from_junction_id} and {to_junction_id} does not exist!")
            self.road_paths[from_junction_id][to_junction_id] = ""
            return ""
        self.road_paths[from_junction_id][to_junction_id] = path.attributes["id"]
        self.routes.append(path)
        return path.attributes["id"]

