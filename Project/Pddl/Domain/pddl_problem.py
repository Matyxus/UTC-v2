

class PddlProblem:
    """ Class holding attributes of pddl problem """
    def __init__(self):
        print("Creating pddl problem class")
        self.attributes: dict = {
            "problem": None,  # Problem is of type string (problem_name of pddl)
            "domain": None,  # Domain is of type string (:domain of pddl)
            "comments": [],  # List of comments (can be added without ';')
            "objects": {},  # {object_group : [object_id, ..], ...} (:objects of pddl)
            "init": [],  # [(predicate1), ...] (:init of pddl)
            "goal": [],  # [(predicate1), ...] (:goal of pddl)
            "metric": None  # Metric is of type string (:metric of pddl)
        }

    def get_problem(self) -> str:
        """
        :return: pddl representation of 'problem' as string (with newline)
        """
        return f"(problem {self.attributes['problem']})\n"

    def get_domain(self) -> str:
        """
        :return: pddl representation of 'domain' as string (with newline)
        """
        return f"(:domain {self.attributes['domain']})\n"

    def get_comments(self) -> str:
        """
        :return: pddl comment (; will be added to front)
        """
        ret_val: str = ""
        for comment in self.attributes["comments"]:
            ret_val += (";" + comment)
        return ret_val

    def get_objects(self) -> str:
        """
        :return: pddl representation of ':objects' as string (with newline)
        """
        ret_val: str = "(:objects\n"
        for object_group, objects in self.attributes["objects"].items():
            ret_val += (" ".join(objects) + f" - {object_group}\n")
        return ret_val + ")\n"

    def get_init(self) -> str:
        """
        :return: pddl representation of ':init' as string (with newline)
        """
        ret_val: str = "(:init\n"
        for predicate in self.attributes["init"]:
            ret_val += (predicate + "\n")
        return ret_val + ")\n"

    def get_goal(self) -> str:
        """
        :return: pddl representation of ':goal' as string (with newline)
        """
        ret_val: str = "(:goal (and\n"
        for predicate in self.attributes["goal"]:
            ret_val += (predicate + "\n")
        return ret_val + "))\n"

    def get_metric(self) -> str:
        """
        :return: pddl representation of ':metric' as string (with newline)
        """
        return f"(:metric {self.attributes['metric']})\n"

    def get_pddl_string(self) -> str:
        """
        :return: entire pddl problem file as string
        """
        ret_val: str = f"(define\n"
        ret_val += self.get_problem() + self.get_domain()
        ret_val += self.get_objects() + self.get_init()
        ret_val += self.get_goal() + self.get_metric()
        return ret_val + ")"
