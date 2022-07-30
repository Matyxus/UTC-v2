import importlib
from typing import Dict
from utc.src.pddl.pddl_problem import PddlLauncher
from utc.src.ui import UserInterface


class PddlMain(UserInterface):
    """ Class that launches program for UTC problem.pddl generation, ask user for input """

    def __init__(self):
        super().__init__()
        self.pddl_launcher: PddlLauncher = None
        # Commands enabled when problem_type is loaded
        self.pddl_commands: Dict[str, callable] = {}
        # -------------- Commands --------------
        self.commands["load_scenario"] = self.load_scenario

    def load_scenario(
            self, scenario: str, new_scenario: str,
            network: str = "default", problem_type: str = "utc"
            ) -> None:
        """

        :param scenario: name of scenario
        :param new_scenario: name of scenario which will get generated from ".pddl" result files
        :param network: name of network on which ".pddl" problem files will be generated,
        if default, will be extracted from scenario
        :param problem_type: name of folder in /utc/src/pddl, expecting suffix '_problem' to be added,
        expecting class 'problem_type_launcher' to be present (subclass of PddlLauncher)
        :return: None
        """
        problem_type = (problem_type if "_problem" in problem_type else problem_type + "_problem")
        module = importlib.import_module(problem_type)
        if module is None:
            print(f"Folder implementing 'pdd_problem' named: {problem_type} does not exist!")
            return
        # Expecting camel case in class name: utc_launcher -> UtcLauncher
        class_name: str = ''.join(
            x.capitalize() or '_' for x in problem_type.replace("_problem", "_launcher").split('_')
        )
        if not hasattr(module, class_name):
            print(f"Module: {problem_type} does not have import class: {class_name} !")
            return
        class_ = getattr(module, class_name)
        instance = None
        try:
            instance = class_()
        except AttributeError as e:
            print(f"Error in initialization of {class_name} class")
            return
        if instance is None or not isinstance(instance, PddlLauncher):
            print(f"Class {class_name} is not subclass of PddlLauncher!")
            return
        # Initialize pddl launcher
        self.pddl_launcher = instance
        if not self.pddl_launcher.initialize(scenario, new_scenario, self.run_command, network):
            return
        # Prepare new methods
        if len(self.pddl_commands.keys()):  # Remove previous pointers
            self.remove_commands(list(self.pddl_commands.keys()))
        self.pddl_commands: Dict[str, callable] = {
            "generate_problems": self.pddl_launcher.generate_problems,
            "generate_results": self.pddl_launcher.generate_results,
            "generate_scenario": self.pddl_launcher.generate_scenario
        }
        self.add_commands(self.pddl_commands)


# Program start
if __name__ == "__main__":
    launcher: PddlMain = PddlMain()
    launcher.run()
