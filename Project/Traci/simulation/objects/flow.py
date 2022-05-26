from Project.Traci.simulation.objects.vehicle import Vehicle
from typing import List
import random


class Flow:
    """ Class representing vehicle flow in SUMO """
    # https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
    # Instead of creating <flow> xml object, converts flow to individual <vehicle> xml objects

    def __init__(self):
        self.SEED: int = 42
        random.seed(self.SEED)
        print(f"Initialized Flow class with random seed: {self.SEED}")

    # Types of Flows, uniform, random, exponential, ....
    # Improve with numpy for performance!

    # -------------------------------------------- Flows --------------------------------------------

    def random_flow(
            self, route_id: str, minimal: int, maximal: int, period: int, start_time: int, end_time: int
            ) -> List[Vehicle]:
        """
        Randomly sends between minimal and maximal cars every period, starting
        from start_time, ending at end_time.
        Vehicles will have random departure time

        :param route_id: id if route cars go trough
        :param minimal: amount of cars to be sent
        :param maximal: maximal amount of cars to be sent
        :param period: time (seconds) over which vehicles are sent
        :param start_time: of flow (seconds)
        :param end_time: of flow (seconds)
        :return: List of vehicles (not sorted by time) if arguments are correct, empty list otherwise
        """
        print("Adding random flow")
        vehicles: List[Vehicle] = []
        minimal = int(minimal)
        maximal = int(maximal)
        period = int(period)
        start_time = int(start_time)
        end_time = int(end_time)
        assert(end_time > start_time >= 0)
        assert(maximal >= minimal >= 1)

        duration: int = (end_time - start_time)
        if ((maximal + minimal) / 2) * int(duration / period) > 10000:
            print("Generating over 10 000 vehicles, returning ....!")
            return vehicles
        # For every period add cars to vehicle list
        for i in range(int(duration / period)):
            current_time: int = start_time + (i * period)
            end_time: int = current_time + period
            # Add randomly chosen number of cars to list
            for car in range(random.randint(minimal, maximal)):
                vehicle: Vehicle = Vehicle()
                vehicle.set_route(route_id)
                # Randomly select departure time
                vehicle.set_depart(random.randint(current_time, end_time))
                vehicles.append(vehicle)
        print(f"Random flow generated: {len(vehicles)} vehicles")
        return vehicles


# For testing purposes
if __name__ == "__main__":
    flow: Flow = Flow()
    flow.random_flow("r1", 10, 25, 20, 0, 1800)


