from utc.src.pddl.pddl_problem.pddl_struct import PddlStruct
from typing import Iterable


class PddlVehicle(PddlStruct):
    """
    Class holding representation of vehicles for '.pddl' problem files,
    extends PddlStruct
    """
    def __init__(self):
        super().__init__()
        # Name of group used by vehicles
        self.vehicle_group_name: str = "car"
        # Pddl if of vehicle (not used, since vehicles are saved by default under this id)
        self.vehicle_object: str = "v{0}"
        self.initialize_object()

    def initialize_object(self) -> None:
        """
        :return: None
        """
        self.add_object_group(self.vehicle_group_name)

    def add_vehicles(self, vehicles: Iterable) -> None:
        """
        Adds vehicles to ':object'

        :param vehicles: Iterable object containing vehicle id's
        :return: None
        """
        for vehicle_id in vehicles:
            self.add_object(self.vehicle_group_name, str(vehicle_id))
