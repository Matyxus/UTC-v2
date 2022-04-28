from Project.Utils.constants import PATH, file_exists, dir_exist
import traci
from sumolib import checkBinary


class SimulationLauncher:
    """ Class that launcher SUMO scenarios (.sumocfg files) """
    def __init__(self):
        self.statistics_cmd: list = ["--statistic-output", "result.txt", "--duration-log.statistics", "true"]

    def run_scenario(self, scenario_name: str, default: bool, statistic: bool, display: bool) -> None:
        """
        :param scenario_name: name of scenario to be launched, must be in
        :param default: if planning result should be used for car routes
        :param statistic: if file containing statistics about vehicles should be generated
        :param display: if SUMO GUI should be launched to display simulation
        :return: None
        """
        if not dir_exist(PATH.TRACI_SCENARIOS.format(scenario_name)):
            return
        sumo_run = checkBinary("sumo-gui") if display else checkBinary("sumo")
        options: list = [
            "-c", PATH.TRACI_SCENARIOS.format(scenario_name) + "/simulation.sumocfg",
            "--statistic-output", "result.txt", "--duration-log.statistics", "true",
            "--tripinfo-output", "tripinfo.xml"
        ]
        # Generate file containing vehicle statistics
        if statistic:
            options += self.statistics_cmd
        # [temp, "-c", PATH.TRACI_SCENARIOS.format(scenario_name) + "/simulation.sumocfg"]
        traci.start([sumo_run, *options])
        while traci.simulation.getMinExpectedNumber() > 0:  # -> "while running.."
            traci.simulationStep()
            # print(traci.simulation.getCurrentTime())
        traci.close()


if __name__ == "__main__":
    temp: SimulationLauncher = SimulationLauncher()
    temp.run_scenario("test", True, False, True)

