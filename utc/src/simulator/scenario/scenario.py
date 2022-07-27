from utc.src.file_system import MyFile, SumoConfigFile, SumoRoutesFile
from utc.src.simulator.simulation import VehicleGenerator
from utc.src.utils.constants import PATH, file_exists, get_file_name
from utc.src.simulator.scenario.generators import RoutesGenerator
from utc.src.graph.components import Graph, Skeleton
from typing import List, Optional


class Scenario:
    """ Class representing scenario for SUMO """

    def __init__(self, scenario: str, network: str = "default"):
        """
        :param scenario: name of scenario, will be used for files corresponding
        to scenario e.g. ".sumocfg", ".rou.xml", etc.
        :param network: name of road network file on which simulation will be displayed,
        if default, expecting parameter "scenario" to exist, network will be extracted from
        scenario.sumocfg file
        """
        self.name: str = scenario  # Name of files related to scenario (.sumocfg, .rou.xml, ..)
        self.graph: Optional[Graph] = None
        self.config_generator: Optional[SumoConfigFile] = None  # ".sumocfg" file
        self.routes_generator: Optional[SumoRoutesFile] = None  # ".rou.xml" file
        self.vehicle_generator: Optional[VehicleGenerator] = None
        self.load(scenario, network)

    def load(self, scenario: str, network: str = "default") -> None:
        """
        :param scenario: name of scenario to load, if such name does not exist, new directory
        will be created when saving scenario
        :param network: name of road network file on which simulation will be displayed,
        if default, network will be extracted from existing scenario.sumocfg file
        :return: None

        :raises FileNotFoundError: if network does not exist
        :raises ValueError: if scenario does not exist and network == 'default' or
        if error occurred during loading ".sumocfg" or ".rou.xml" file
        """
        self.name = scenario
        routes_path: str = PATH.SUMO_ROUTES_TEMPLATE
        # ---------------------------- Load existing scenario ----------------------------
        self.config_generator = SumoConfigFile(scenario)
        if MyFile.file_exists(self.config_generator, message=False):
            if network == "default":
                network = MyFile.get_file_name(self.config_generator.get_network())
            print(f"Loaded existing scenario: '{scenario}' with network: '{network}'")
            routes_path = PATH.SCENARIO_ROUTES.format(scenario)
        # ---------------------------- Create new scenario ----------------------------
        else:
            print(f"Creating new scenario: {scenario} with network: {network}")
            # Check network
            if network == "default":
                raise ValueError(f"For new scenario: {scenario} network: {network} must not equal 'default'!")
            self.config_generator = SumoConfigFile()
            self.config_generator.set_routes_file(scenario)
            self.config_generator.set_network_name(network)
        # Check config file
        if not self.config_generator.check_file():
            raise ValueError("Error at creating class 'SumoConfigFile' for '.sumocfg' file!")
        # Graph
        self.graph: Graph = Graph(Skeleton())
        self.graph.loader.load_map(network)  # No need to check for network existence, SumoConfig does that
        self.graph.simplify.simplify_graph()
        # Sumo routes file
        self.routes_generator = SumoRoutesFile(routes_path)
        if not self.routes_generator.check_file():
            raise ValueError("Error at creating class 'RoutesGenerator' for '.rou.xml' file!")

    def save(self, config_path: str = PATH.SCENARIO_SIM_GENERATED) -> bool:
        """
        Creates '.rou.xml' file containing vehicle types, routes, individual vehicles.
        Creates '.sumocfg' file that launches simulation in SUMO GUI.

        :param config_path: path to config path (format string, either
        PATH.SCENARIO_SIM_GENERATED or PATH.SCENARIO_SIM_PLANNED)
        :return: True on success, false otherwise
        """
        # Create "scenario_routes.rou.xml"
        if not self.routes_generator.save(PATH.SCENARIO_ROUTES.format(self.name)):
            print(f"Error at creating '{self.name}.rou.xml' file.")
            return False
        # Create ".sumocfg" (executable)
        elif not self.config_generator.save(config_path.format(self.name)):
            print(f"Error at creating '{self.name}.sumocfg' file.")
            return False
        print(f"Scenario: '{self.name}' created successfully")
        return True


# For testing purposes
if __name__ == "__main__":
    temp: Scenario = Scenario("test")


