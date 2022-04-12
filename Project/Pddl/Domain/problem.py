from Project.Simplify.Components import Skeleton
from Project.constants import CWD
from typing import Dict


class Problem:
    """ """
    def __init__(self):
        self.attributes: dict = {
            "problem": None,
            ":domain": None,
            "comments": [],
            ":objects": {},  # object_group : [object_id, ..]
            ":init": [],  # (predicate1), ...
            ":goal": [],  # (predicate1), ...
            ":metric": None
        }
        self.junction_mapping: Dict[str, str] = {}

    # -------------------------------- Setters --------------------------------

    def set_problem_name(self, problem_name: str) -> None:
        """
        :param problem_name: of pddl problem
        :return: None
        """
        self.attributes[":problem"] = problem_name

    def set_domain(self, domain_name: str) -> None:
        """
        :param domain_name: of pddl problem
        :return: None
        """
        self.attributes[":domain"] = domain_name

    def set_metric(self, metric: str) -> None:
        """
        :param metric:
        :return:
        """
        self.attributes[":metric"] = metric

    # -------------------------------- Adders --------------------------------

    def add_object(self, object_name: str, object_group: str) -> None:
        """
        :param object_name: name of object to be added into ':objects - object_group'
        :param object_group: name of object group
        :return: None
        """
        if object_group not in self.attributes[":objects"]:
            print(f"Object group: {object_group} does not exist, adding...")
            self.add_object_group(object_group)
        self.attributes[":objects"][object_group].append(object_name)

    def add_object_group(self, object_group: str) -> None:
        """
        :param object_group: name of object group added into ':objects'
        :return: None
        """
        self.attributes[":objects"][object_group] = []

    def add_comment(self, comment: str) -> None:
        """
        :param comment: to be added (comment lines start with ';')
        :return: None
        """
        self.attributes["comments"].append(comment)

    def add_predicate(self, predicate: str) -> None:
        """
        :param predicate: to be added into ':init'
        :return: None
        """
        if not predicate or predicate[0] != "(" or predicate[-1] != ")":
            print(f"Invalid predicate: {predicate}")
            return
        self.attributes[":init"].append(predicate)

    def add_goal_predicate(self, goal_predicate: str) -> None:
        """
        :param goal_predicate: goal predicate of problem added to ':goal'
        :return: None
        """
        self.attributes[":goal"].append(goal_predicate)

    def add_network(self, skeleton: Skeleton) -> None:
        """
        :param skeleton: of graph
        :return: None
        """
        if skeleton is None:
            print("Cannot add network, skeleton object is none!")
            return
        self.add_object_group("junction")
        self.add_object_group("road")
        # Add junctions, create mapping for junction id's
        for counter, junction_id in enumerate(skeleton.junctions.keys()):
            mapped_id: str = f"j{counter}"
            self.junction_mapping[junction_id] = mapped_id
            self.add_object(mapped_id, "junction")
        tmp: str = ""
        for junction_id, mapped_id in self.junction_mapping.items():
            tmp += f" {mapped_id}:{junction_id}"
        self.add_comment(tmp)  # Add junction mapping as comment (single string)
        # Add routes, create mapping for routes (route_id -> list of edges)
        tmp = ""
        for route_id, route in skeleton.routes.items():
            mapped_id: str = f"r{route_id}"
            tmp += f" {mapped_id}:{','.join([edge.attributes['id'] for edge in route.edge_list])}"
            self.add_object(mapped_id, "road")
            # Add connections between junctions and routes
            self.add_predicate(  # (connected from_junction_id road_id to_junction_id)
                f"(connected {self.junction_mapping[route.get_start()]} {mapped_id} {self.junction_mapping[route.get_destination()]})"
            )
        self.add_comment(tmp)  # Add route mapping as comment (single string)

    # -------------------------------- Utils --------------------------------

    def save(self, file_name: str) -> None:
        file_path: str = (CWD + "/Pddl/Problems/generated/" + file_name + ".pddl")
        print(f"Saving problem to file: {file_path}")
        try:
            with open(file_path, "w") as file:
                file.write(f"(define (problem {self.attributes[':problem']}) (:domain {self.attributes[':domain']})\n")
                # ---------------- Objects & Comments ----------------
                file.write(f"(:objects\n")
                for comment in self.attributes["comments"]:
                    file.write(";" + comment + "\n")
                for object_group, objects in self.attributes[":objects"].items():
                    file.write(" ".join(objects) + f" - {object_group}\n")
                file.write(")\n")
                # ---------------- Init ----------------
                file.write("(:init\n")
                for predicate in self.attributes[":init"]:
                    file.write(predicate + "\n")
                file.write(")\n")
                # ---------------- Goal ----------------
                file.write("(:goal (and\n")
                for predicate in self.attributes[":goal"]:
                    file.write(predicate + "\n")
                file.write("))\n")
                # ---------------- Metric ----------------
                file.write(f"(:metric {self.attributes[':metric']})\n")
                file.write(")")  # End of file
        except Exception as e:
            print(f"Error occurred: {e}")
            return
        print(f"Successfully created problem file")

