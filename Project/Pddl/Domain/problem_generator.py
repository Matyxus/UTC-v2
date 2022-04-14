from Project.Simplify.Components import Skeleton
from Project.Pddl.Domain import PddlProblem
from Project.constants import Path


class ProblemGenerator(PddlProblem):
    """ Child class of PddlProblem, provides function to add/set parts of pddl file """
    def __init__(self):
        super().__init__()

    # -------------------------------- Setters --------------------------------

    def set_problem_name(self, problem_name: str) -> None:
        """
        :param problem_name: of pddl problem
        :return: None
        """
        self.attributes["problem"] = problem_name

    def set_domain(self, domain_name: str) -> None:
        """
        :param domain_name: of pddl problem
        :return: None
        """
        self.attributes["domain"] = domain_name

    def set_metric(self, metric: str) -> None:
        """
        :param metric:
        :return:
        """
        self.attributes["metric"] = metric

    # -------------------------------- Adders --------------------------------

    def add_object(self, object_name: str, object_group: str) -> None:
        """
        :param object_name: name of object to be added into ':objects - object_group'
        :param object_group: name of object group
        :return: None
        """
        if object_group not in self.attributes["objects"]:
            print(f"Object group: {object_group} does not exist, adding...")
            self.add_object_group(object_group)
        self.attributes["objects"][object_group].append(object_name)

    def add_object_group(self, object_group: str) -> None:
        """
        :param object_group: name of object group added into ':objects'
        :return: None
        """
        self.attributes["objects"][object_group] = []

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
        self.attributes["init"].append(predicate)

    def add_goal_predicate(self, goal_predicate: str) -> None:
        """
        :param goal_predicate: goal predicate of problem added to ':goal'
        :return: None
        """
        self.attributes["goal"].append(goal_predicate)

    def add_network(self, skeleton: Skeleton) -> None:
        """
        Adds basic network (junction, edges, connections) to pddl\n
        Into :objects
            road_id1, ..., road_idX - road\n
            junction_id1, ..., junction_idX - junction\n
        Into :init
            (connected from_junction_id road_id to_junction_id)
        :param skeleton: of graph
        :return: None
        """
        if skeleton is None:
            print("Cannot add network, skeleton object is 'None'!")
            return
        self.add_object_group("junction")
        self.add_object_group("road")
        # Add junctions
        for counter, junction_id in enumerate(skeleton.junctions.keys()):
            self.add_object(f"j{junction_id}", "junction")
        # Add roads and connections between junctions
        for route_id, route in skeleton.routes.items():
            self.add_object(f"r{route_id}", "road")
            # Add connections between junctions and routes
            self.add_predicate(  # (connected from_junction_id road_id to_junction_id)
                f"(connected j{route.get_start()} r{route_id} j{route.get_destination()})"
            )

    # -------------------------------- Utils --------------------------------

    def save(self) -> None:
        if self.attributes["problem"] is None:
            print(f"Problem name is not set, cannot save file!")
            return
        file_path: str = (Path.PDDL_GENERATED_PROBLEMS + self.attributes["problem"] + ".pddl")
        print(f"Saving problem to file: {file_path}")
        try:
            with open(file_path, "w") as file:
                file.write(self.get_pddl_string())
        except Exception as e:
            print(f"Error occurred: {e}")
            return
        print(f"Successfully created problem file")

