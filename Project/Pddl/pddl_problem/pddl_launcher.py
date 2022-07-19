from Project.Pddl.pddl_problem.pddl_problem import PddlProblem
from Project.Pddl.pddl_problem.pddl_result import PddlResult
from Project.Simplify.components import Graph
from Project.Utils.constants import PATH
from typing import List, Callable, Optional, Tuple


class PddlLauncher:
    """ Class that implements interface methods for generating pddl problems/results """

    def __init__(self, shell: Callable[[str, Optional[int]], Tuple[str, bool]]):
        """
        :param shell: function able to pass commands into shell/cmd (expecting 'UserInterface.run_command')
        """
        self.graph: Graph = None
        # -------------- Pddl --------------
        self.pddl_problem: PddlProblem = None
        self.pddl_result: PddlResult = None
        # function able to call commands into shell/cmd (expecting 'UserInterface.run_command')
        self.shell: callable = shell

    def generate_problems(self, scenario: str, network: str = "default", *args, **kwargs) -> None:
        """

        :param scenario: name of scenario (must contain empty '/problems' folder)
        :param network: name of network, on which problem will be generated (if default, name of network
        is extracted from '.ruo.xml' file)
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("")

    def generate_results(self, scenario: str, planner: str, shell: callable,  *args, **kwargs) -> None:
        """

        :param scenario:
        :param planner:
        :param shell: function able to call commands into shell/cmd
        :param args: additional arguments
        :param kwargs: additional arguments
        :return: None
        """
        raise NotImplementedError("")

    def generate_scenario(self, scenario: str, *args, **kwargs) -> None:
        """
        :param scenario:
        :param args: additional arguments
        :param kwargs: additional arguments
        :return:
        """
        raise NotImplementedError("")

    # ---------------------------------------------- Utils ----------------------------------------------

    def get_planner_args(self, domain: str, scenario: str, problem: str, result: str) -> List[str]:
        """
        :param domain: name of domain (extension added automatically)
        :param scenario: name of scenario
        :param problem: name of problem file (extension added automatically)
        :param result: name of resulting file (extension added automatically)
        :return: absolute paths to domain, problem, result files (expecting planners to use these arguments)
        """
        # Call planner
        planner_args: List[str] = [
            PATH.PDDL_DOMAINS.format(domain),  # Domain
            PATH.TRACI_SCENARIOS_PROBLEMS.format(scenario, problem),  # Problem
            PATH.TRACI_SCENARIOS_RESULTS.format(scenario, result)  # Result
        ]
        return planner_args
