from Project.Pddl.pddl_problem import PddlProblem
from Project.Pddl.utc_problem.utc_network import UtcNetwork
from Project.Pddl.utc_problem.utc_vehicle import UtcVehicle


class UtcProblem(PddlProblem):
    """
    Class defining UrbanTrafficControl pddl problem
    """
    def __init__(self):
        super().__init__()
        self.set_domain("utc")  # Default domain

    def initialize_problem(self) -> None:
        """
        Initializes other classes defining pddl problem.

        :return: None
        """
        self.add_init_state("(= (total-cost) 0)")  # Initial situation current cost is 0
        self.set_metric("minimize (total-cost)")  # Minimization of traveling cost
        self.pddl_vehicle = UtcVehicle()
        self.pddl_network = UtcNetwork()

    def save(self, file_path: str) -> None:
        # Checks
        if not self.problem_name:
            print("Problem name is not set, cannot save problem!")
            return
        elif not self.domain:
            print("Domain name is not set, cannot save problem!")
            return
        print(f"Creating pddl problem: {self.problem_name} in: {file_path}")
        tmp: PddlProblem = self | (self.pddl_network | self.pddl_vehicle)
        with open(file_path, "w") as pddl_problem_file:
            pddl_problem_file.write(str(tmp))
        print(f"Successfully created pddl problem file")


# For testing purposes
if __name__ == "__main__":
    temp: UtcProblem = UtcProblem()

