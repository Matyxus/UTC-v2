from utc.src.simulator.vehicle.generators.vehicle_generator import VehicleGenerator, Graph, Vehicle
from typing import Tuple, Iterator, Dict
import numpy as np


class VehicleFlows(VehicleGenerator):
    """ Class serving for generating vehicles """

    def __init__(self, graph: Graph = None):
        super().__init__(graph)
        print("Initialized VehicleFlows")

    # -------------------------------------------- Interface --------------------------------------------

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
        if not self.check_args(from_junction_id, to_junction_id, start_time=start_time, end_time=end_time):
            return
        elif not maximal >= minimal:
            print(f"Expected argument 'maximal' to be higher or equal to 'minimal', got: {maximal} < {minimal} !")
            return
        elif not minimal >= 1:
            print(f"Expected arguments 'minimal' to be at least one, got: {minimal} !")
            return
        route_id: str = self.get_path(from_junction_id, to_junction_id)
        self.generators.append(self.generate_random_flow((minimal, maximal), period, route_id, (start_time, end_time)))

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
        # Check args
        if not self.check_args(from_junction_id, to_junction_id, vehicle_count, start_time, end_time):
            return
        route_id: str = self.get_path(from_junction_id, to_junction_id)
        print("Generating uniform flow..")
        self.generators.append(self.generate_uniform_flow((start_time, end_time), route_id, vehicle_count))

    # -------------------------------------------- Generators --------------------------------------------

    @staticmethod
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
        for vehicle_count in np.random.randint(vehicle_interval[0], vehicle_interval[1] + 1, episodes):
            starting_time += _period
            ending_time += _period
            # Generate random departing times for vehicles
            for depart_time in np.random.randint(starting_time, ending_time, vehicle_count):
                yield Vehicle(depart_time, _route_id)

    @staticmethod
    def generate_uniform_flow(time_interval: Tuple[int, int], route_id: str, vehicle_count: int) -> Iterator[Vehicle]:
        """
        :param time_interval: of vehicles arrival time (start_time, end_time)
        :param route_id: id of route that cars will use
        :param vehicle_count: number of vehicles (equally spaced)
        :return: Iterator of vehicles
        """
        for depart_time in np.linspace(time_interval[0], time_interval[1], vehicle_count):
            yield Vehicle(round(depart_time), route_id)

    # -------------------------------------------- Utils --------------------------------------------

    def get_methods(self) -> Dict[str, callable]:
        return {"add-random-flow": self.random_flow, "add-uniform-flow": self.uniform_flow}
