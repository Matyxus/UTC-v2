from Project.Pddl.Domain.problem import Problem, Skeleton
from Project.Pddl.Domain.Utils import Capacity


class Utc(Problem):
    """ Class creating problem.pddl files for utc.pddl domain """
    def __init__(self):
        super().__init__()
        self.car_id: int = 0  # Variable to count number of cars
        self.capacity: Capacity = Capacity()
        self.set_domain("utc")
        self.set_metric("minimize (total-cost)")
        self.add_predicate("(= (total-cost) 0)")  # Initial situation -> no penalization

    def add_car(self, from_junction_id: str, to_junction_id: str) -> None:
        """
        Adds car

        :return: None
        """
        self.add_object(f"car{self.car_id}", "car")
        self.add_predicate(f"(at car{self.car_id} {self.junction_mapping[from_junction_id]})")  # Initial position
        self.add_predicate(f"(togo car{self.car_id} {self.junction_mapping[to_junction_id]})")  # Destination pos
        self.add_goal_predicate(f"(at car{self.car_id} {self.junction_mapping[to_junction_id]})")  # Goal position
        self.car_id += 1

    def add_network(self, skeleton: Skeleton) -> None:
        """
        :param skeleton: of graph
        :return: None
        """
        super().add_network(skeleton)
        # Add road capacity
        for predicate in self.capacity.road_to_predicates(skeleton):
            self.add_predicate(predicate)
        for i in range(self.capacity.max_capacity+1):
            self.add_object(f"use{i}", "use")


