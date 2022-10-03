from utc.src.file_system import MyFile, SumoConfigFile, SumoRoutesFile
from utc.src.simulator.vehicle import VehicleFactory
from utc.src.file_system import FilePaths, FileExtension
from utc.src.graph.components import Graph, Skeleton
from typing import Optional


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
        self.vehicle_factory: Optional[VehicleFactory] = None
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
        routes_path: str = FilePaths.SUMO_ROUTES_TEMPLATE
        # ---------------------------- Load existing scenario ----------------------------
        self.config_generator = SumoConfigFile(scenario)
        if MyFile.file_exists(self.config_generator, message=False):
            if network == "default":
                network = MyFile.get_file_name(self.config_generator.get_network())
            print(f"Loaded existing scenario: '{scenario}' with network: '{network}'")
            routes_path = FilePaths.SCENARIO_ROUTES.format(scenario)
        # ---------------------------- Create new scenario ----------------------------
        else:
            print(f"Creating new scenario: '{scenario}' with network: '{network}'")
            # Check network
            if network == "default":
                raise ValueError(f"For new scenario: '{scenario}', network: '{network}' must not equal 'default'!")
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
        # Vehicle generator
        self.vehicle_factory = VehicleFactory(self.graph)
        # Sumo routes file
        self.routes_generator = SumoRoutesFile(routes_path)
        if not self.routes_generator.check_file():
            raise ValueError("Error at creating class 'RoutesGenerator' for '.rou.xml' file!")

    def save(self, config_path: str = FilePaths.SCENARIO_SIM_GENERATED) -> bool:
        """
        Creates '.rou.xml' file containing vehicle types, routes, individual vehicles.
        Creates '.sumocfg' file that launches simulation in SUMO GUI (expecting
        xml element "net-file" and "routes-file" to be set before saving)

        :param config_path: path to config path (format string, either
        PATH.SCENARIO_SIM_GENERATED or PATH.SCENARIO_SIM_PLANNED)
        :return: True on success, false otherwise
        """
        if config_path not in {FilePaths.SCENARIO_SIM_PLANNED, FilePaths.SCENARIO_SIM_GENERATED}:
            print(
                f"Invalid config_path: {config_path}, expecting one of: "
                f"{FilePaths.SCENARIO_SIM_PLANNED, FilePaths.SCENARIO_SIM_GENERATED}"
            )
        print(f"Saving scenario: {self.name}")
        # Check
        if self.routes_generator is None or self.config_generator is None:
            print(f"Load scenario first, routes and/or config are 'None' !")
            return False
        elif self.vehicle_factory is not None:  # Add vehicles to routes file
            self.vehicle_factory.save(self.routes_generator.root)
        # Create "scenario_routes.rou.xml"
        if not self.routes_generator.save(FilePaths.SCENARIO_ROUTES.format(self.name)):
            print(f"Error at creating '{self.name + FileExtension.SUMO_ROUTES}' file.")
            return False
        # Create ".sumocfg" (executable)
        elif not self.config_generator.save(config_path.format(self.name)):
            print(f"Error at creating '{self.name + FileExtension.SUMO_CONFIG} file.")
            return False
        print(f"Scenario: '{self.name}' created successfully")
        return True


# For testing purposes
if __name__ == "__main__":
    temp: Scenario = Scenario("test", "Chodov")


