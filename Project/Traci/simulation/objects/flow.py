from Project.Traci.simulation.objects.vehicle import Vehicle
from typing import List


class Flow:
    """ Class representing vehicle flow in SUMO """
    # https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
    # Instead of creating <flow> xml object, converts flow to individual <vehicle> xml objects

    def __init__(self, vehicle_list: List[Vehicle]):
        # List for appending vehicles
        self.vehicle_list: List[Vehicle] = vehicle_list

    # Types of Flows, uniform, random, exponential, ....

