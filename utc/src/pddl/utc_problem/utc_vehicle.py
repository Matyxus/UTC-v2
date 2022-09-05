from utc.src.pddl.pddl_problem import PddlVehicle
from typing import Dict, Tuple


class UtcVehicle(PddlVehicle):
    """
    Class holding representation of vehicles for utc problem files,
    extends PddlVehicle
    """
    def __init__(self):
        super().__init__()

    def add_vehicles(self, vehicles: Dict[str, Tuple[str, str]]) -> None:
        """
        Adds vehicles to ':object', adds their initial and goal states (positions)

        :param vehicles: dictionary mapping vehicle id to their starting and ending junctions
        :return: None
        """
        super().add_vehicles(vehicles)
        for vehicle_id, junctions in vehicles.items():
            self.add_init_state(f"(at {vehicle_id} j{junctions[0]})")    # Initial position
            self.add_init_state(f"(togo {vehicle_id} j{junctions[1]})")  # Destination pos
            self.add_goal_state(f"(at {vehicle_id} j{junctions[1]})")    # Goal position

