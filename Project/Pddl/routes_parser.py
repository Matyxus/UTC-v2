import xml.etree.ElementTree as ET
from Project.Utils.constants import PATH, file_exists
from typing import Dict


class RouteParser:
    """ """
    def __init__(self):
        # Xml root of .rou.xml file
        self.root: ET.Element = None

    def load_vehicles(self, scenario_name: str, start_time: int, end_time: int) -> Dict[str, tuple]:
        """
        :param scenario_name: scenario
        :param start_time: earliest vehicle arrival
        :param end_time: latest vehicle arrival
        :return: Vehicle dictionary mapping vehicle id to initial and ending edge of its route
        """
        vehicles: Dict[str, tuple] = {}
        if not file_exists(PATH.TRACI_SCENARIOS.format(scenario_name) + "/routes.rou.xml"):
            return vehicles
        self.root = ET.parse(PATH.TRACI_SCENARIOS.format(scenario_name) + "/routes.rou.xml").getroot()
        routes: Dict[str, tuple] = {}
        for route in self.root.findall("route"):
            edges: list = route.attrib["edges"].split()
            routes[route.attrib["id"]] = (edges[0], edges[-1])  # Initial and ending edges
        for vehicle in self.root.findall("vehicle"):
            if start_time <= float(vehicle.attrib["depart"]) <= end_time:
                vehicles[vehicle.attrib["id"]] = routes[vehicle.attrib["route"]]
        return vehicles


if __name__ == "__main__":
    tmp: RouteParser = RouteParser()
    print(tmp.load_vehicles("test", 10, 20))

