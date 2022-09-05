from utc.src.pddl.pddl_problem.pddl_struct import PddlStruct
from utc.src.graph.components import Skeleton


class PddlNetwork(PddlStruct):
    """
    Class holding representation of road networks for '.pddl' problem files,
    extends PddlStruct
    """
    def __init__(self):
        super().__init__()
        # Name of group used by junctions
        self.junction_group_name: str = "junction"
        # Pddl if of junction
        self.junction_object: str = "j{0}"
        # Name of group used by routes
        self.route_group_name: str = "road"
        # Pddl id of route
        self.route_object: str = "r{0}"
        # Connections between junctions (by route) -> (connected from_junction_id road_id to_junction_id)
        self.connected_state: str = "(connected j{0} {1} j{2})"
        self.initialize_object()

    def initialize_object(self) -> None:
        """
        :return: None
        """
        self.add_object_group(self.junction_group_name)
        self.add_object_group(self.route_group_name)

    def process_graph(self, skeleton: Skeleton) -> None:
        """
        Creates basic pddl representation of graph\n
        ':init' -> (connected junction_id route_id junction_id),\n
        adds id's of junction to group: junction,\n
        id's of routes to group: road\n
        -> ':object' -> j{junction_id}, ..., - junction\n
        -> ':object' -> r{route_id}, ..., - road

        :param skeleton: of Graph
        :return: None
        """
        # Remove unused junctions, etc.
        skeleton.validate_graph()
        # Add junctions (jr{junction_id} is used for roundabouts)
        for junction_id in skeleton.junctions.keys():
            self.add_object(self.junction_group_name, self.junction_object.format(junction_id))
        # Add roads and connections between junctions
        for route_id, route in skeleton.routes.items():
            self.add_object(self.route_group_name, route_id)
            # Add connections between junctions and routes -> (connected from_junction_id road_id to_junction_id)
            self.add_init_state(self.connected_state.format(route.get_start(), route_id, route.get_destination()))
