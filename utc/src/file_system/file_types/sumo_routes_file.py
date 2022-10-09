from utc.src.file_system.file_types.xml_file import XmlFile
from utc.src.file_system.file_constants import FileExtension, FilePaths
from typing import Tuple, Dict


class SumoRoutesFile(XmlFile):
    """
    File class handling ".rou.xml" files, provides utility methods
    """

    def __init__(self, file_path: str = FilePaths.SUMO_ROUTES_TEMPLATE):
        """
        :param file_path: to ".rou.xml" file, can be name (in such case
        directory 'utc/data/scenarios/routes' will be search for corresponding file),
        default is template of ".rou.xml" file
        """
        super().__init__(file_path, extension=FileExtension.SUMO_ROUTES)
        # Memory of previously searched vehicles (end_time, index)
        self.previous_search: Tuple[int, int] = (0, 0)

    def save(self, file_path: str = "default") -> bool:
        if not self.check_file():
            return False
        elif file_path == "default" and self.file_path == FilePaths.SUMO_ROUTES_TEMPLATE:
            print(f"Cannot overwrite template for '{self.extension}' files!")
            return False
        return super().save(file_path)

    # ------------------------------------------ Getters ------------------------------------------

    def get_end_time(self) -> float:
        """
        :return: Last vehicle arrival time (-1 if no vehicles are found)
        """
        if not self.check_file():
            return -1
        elif not self.has_vehicles():
            print(f"No vehicles in routes file!")
            return -1
        return float(self.root.findall("vehicle")[-1].attrib["depart"])

    def get_vehicles(self, start_time: float, end_time: float) -> Dict[str, Tuple[str, str]]:
        """
        Extracts vehicles from '.ruo.xml' file, filtered by start/end time as <start_time, end_time)

        :param start_time: earliest vehicle arrival
        :param end_time: latest vehicle arrival (without)
        :return: Vehicle dictionary mapping vehicle id to initial and ending junctions of its route
        """
        # Lower precision
        start_time = round(start_time, 3)
        end_time = round(end_time, 3)
        vehicles: Dict[str, Tuple[str, str]] = {}
        if not self.check_file():
            return vehicles
        elif not self.has_vehicles():
            print("No vehicles in routes file!")
            return vehicles
        routes: Dict[str, Tuple[str, str]] = {}
        # Routes mapping (id: from, to)
        for route in self.root.findall("route"):
            routes[route.attrib["id"]] = (route.attrib["fromJunction"], route.attrib["toJunction"])
        # Find if previous end_time is less than or equal to current start_time, if so
        # get saved index of last vehicle
        search_start: int = 0
        if self.previous_search is not None and self.previous_search[0] <= start_time:
            search_start = self.previous_search[1]  # Index
        # Vehicles
        for index, vehicle in enumerate(self.root.findall("vehicle")[search_start:]):
            depart: float = float(vehicle.attrib["depart"])
            if start_time <= depart < end_time:
                vehicles[vehicle.attrib["id"]] = routes[vehicle.attrib["route"]]
            elif depart >= end_time:
                self.previous_search = (end_time, index)
                break
        return vehicles

    # ------------------------------------------ Utils  ------------------------------------------

    def has_vehicles(self) -> bool:
        """
        :return: True if there are any xml elements of tag "vehicle", false otherwise
        """
        return self.root.find("vehicle") is not None

    def check_file(self) -> bool:
        """
        :return: True if file has correct structure and files used in <input> exist
        """
        # Checks ".sumocfg" file structure
        if self.tree is None:
            print(f"XML Tree is None, cannot save RoutesFile!")
            return False
        elif self.root is None:
            print("XML root of Tree is None, cannot save RoutesFile!")
            return False
        elif self.root.find("vType") is None:
            print(f"Unable to find xml element <vType> in file: {self} !")
            return False
        return True

    def get_known_path(self, file_name: str) -> str:
        # Does not exist, return original
        return file_name


# For testing purposes
if __name__ == "__main__":
    pass
