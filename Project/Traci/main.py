from Project.UI import UserInterface
from Project.Utils.constants import file_exists, PATH
from Project.Traci.scenarios import Scenario


class TraciLauncher(UserInterface):
    """ Class that ask user for input related to generating SUMO scenarios, planning and running scenarios """

    def __init__(self):
        super().__init__()
        self.scenario: Scenario = None
        self.commands["generate-scenario"] = self.scenario_command

    def static_input(self) -> None:
        print("TraciLauncher Class does not take static input!")

    # ---------------------------------- Commands ----------------------------------

    def scenario_command(self, scenario_name: str, network_name: str) -> None:
        """
        :param scenario_name: name of scenario folder
        :param network_name: name of network on which simulation will be displayed
        :return: None
        """
        if not file_exists(PATH.NETWORK_SUMO_MAPS.format(network_name)):
            return
        self.scenario = Scenario(scenario_name, network_name)
        self.add_commands(
            {
                "add-cars": self.scenario.routes_generator.vehicle_generator.add_vehicles,
                "add-random-flow": self.scenario.routes_generator.vehicle_generator.random_flow,
                "save": self.save_command,
                "plot": self.scenario.graph.display.plot
            }
        )

    def save_command(self) -> None:
        """
        :return:
        """
        self.scenario.save()
        self.scenario = None
        self.remove_commands(["add-cars", "add-random-flow", "save", "plot"])


if __name__ == "__main__":
    traci_launcher: TraciLauncher = TraciLauncher()
    traci_launcher.dynamic_input()

