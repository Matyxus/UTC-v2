from Project.Pddl.Domain.problem_generator import ProblemGenerator, Skeleton
from Project.Pddl.Domain.Utils import Network


# UTC -> Urban Traffic Control
class UtcProblem(ProblemGenerator):
    """ Class creating problem.pddl files for utc.pddl domain """
    def __init__(self):
        super().__init__()
        self.car_id: int = 0  # Variable to count number of cars
        self.network: Network = Network()
        self.set_domain("utc")  # utc domain
        self.set_metric("minimize (total-cost)")  # Minimization of traveling cost
        self.add_predicate("(= (total-cost) 0)")  # Initial situation current cost is 0
        self.add_object_group("car")  # Add car object group
        self.add_object_group("use")  # Add use object group (for counting cars on road)

    def add_car(self, amount: int, from_junction_id: str, to_junction_id: str) -> None:
        """
        :param amount: number of cars
        :param from_junction_id: starting junction
        :param to_junction_id: ending junction
        :return: None
        """
        for _ in range(1, amount+1):
            self.add_object(f"car{self.car_id}", "car")
            self.add_predicate(f"(at car{self.car_id} j{from_junction_id})")  # Initial position
            self.add_predicate(f"(togo car{self.car_id} j{to_junction_id})")  # Destination pos
            self.add_goal_predicate(f"(at car{self.car_id} j{to_junction_id})")  # Goal position
            self.car_id += 1

    def add_network(self, skeleton: Skeleton) -> None:
        """
        Extends basic network graph with:\n
        1 ) Road capacity based on current traffic burden (light/medium/heavy)\n
        2 ) Traveling cost based on roads traffic burden\n
        3 ) Capacity threshold for different traffic burden (light -> medium -> heavy -> congested)

        :param skeleton: of graph
        :return: None
        """
        super().add_network(skeleton)
        # Extend basic network by utc domain requirements
        for predicate in self.network.road_to_predicates(skeleton):
            self.add_predicate(predicate)
        # Add counter for cars (maximal is equivalent to maximal capacity)
        for i in range(self.network.max_capacity+1):
            self.add_object(f"use{i}", "use")
