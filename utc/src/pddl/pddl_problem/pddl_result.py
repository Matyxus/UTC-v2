from utc.src.graph.components import Skeleton
from utc.src.simulator.scenario import Scenario


class PddlResult:
    """
    Class interpreting pddl result files generated by planners,
    functions as an interface
    """
    def __init__(self, scenario: Scenario, skeleton: Skeleton):
        """
        :param scenario: loaded with routes and config file on which planning
        is done, with correctly set name and folder name
        :param skeleton: skeleton of network
        """
        self.scenario: Scenario = scenario
        self.skeleton: Skeleton = skeleton

    def parse_result(self, result_name: str, *args, **kwargs) -> dict:
        """
        Parses pddl result files, returning dictionary

        :param result_name: name of result file
        :param args: additional arguments
        :param kwargs: additional arguments
        :return:
        """
        raise NotImplementedError("Method 'parse_result' must be implemented by children of PddlResult")

    def results_to_scenario(self, *args, **kwargs) -> bool:
        """
        Converts folder containing pddl result files to '.sumocfg' file (in case
        of more types -> e.g. ".1.pddl", ".2.pddl" creates multiple '.type.sumocfg' files,
        where types does not contain ".pddl")

        :param args: additional arguments
        :param kwargs: additional arguments
        :return: true on success, false otherwise
        """
        raise NotImplementedError("Method 'results_to_scenario' must be implemented by children of PddlResult")
