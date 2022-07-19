from Project.Pddl.pddl_problem import PddlNetwork
from Project.Simplify.components import Skeleton, Route
from typing import List, Dict


class UtcNetwork(PddlNetwork):
    """
    Class holding representation of road networks for '.pddl' problem files,
    extends PddlStruct
    """
    def __init__(self):
        # Pddl predicate for counting number of cars on route
        self.use_object_group: str = "use"
        self.use_object: str = "use{0}"
        #
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
        super().__init__()

    def initialize_object(self) -> None:
        """
        :return: None
        """
        super().initialize_object()
        self.add_object_group(self.use_object_group)

    def process_graph(self, skeleton: Skeleton) -> None:
        """
        Creates basic pddl representation of graph\n
        ':init' -> (connected junction_id route_id junction_id),\n
        adds id's of junction to group: junction,\n
        id's of routes to group: road\n
        -> ':object' -> j{junction_id}, ..., - junction\n
        -> ':object' -> r{route_id}, ..., - road

        :param skeleton: of Graph
        :return: None
        """
        super().process_graph(skeleton)
        # Add capacity, cost ..
        #  --------------- Extend network ---------------
        # Add predicates: 'length', 'use', 'cap', 'using', 'light, medium, heavy'
        for route_id, route in skeleton.routes.items():
            capacity: int = self.calculate_capacity(route)
            assert (capacity > 0)
            self.max_capacity = max(capacity, self.max_capacity)
            for predicate in self.calculate_density(route):
                self.add_init_state(predicate)
            for predicate in self.calculate_thresholds(capacity, route_id):
                self.add_init_state(predicate)
            # Maximum capacity (after it becomes congested)
            self.add_init_state(f"(cap {self.route_object.format(route_id)} {self.use_object.format(capacity)})")
            # Current number of cars = 0
            self.add_init_state(f"(using {self.route_object.format(route_id)} {self.use_object.format(0)})")
        # Add 'use', 'next' predicate (to calculate how many cars are on road)
        for i in range(self.max_capacity):
            self.add_init_state(f"(next {self.use_object.format(i)} {self.use_object.format(i+1)})")
            self.add_object(self.use_object_group, self.use_object.format(i))
        self.add_object(self.use_object_group, self.use_object.format(self.max_capacity))

    # ---------------------------------------- Utils ----------------------------------------

    def calculate_thresholds(self, capacity: int, route_id: int) -> List[str]:
        """
        :param capacity: of route
        :param route_id: of route
        :return: List of predicates -> (light/medium/heavy route_id useX)
        """
        # Default for every route (-> 0 cars on road)
        predicates: List[str] = [f"(light {self.route_object.format(route_id)} {self.use_object.format(0)})"]
        index: int = 1
        for density_type, density in self.get_thresholds(capacity).items():
            for _ in range(density):
                predicates.append(
                    f"({density_type} {self.route_object.format(route_id)} {self.use_object.format(index)})"
                )
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

        :param route: which capacity is calculated
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
