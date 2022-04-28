from Project.Utils.xml_object import XmlObject


class Flow(XmlObject):
    """ Class representing vehicle flow in SUMO """
    # https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
    _counter: int = 0  # Variable serving to count number of class instances (to assign id's to flows)

    def __init__(self):
        super().__init__("flow")
        # ---------- Prepare flow attributes ----------
        self.attributes["id"] = f"flow{Flow._counter}"
        Flow._counter += 1
        self.attributes["begin"] = ""
        self.attributes["end"] = ""
        self.attributes["vehsPerHour"] = ""
        self.attributes["period"] = ""
        self.attributes["probability"] = ""
        self.attributes["number"] = ""
        self.attributes["route"] = ""
        self.attributes["type"] = "CarDefault"

    # -------------------- Setters  --------------------

    def set_time(self, start: float, end: float) -> None:
        """
        :param start: starting time of flow (in seconds)
        :param end: ending time of flow (in seconds)
        :return: None
        """
        assert (end > start >= 0)
        self.attributes["begin"] = start
        self.attributes["end"] = end

    def set_vehicles_per_hour(self, amount: int) -> None:
        """
        :param amount: 	number of vehicles per hour, equally spaced (not together with period or probability)
        :return: None
        """
        self.attributes["vehsPerHour"] = amount

    def set_period(self, period: str) -> None:
        """
        :param period: float or "exp(X)" where x is float, (not together with vehsPerHour or probability)
        :return: None
        """
        self.attributes["period"] = period

    def set_probability(self, probability: float) -> None:
        """
        Probability for emitting a vehicle each second

        :param probability: 0 <= probability <= 1, (not together with vehsPerHour or period)
        :return: None
        """
        assert (0 <= probability <= 1)
        self.attributes["probability"] = probability

    def set_number(self, number: int) -> None:
        """
        :param number: total number of vehicles, equally spaced
        :return: None
        """
        assert (number > 0)
        self.attributes["number"] = number

    def set_route(self, route_id: str) -> None:
        """
        :param route_id:  id of route trough which cars will travel (must be defined in routes.route.xml file !)
        :return: None
        """
        self.attributes["route"] = route_id

    # -------------------- Getters --------------------

    def get_begin(self) -> float:
        """
        :return: time of vehicle arrival (used for sorting), raises error if attribute is not set!
        """
        if self.attributes["begin"] is None:
            raise AttributeError(f"Attribute 'begin' for flow: {self.attributes['id']} is not set!")
        return self.attributes["begin"]
