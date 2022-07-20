from Project.Pddl.pddl_problem.pddl_problem import PddlProblem
from Project.Pddl.pddl_problem.pddl_result import PddlResult
from Project.Traci.scenarios.generators import ConfigGenerator
from Project.Simplify.components import Graph
from Project.Utils.constants import PATH, file_exists, get_file_name
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

    def generate_results(self, scenario: str, planner: str, domain: str, timeout: int = 30, *args, **kwargs) -> None:
        """

        :param scenario: name of scenario
        :param planner: name of planner to be used (must be defined in /Project/Pddl/Utils/constants)
        :param domain: name of pddl domain (must be in /Project/Pddl/Domains)
        :param timeout: seconds given to planner execution
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

    def get_network(self, scenario: str, network: str) -> str:
        """
        :param scenario: name of scenario
        :param network: name of network (if default, extracted from 'simulation.sumocfg')
        :return: name of network (empty string, if its invalid)
        """
        # Error message string
        msg: str = ""
        # Extract network from 'simulation.sumocfg' file
        if network == "default":
            print(f"Network == 'default', extracting name from: {PATH.TRACI_SIMULATION.format(scenario, 'simulation')}")
            if not file_exists(PATH.TRACI_SIMULATION.format(scenario, "simulation")):
                return ""
            temp: ConfigGenerator = ConfigGenerator(config_path=PATH.TRACI_SIMULATION.format(scenario, "simulation"))
            network = get_file_name(temp.get_network_name())
            msg = (
                f"Network: {network} used in simulation "
                f"file: {PATH.TRACI_SIMULATION.format(scenario, 'simulation')} does not exist!"
            )
        if not file_exists(PATH.NETWORK_SUMO_MAPS.format(network), message=(not msg)):
            if msg:
                print(msg)
            return ""
        return network

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
