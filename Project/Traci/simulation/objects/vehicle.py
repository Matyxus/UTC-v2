from Project.Utils.xml_object import XmlObject
from typing import List


class Vehicle(XmlObject):
    """ Class representing vehicle (multiple if they have the same route) for SUMO """
    # https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
    _counter: int = 0  # Variable serving to count number of class instances (to assign id's to vehicles)

    def __init__(self):
        super().__init__("vehicle")
        # ---------- Prepare vehicle attributes  ----------
        self.attributes["depart"] = ""
        # Route (id) trough which cars will travel (must be defined in routes.route.xml file !)
        self.attributes["route"] = ""
        # Average passenger car type (must be defined in routes.route.xml file !)
        self.attributes["type"] = "CarDefault"
        self.attributes["departLane"] = "random"  # Lane on which car will arrive (must be number, or 'random')
        self.amount: int = 1  # Number of cars
        self.interval: str = ""

    # -------------------------------- Setters --------------------------------

    def set_route(self, route_id: str) -> None:
        """
        :param route_id: id of route trough which cars will travel (must be defined in routes.route.xml file !)
        :return: None
        """
        self.attributes["route"] = route_id

    def set_depart(self, depart_time: float) -> None:
        """
        :param depart_time: time after which vehicle/s should arrive (seconds)
        :return: None
        """
        self.attributes["depart"] = str(depart_time )

    def set_amount(self, amount: int) -> None:
        """
        :param amount: Number of cars that have the same starting/ending position
        :return: None
        """
        assert (amount >= 1)
        self.amount = amount

    def set_interval(self, interval: str) -> None:
        """
        :param interval: over which vehicles will arrive departing time [""/uniform/random]
        :return: NOne
        """
        self.interval = self.check_interval(interval)

    # -------------------------------- Getters --------------------------------

    def get_begin(self) -> float:
        """
        :return: time of vehicle arrival (used for sorting), raises error if attribute is not set!
        """
        if self.attributes["depart"] is None:
            raise AttributeError(f"Attribute 'depart' for vehicle: {self.attributes['id']} is not set!")
        return self.attributes["depart"]

    # -------------------------------- Override --------------------------------

    def to_xml(self) -> str:
        # Check what type of interval is selected
        ret_val: str = ""
        for i in range(1, self.amount+1):
            self.attributes["id"] = f"car{Vehicle._counter}"  # Change id during each iteration
            ret_val += super().to_xml()
            Vehicle._counter += 1
        return ret_val

    # -------------------------------- Utils --------------------------------

    def check_interval(self, interval: str) -> str:
        possible_intervals: List[str] = ["uniform", "random", ""]
        if interval not in possible_intervals:
            print(f"Unknown interval: {interval}, possible interval are: {possible_intervals}")
            print("Setting interval to default: None -> all cars will arrive at the same time if possible")
            return ""
        return interval
