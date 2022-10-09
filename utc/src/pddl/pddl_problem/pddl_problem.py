from utc.src.pddl.pddl_problem.pddl_struct import PddlStruct
from utc.src.pddl.pddl_problem.pddl_network import PddlNetwork
from utc.src.pddl.pddl_problem.pddl_vehicle import PddlVehicle
from utc.src.file_system import MyFile, FilePaths


class PddlProblem(PddlStruct):
    """
    Class extending PddlStruct by ':domain', 'problem', ':metric',
    holds other classes defining pddl problem files, provides
    methods to create pddl problem files, functions as
    interface for specific pddl problems.
    """
    def __init__(self):
        super().__init__()
        # Pddl attributes
        self.problem_name: str = ""
        self.domain: str = ""
        self.metric: str = ""
        # Other classes defining pddl problem file
        self.pddl_network: PddlNetwork = None
        self.pddl_vehicle: PddlVehicle = None
        self.initialize_problem()

    def initialize_problem(self) -> None:
        """
        Initializes other classes defining pddl problem.

        :return: None
        """
        raise NotImplementedError("Method: 'initialize_problem' must be implemented by children of PddlProblem")

    # ------------------------------------ Setters ------------------------------------

    def set_problem_name(self, problem_name: str) -> None:
        """
        :param problem_name: name of problem (doesnt have to be same as file name)
        :return: None
        """
        self.problem_name = problem_name

    def set_domain(self, domain: str) -> None:
        """
        :param domain: name of pddl domain file
        :return: None
        """
        if not MyFile.file_exists(FilePaths.PDDL_DOMAIN.format(domain)):
            return
        self.domain = domain

    def set_metric(self, metric: str) -> None:
        """
        :param metric: metric of pddl problem
        :return: None
        """
        self.metric = metric

    # ------------------------------------ Utils ------------------------------------

    def save(self, file_path: str) -> bool:
        """
        :param file_path: path to file which will be created
        :return: True on success, false otherwise
        """
        raise NotImplementedError("Method: 'save' must be implemented by children of PddlProblem")

    # ------------------------------------ Magic Methods ------------------------------------

    def __str__(self) -> str:
        """
        :return: Pddl problem file -> https://planning.wiki/ref/pddl/problem
        """
        ret_val: str = "(define\n"
        ret_val += f"(problem {self.problem_name})\n"
        ret_val += f"(:domain {self.domain})\n"
        ret_val += super().__str__()
        if self.metric:
            ret_val += f"(:metric {self.metric})\n"
        return ret_val + ")"
