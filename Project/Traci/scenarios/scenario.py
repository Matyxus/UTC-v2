from Project.Utils.constants import PATH
from Project.Traci.scenarios.sumo_xml import ConfigGenerator, RoutesGenerator
from Project.Simplify.Components import Graph
from os import mkdir


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
        self.config_generator.set_routes_file("routes.ruo.xml")
        self.config_generator.set_network_name(network_name)
        # Graph
        self.graph: Graph = Graph()
        self.graph.loader.load_map(network_name)
        self.graph.simplify.simplify()
        # Sumo routes file
        self.routes_generator: RoutesGenerator = RoutesGenerator(graph=self.graph)

    def save(self) -> bool:
        """
        Saves scenario into folder defined in constants.PATH.TRACI_SCENARIOS
        Creates route.rou.xml file containing vehicle types, routes, individual vehicles.
        Creates simulation.sumocfg file that launches simulation in SUMO GUI.

        :return: True if successful, false otherwise
        """
        try:
            #  --------- Create directory ---------
            dir_path: str = PATH.TRACI_SCENARIOS.format(self.name)
            mkdir(dir_path)
            dir_path += "/"
            # Create simulation.sumocfg (executable)
            self.config_generator.save(dir_path + "simulation.sumocfg")
            # Create routes.rout.xml
            self.routes_generator.save(dir_path + "routes.ruo.xml")
            # Add folders for plans, results of pddl plans
            mkdir(dir_path + "problems")
            mkdir(dir_path + "results")
        except FileExistsError:
            print(f"Scenario: {PATH.TRACI_SCENARIOS.format(self.name)} already exists!")
            return False
        print(f"Scenario: {PATH.TRACI_SCENARIOS.format(self.name)} created successfully")
        return True
