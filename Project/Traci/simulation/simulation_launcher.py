from Project.Utils.constants import PATH, file_exists
import traci
from sumolib import checkBinary


class SimulationLauncher:
    """ Class that launcher SUMO scenarios (.sumocfg files) """
    def __init__(self):
        self.statistics_cmd: list = [
            "--statistic-output", "result.txt",
            "--duration-log.statistics", "true",
            "--tripinfo-output", "tripinfo.xml",
            "--summary", "summary.txt"
        ]

    def run_scenario(
            self, scenario_name: str, statistic: bool,
            display: bool = True, simulation_name: str = "simulation"
            ) -> None:
        """
        :param scenario_name: name of scenario to be launched
        :param simulation_name: name of '.sumocfg' file (default -> 'simulation.sumocfg')
        :param statistic: if file containing statistics about vehicles should be generated
        :param display: bool (true/false) if SUMO GUI should be launched to display simulation (default True)
        :return: None
        """
        if not file_exists(PATH.TRACI_SIMULATION.format(scenario_name, simulation_name)):
            return
        sumo_run = checkBinary("sumo-gui") if display else checkBinary("sumo")
        options: list = [
            "-c", PATH.TRACI_SCENARIOS.format(scenario_name) + "/simulation.sumocfg",
            "--route-steps", "0",  # Force sumo to load all vehicles at once
            # "--junction-taz"
        ]
        # Generate file containing vehicle statistics
        if statistic:
            options += self.statistics_cmd
        try:
            traci.start([sumo_run, *options])
            while traci.simulation.getMinExpectedNumber() > 0:  # -> "while running.."
                traci.simulationStep()
            traci.close()
        except traci.exceptions.FatalTraCIError as e:
            if str(e) == "connection closed by SUMO":
                print("Closed GUI, exiting ....")
            else:
                print(f"Error occurred: {e}")

    def plan_scenario(self, scenario_name: str, network_name: str, display: bool) -> None:
        """
        Starts 'simulation.cfg' using TraCI, parses 'routes.ruo.xml' file to generate
        vehicle routes using automated AI (planner) -> every X seconds pauses simulation to plan
        vehicle routes, then for another X seconds the simulation will continue.

        :param scenario_name: name of scenario to be launched
        :param network_name: name of '.net.xml' file on which planner will plan (default is the one
        used in 'simulation.sumocfg' file)
        :param display: if SUMO GUI should be launched to display simulation
        :return: None
        """
        pass


# For testing purposes
if __name__ == "__main__":
    pass

