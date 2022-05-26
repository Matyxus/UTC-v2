from Project.Utils.xml_object import XmlObject
from typing import List


class Vehicle(XmlObject):
    """ Class representing vehicle for SUMO """
    # https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
    _counter: int = 0  # Variable serving to count number of class instances (to assign id's to vehicles)

    def __init__(self):
        super().__init__("vehicle")
        # ---------- Prepare vehicle attributes  ----------
        self.attributes["id"] = f"v{Vehicle._counter}"
        Vehicle._counter += 1
        self.attributes["depart"] = ""
        # Route (id) trough which cars will travel (must be defined in routes.route.xml file !)
        self.attributes["route"] = ""
        # Average passenger car type (must be defined in routes.route.xml file !)
        self.attributes["type"] = "CarDefault"
        self.attributes["departLane"] = "random"  # Lane on which car will arrive (must be number, or 'random')

    # -------------------------------- Setters --------------------------------

    def set_route(self, route_id: str) -> None:
        """
        :param route_id: id of route trough which cars will travel (must be defined in routes.route.xml file !)
        :return: None
        """
        self.attributes["route"] = route_id

    def set_depart(self, depart_time: int) -> None:
        """
        :param depart_time: time after which vehicle/s should arrive (seconds)
        :return: None
        """
        self.attributes["depart"] = str(depart_time)

    # -------------------------------- Getters --------------------------------

    def get_depart(self) -> float:
        """
        :return: time of vehicle depart (used for sorting), raises error if attribute is not set!
        """
        if self.attributes["depart"] is None:
            raise AttributeError(f"Attribute 'depart' for vehicle: {self.attributes['id']} is not set!")
        return float(self.attributes["depart"])

    # -------------------------------- Utils --------------------------------

    def __lt__(self, other) -> bool:
        if isinstance(other, Vehicle):
            return self.get_depart() < other.get_depart()
        return False


if __name__ == "__main__":
    tmp: Vehicle = Vehicle()
    print(tmp.set_depart.__doc__)
    help(tmp.set_depart)
    # help(Vehicle.set_depart.__doc__)
