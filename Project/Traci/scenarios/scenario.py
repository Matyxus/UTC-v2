from Project.Utils.constants import PATH
from Project.Traci.simulation import Vehicle, Flow
from Project.Simplify.Components import Route
from Project.Simplify.Components import Graph
from os import mkdir
from typing import List, Dict
import xml.etree.ElementTree as ET


class Scenario:
    """ Class representing scenario for SUMO """

    def __init__(self, scenario_name: str, road_network_name: str):
        self.name: str = scenario_name  # Name of generated directory
        self.road_network: str = road_network_name  # Name of road network
        self.vehicles: List[Vehicle] = []  # List of vehicles in simulation
        self.vehicle_flows: List[Flow] = []  # List of vehicle flows in simulation
        self.routes: List[Route] = []  # List of routes used by vehicles
        self.graph: Graph = Graph()
        self.graph.loader.load_map(self.road_network)
        self.graph.simplify.simplify()
        self.road_paths: Dict[str, Dict[str, str]] = {
            # Recording found shortest paths
            # from_junction_id : {to_junction_id : route_id, ...}, ...
        }

    def add_cars(self, args: List[str]) -> None:
        """
        Adds route (if its new), Vehicle to scenario, expects correct arguments

        :param args: [amount, from_junction_id, to_junction_id, depart_time]
        :return: None
        """
        #
        route_id: str = self.get_path(args[1], args[2])
        if not route_id:
            return
        # Add vehicle
        temp: Vehicle = Vehicle()
        temp.set_route(route_id)
        temp.set_amount(int(args[0]))
        temp.set_depart(float(args[3]))
        self.vehicles.append(temp)

    def add_flow(self, args: List[str]) -> None:
        """
        Adds route (if its new), Flow to scenario, expects correct arguments

        :param args: [begin, end, from_junction_id, to_junction_id, vehicles_per_hour, period, probability, number]
        :return: None
        """
        route_id: str = self.get_path(args[2], args[3])
        if not route_id:
            return
        temp: Flow = Flow()
        temp.set_route(route_id)
        temp.set_time(float(args[0]), float(args[1]))
        temp.set_vehicles_per_hour(int(args[4]))
        self.vehicle_flows.append(temp)

    def save(self) -> bool:
        """
        Saves scenario into folder defined in constants.PATH.TRACI_SCENARIOS
        Creates route.rou.xml file containing vehicle types, routes, individual vehicles,
        vehicle flows. Create simulation.sumocfg file that launches simulation in SUMO GUI.

        :return: True if successful, false otherwise
        """
        try:
            #  --------- Create directory ---------
            dir_path: str = PATH.TRACI_SCENARIOS.format(self.name)
            mkdir(dir_path)
            dir_path += "/"
            # --------- Create simulation.sumocfg (executable)  ---------
            tree = ET.parse(PATH.SUMO_CONFIG_TEMPLATE)
            root = tree.getroot()
            xml_input = root.find("input")
            assert (xml_input is not None)
            net_file = xml_input.find("net-file")
            assert (net_file is not None)
            assert ("value" in net_file.attrib.keys())
            net_file.attrib["value"] = PATH.NETWORK_SUMO_MAPS.format(self.road_network)
            tree.write(dir_path + "simulation.sumocfg", encoding="UTF-8", xml_declaration=True)
            # ---------  Create routes.rout.xml ---------
            with open(dir_path + "routes.rou.xml", "w") as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write("<routes>\n")
                # Add Vehicle types
                file.write("\t" + '<vType accel="3.0" decel="6.0" id="CarDefault" length="4.5" minGap="2.5" maxSpeed="50.0" sigma="0.5" />\n')
                # Add routes
                for route in self.routes:
                    file.write(route.to_xml())
                # Sort vehicles and flows by their beginning time
                combined: list = []
                combined.extend(self.vehicles)
                combined.extend(self.vehicle_flows)
                combined.sort(key=lambda x: x.get_begin(), reverse=True)
                # Write vehicles, flows into file
                for i in combined:
                    file.write(i.to_xml())
                file.write("</routes>\n")
        except FileExistsError:
            print(f"Directory:{PATH.TRACI_SCENARIOS.format(self.name)} already exists!")
            return False
        print(f"Directory:{PATH.TRACI_SCENARIOS.format(self.name)} created successfully")
        return True

    # ---------------------------------- Utils ----------------------------------

    def get_path(self, from_junction_id: str, to_junction_id: str, save: bool = True) -> str:
        """
        :param from_junction_id: starting junction
        :param to_junction_id: destination junction
        :param save: if path should be added to dictionary mapping of found paths (default True)
        :return: id of route, None if it does not exist
        """
        if from_junction_id in self.road_paths and to_junction_id in self.road_paths[from_junction_id]:
            return self.road_paths[from_junction_id][to_junction_id]  # Get route from already found routes
        path: Route
        path = self.graph.shortest_path.a_star(from_junction_id, to_junction_id)[1]
        if path is None:
            print(f"Path between {from_junction_id} and {to_junction_id} does not exist!")
            return ""
        if save:  # Add route to dictionary
            if from_junction_id not in self.road_paths:
                self.road_paths[from_junction_id] = {}
            self.road_paths[from_junction_id][to_junction_id] = path.attributes["id"]
            self.routes.append(path)
        return path.attributes["id"]
