from Project.Simplify.components import Skeleton
from Project.Pddl.Domain import PddlProblem
from Project.Simplify.graph_modules import ToPddl


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
        :param object_name: name of object to be added into ':object - object_group'
        :param object_group: name of object group
        :return: None
        """
        if object_group not in self.attributes["object"]:
            print(f"Object group: {object_group} does not exist, adding...")
            self.add_object_group(object_group)
        self.attributes["object"][object_group].append(object_name)

    def add_object_group(self, object_group: str) -> None:
        """
        :param object_group: name of object group added into ':objects'
        :return: None
        """
        self.attributes["object"][object_group] = []

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

    def add_network(self, skeleton: Skeleton, clear: bool = True, extended: bool = False) -> None:
        """
        Adds basic network (junction, edges, connections) to pddl\n
        Into :object
            road_id1, ..., road_idX - road\n
            junction_id1, ..., junction_idX - junction\n
        Into :init
            (connected from_junction_id road_id to_junction_id)
        :param skeleton: of graph
        :param clear: replace previously added network with this one
        :param extended: bool, if road network should include capacity, traffic threshold, 'next' predicate
        :return: None
        """
        # Check
        if skeleton is None:
            print("Cannot add network, skeleton object is 'None'!")
            return
        # Clear previous network
        if clear:
            self.clear_network()
        # ---------------- Add network ----------------
        self.network_pddl = ToPddl(skeleton).convert(extended)

    # -------------------------------- Utils --------------------------------

    def clear_attributes(self) -> None:
        """
        :return: Clears dictionary containing pddl objects (cars, domain, ..) apart from network
        """
        self.attributes.clear()

    def clear_network(self) -> None:
        """
        :return: Clears dictionary containing pddl representation of road network
        """
        self.network_pddl.clear()

    def save(self, file_path: str) -> None:
        if self.attributes["problem"] is None:
            print(f"Problem name is not set, cannot save file!")
            return
        print(f"Saving problem to file: {file_path}")
        try:
            with open(file_path, "w") as file:
                file.write(self.get_pddl_string())
        except Exception as e:
            print(f"Error occurred: {e}")
            return
        print("Successfully created problem file")
