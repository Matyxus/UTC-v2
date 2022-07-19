import importlib
from typing import List, Tuple, Dict
from Project.Utils.constants import file_exists, dir_exist, PATH
from Project.Pddl.pddl_problem import PddlLauncher
from Project.UI import UserInterface


class PddlMain(UserInterface):
    """ Class that launches program for UTC problem.pddl generation, ask user for input """

    def __init__(self):
        super().__init__()
        self.pddl_launcher: PddlLauncher = None
        # Commands enabled when problem_type is loaded
        self.pddl_commands: Dict[str, callable] = {}
        # -------------- Commands --------------
        self.commands["load_problem"] = self.load_problem

    def load_problem(self, problem_type: str = "utc") -> None:
        """
        :param problem_type: name of folder in /Project/Pddl, expecting suffix '_problem' to be added,
        expecting class 'problem_type_launcher' to be present (extension of /pddl_problem/pddl_launcher.py)
        :return: None
        """
        problem_type = (problem_type if "_problem" in problem_type else problem_type + "_problem")
        """
        if not dir_exist(problem_type):  # Check for pddl '_problem' dir
           return
        elif not file_exists(""):  # Check for pddl '__init__.py' file
            return
        elif not file_exists(""):  # Check for pddl 'problem_type_launcher.py' file
            return
        """
        module = importlib.import_module(problem_type)
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
            instance = class_(self.run_command)
        except Exception as e:
            print(f"Error in initialization of {class_name} class")
            return
        if instance is None or not isinstance(instance, PddlLauncher):
            print(f"Class {class_name} is not subclass of PddlLauncher!")
            return
        self.pddl_launcher = instance
        quit()
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
