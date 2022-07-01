from Project.Simplify.graph_modules.graph_module import GraphModule
from Project.Simplify.components import Skeleton, Route
from typing import List, Dict


class ToPddl(GraphModule):
    """ Class converting skeleton of graph to pddl representation """
    def __init__(self, skeleton: Skeleton = None):
        super().__init__(skeleton)
        self.CAR_LENGTH: float = 4.5  # Average car length (in meters)
        self.MIN_GAP: float = 2.5  # Minimal gap (meters) between vehicles, as defined in SUMO
        # self.FOLLOWING_DISTANCE: float = 2.0  # Safe following distance (in seconds), depends on speed
        self.max_capacity: int = 0  # Maximal capacity, necessary for 'use' predicate
        # ------------------- DENSITY CONSTANTS -------------------
        # Light traffic -> (maximum_road_capacity * LIGHT_CAPACITY_THRESHOLD), similar for medium/heavy
        self.LIGHT_CAPACITY_THRESHOLD: float = 0.35  # Low -> Medium (%)
        self.MEDIUM_CAPACITY_THRESHOLD: float = 0.4  # Medium -> Heavy (Up to 75 = LOW + MEDIUM % of capacity)
        self.HEAVY_CAPACITY_THRESHOLD: float = 0.25  # Heavy (Over LIGHT+MEDIUM capacity) -> Congested (over 100%)
        assert (self.LIGHT_CAPACITY_THRESHOLD + self.MEDIUM_CAPACITY_THRESHOLD + self.HEAVY_CAPACITY_THRESHOLD == 1)
        # Penalization multipliers for higher than light capacity
        # self.LIGHT_CAPACITY_MULTIPLIER: float = 1
        self.MEDIUM_CAPACITY_MULTIPLIER: float = 10
        self.HEAVY_CAPACITY_MULTIPLIER: float = 100

    def convert(self, capacity: bool = False) -> dict:
        """
        :param capacity: bool, if pddl representation should include road capacity + predicate 'next'
        for counting number of cars on road
        :return: dictionary containing 'init' and 'object' pddl representation of road network
        """
        assert (self.skeleton is not None)
        ret_val: dict = {
            "init": [],
            "object": {
                "junction": [],
                "road": []
            }
        }
        # --------------- Add basic network  ---------------
        # Add junctions
        for junction_id in self.skeleton.junctions.keys():
            ret_val["object"]["junction"].append(f"j{junction_id}")
        # Add roads and connections between junctions
        for route_id, route in self.skeleton.routes.items():
            ret_val["object"]["road"].append(f"r{route_id}")
            # Add connections between junctions and routes  -> (connected from_junction_id road_id to_junction_id)
            ret_val["init"].append(f"(connected j{route.get_start()} r{route_id} j{route.get_destination()})")
        #  --------------- Extend network ---------------
        if capacity:
            ret_val["init"].extend(self.extended_network())
            ret_val["object"]["next"] = [f"use{i}" for i in range(self.max_capacity+1)]
        return ret_val

    def extended_network(self) -> List[str]:
        """
        Extends basic road network by road capacity, traffic thresholds,
        'next' predicate for counting number of cars on road

        :return: list of predicates
        """
        predicates: List[str] = []
        # Add predicates: 'length', 'use', 'cap', 'using', 'light, medium, heavy'
        for route_id, route in self.skeleton.routes.items():
            capacity: int = self.calculate_capacity(route)
            assert (capacity > 0)
            self.max_capacity = max(capacity, self.max_capacity)
            [predicates.append(predicate) for predicate in self.calculate_density(route)]
            [predicates.append(predicate) for predicate in self.calculate_thresholds(capacity, route_id)]
            predicates.append(f"(cap r{route_id} use{capacity})")  # Maximum capacity (after it becomes congested)
            predicates.append(f"(using r{route_id} use0)")  # Current number of cars = 0
        # Add 'use' predicate (to calculate how many cars are on road)
        for i in range(self.max_capacity):
            predicates.append(f"(next use{i} use{i + 1})")
        return predicates

    def calculate_thresholds(self, capacity: int, route_id: int) -> List[str]:
        """
        :param capacity: of route
        :param route_id: of route
        :return: List of predicates -> (light/medium/heavy route_id useX)
        """
        predicates: List[str] = [f"(light r{route_id} use0)"]  # Default for every route (-> 0 cars on road)
        index: int = 1
        for density_type, density in self.get_thresholds(capacity).items():
            for _ in range(density):
                predicates.append(f"({density_type} r{route_id} use{index})")
                index += 1
        return predicates

    def calculate_density(self, route: Route) -> List[str]:
        """
        :param route: to be calculated
        :return: List of predicates -> for traffic density on route
        """
        predicates: List[str] = []
        cost: float = (  # route_length / average_speed
                route.traverse()[0] /
                (sum([edge.attributes["speed"] for edge in route.edge_list]) / len(route.edge_list))
        )
        # In case route is too short (can be traveled under second)
        if cost < 1:
            cost = 1
        predicates.append(f"(= (length-light r{route.id}) {int(cost)})")
        predicates.append(f"(= (length-medium r{route.id}) {int(cost * self.MEDIUM_CAPACITY_MULTIPLIER)})")
        predicates.append(f"(= (length-heavy r{route.id}) {int(cost * self.HEAVY_CAPACITY_MULTIPLIER)})")
        return predicates

    def calculate_capacity(self, route: Route) -> int:
        """
        Calculates theoretical capacity of route,
        as maximal number of cars possible on route

        :param route: to be calculated
        :return: capacity, 0 if error occurs
        """
        if route is None or len(route.edge_list) == 0:
            print(f"Route: {route} is invalid object!")
            return 0
        # Find how many lanes routes has, if there is edge with only 1 lane (capacity multiplier is 1)
        lane_multiplier: int = max(min([len(edge.lanes.keys()) for edge in route.edge_list]), 1)
        # Route_length / (car_length + gap)
        capacity: int = max(int(route.traverse()[0] / (self.CAR_LENGTH + self.MIN_GAP)), 1)
        return capacity * lane_multiplier

    def get_thresholds(self, capacity: int) -> Dict[str, int]:
        """
        :param capacity: of road
        :return: Mapping of traffic density to number of cars
        """
        # At least one car has to be on as light-traffic (minimum)
        light_cap: int = max(round(capacity * self.LIGHT_CAPACITY_THRESHOLD), 1)
        medium_cap: int = round(capacity * self.MEDIUM_CAPACITY_THRESHOLD)
        heavy_cap: int = capacity - light_cap - medium_cap
        if capacity - light_cap < 0:
            medium_cap = 0
            heavy_cap = 0
        elif capacity - light_cap - medium_cap < 0:
            heavy_cap = 0
        ret_val: Dict[str, int] = {
            "light": light_cap,
            "medium": medium_cap,
            "heavy": heavy_cap,
        }
        assert (light_cap + medium_cap + heavy_cap == capacity)
        return ret_val
