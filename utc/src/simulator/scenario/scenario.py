from utc.src.utils.constants import PATH, file_exists
from utc.src.simulator.scenario.generators import ConfigGenerator, RoutesGenerator
from utc.src.graph.components import Graph, Skeleton


class Scenario:
    """ Class representing scenario for SUMO """

    def __init__(self, scenario_name: str, network_name: str):
        """
        :param scenario_name: name of scenario, will be used as directory name
        :param network_name: name of road network file on which simulation will be displayed
        """
        self.name: str = scenario_name  # Name of generated directory
        # Sumo config file
        self.config_generator: ConfigGenerator = ConfigGenerator()
        self.config_generator.set_routes_file(PATH.SCENARIO_ROUTES.format(self.name))
        self.config_generator.set_network_name(network_name)
        # Graph
        self.graph: Graph = Graph(Skeleton())
        self.graph.loader.load_map(network_name)
        self.graph.simplify.simplify_graph()
        # Sumo routes file
        self.routes_generator: RoutesGenerator = RoutesGenerator(graph=self.graph)

    def save(self) -> None:
        """
        Creates route.rou.xml file containing vehicle types, routes, individual vehicles.
        Creates simulation.sumocfg file that launches simulation in SUMO GUI.

        :return: None
        """
        # Create "scenario_routes.rou.xml"
        self.routes_generator.save(PATH.SCENARIO_ROUTES.format(self.name))
        # Create ".sumocfg" (executable)
        self.config_generator.save(PATH.SCENARIO_SIMULATION.format(self.name))
        if not file_exists(PATH.SCENARIO_ROUTES.format(self.name)):
            print(f"Error at creating '.rou.xml' file.")
        elif not file_exists(PATH.SCENARIO_SIMULATION.format(self.name)):
            print(f"Error at creating '.sumocfg' file.")
        else:
            print(f"Scenario: '{self.name}' created successfully")
