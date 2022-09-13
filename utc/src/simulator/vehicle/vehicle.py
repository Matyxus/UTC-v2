from utc.src.utils.xml_object import XmlObject


class Vehicle(XmlObject):
    """ Class representing vehicle for SUMO """
    # https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
    _counter: int = 0  # Variable serving to count number of class instances (to assign id's to vehicles)

    def __init__(self, depart: float = -1, route_id: str = ""):
        """
        :param depart: time of vehicle
        :param route_id: which vehicle traverses (must be defined in ".rou.xml" file)
        """
        super().__init__("vehicle")
        # ---------- Prepare vehicle attributes ----------
        self.attributes["id"] = f"v{Vehicle._counter}"
        Vehicle._counter += 1
        self.set_depart(depart)
        # Route (id) trough which cars will travel (must be defined in routes.route.xml file !)
        self.attributes["route"] = route_id
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

    def set_depart(self, depart_time: float) -> None:
        """
        :param depart_time: time after which vehicle/s should arrive (seconds), 2 digit precision
        :return: None
        """
        self.attributes["depart"] = ("" if depart_time < 0 else str(round(depart_time, 2)))

    # -------------------------------- Getters --------------------------------

    def get_depart(self) -> float:
        """
        :return: time of vehicle depart, 2 digit precision (used for sorting), raises error if attribute is not set!
        """
        if self.attributes["depart"] is None:
            raise AttributeError(f"Attribute 'depart' for vehicle: {self.attributes['id']} is not set!")
        return float(self.attributes["depart"])

    # -------------------------------- Utils --------------------------------

    def __lt__(self, other: 'Vehicle') -> bool:
        if isinstance(other, Vehicle):
            return self.get_depart() < other.get_depart()
        return False
