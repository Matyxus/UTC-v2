from Project.Utils.constants import PATH, file_exists, dir_exist
import traci
from sumolib import checkBinary


class SimulationLauncher:
    """ Class that launcher SUMO scenarios (.sumocfg files) """
    def __init__(self):
        self.statistics_cmd: list = [
            "--statistic-output", "result.txt",
            "--duration-log.statistics", "true",
            "--tripinfo-output", "tripinfo.xml"
        ]

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
            "--route-steps", "0",  # Force sumo to load all vehicles at once
            # "--junction-taz"
        ]
        # Generate file containing vehicle statistics
        if statistic:
            options += self.statistics_cmd
        # [temp, "-c", PATH.TRACI_SCENARIOS.format(scenario_name) + "/simulation.sumocfg"]
        try:
            traci.start([sumo_run, *options])
            print(traci.simulation.getLoadedIDList(), traci.simulation.getPendingVehicles(), traci.simulation.getTime())
            for vehicle_id in traci.simulation.getLoadedIDList():
                print(f"Vehicle: {vehicle_id} departs in: {traci.vehicle.getParameter(vehicle_id, 'param')}")
            traci.vehicle.getParameter()

            while traci.simulation.getMinExpectedNumber() > 0:  # -> "while running.."
                traci.simulationStep()
                print(traci.vehicle.getIDList())
            traci.close()
        except traci.exceptions.FatalTraCIError as e:
            if str(e) == "connection closed by SUMO":
                print("Closed GUI, exiting ....")
            else:
                print(f"Error occurred: {e}")


if __name__ == "__main__":
    temp: SimulationLauncher = SimulationLauncher()
    temp.run_scenario("test", True, False, True)

