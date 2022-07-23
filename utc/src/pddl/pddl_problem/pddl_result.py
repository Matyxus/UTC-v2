from typing import List


class PddlResult:
    """
    Class interpreting pddl result files generated by planners,
    functions as an interface
    """
    def __init__(self):
        pass

    def parse_result(self, scenario_name: str, result_name: str) -> dict:
        """
        Parses pddl result files, returning dictionary

        :param scenario_name: name of scenario
        :param result_name: name of result file
        :return:
        """
        raise NotImplementedError("Method 'parse_result' must be implemented by children of PddlResult")

    def results_to_scenario(self, scenario: str, simulation: str, result_files: List[str]) -> None:
        """
        Converts folder containing pddl result files to '.sumocfg' file (in case
        of more types -> e.g. result.pddl.1, result.pddl.2 creates multiple '_type.sumocfg' files)

        :param scenario: name of scenario
        :param simulation: name of '.sumocfg' file to be created
        :param result_files: pddl result files to convert into '.sumocfg'
        :return: None
        """
        raise NotImplementedError("Method 'results_to_scenario' must be implemented by children of PddlResult")