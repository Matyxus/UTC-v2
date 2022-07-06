from Project.Pddl.Domain.problem_generator import ProblemGenerator


# UTC -> Urban Traffic Control
class UtcProblem(ProblemGenerator):
    """ Class creating problem.pddl files for utc.pddl domain """
    def __init__(self):
        super().__init__()

    def init_pddl_attributes(self) -> None:
        print("Initializing attributes")
        self.set_domain("utc")  # utc domain
        self.set_metric("minimize (total-cost)")  # Minimization of traveling cost
        self.add_predicate("(= (total-cost) 0)")  # Initial situation current cost is 0
        self.vehicles_pddl["object"] = {}  # Add vehicle object group
        self.vehicles_pddl["object"]["car"] = []
        self.vehicles_pddl["init"] = []
        self.vehicles_pddl["goal"] = []

    def add_car(self, car_id: str, from_junction_id: str, to_junction_id: str) -> None:
        """
        :param car_id: id of car (corresponds to id of car in .rout.xml file)
        :param from_junction_id: starting junction
        :param to_junction_id: ending junction
        :return: None
        """
        self.vehicles_pddl["object"]["car"].append(car_id)
        self.vehicles_pddl["init"].append(f"(at {car_id} j{from_junction_id})")  # Initial position
        self.vehicles_pddl["init"].append(f"(togo {car_id} j{to_junction_id})")  # Destination pos
        self.vehicles_pddl["goal"].append(f"(at {car_id} j{to_junction_id})")  # Goal position
