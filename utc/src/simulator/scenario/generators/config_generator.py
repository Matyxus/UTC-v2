from utc.src.simulator.scenario.generators.generator import Generator
from utc.src.utils.constants import PATH, file_exists, dir_exist
from typing import List, Optional
from os import listdir


class ConfigGenerator(Generator):
    """ Class that generates '.sumocfg' files for SUMO """
    def __init__(self, config_path: str = PATH.SUMO_CONFIG_TEMPLATE):
        """
        :param config_path: path to '.sumocfg' file
        """
        super().__init__(config_path)
        # Checks template
        assert (self.tree is not None)
        assert (self.root is not None)
        assert (self.root.find("input") is not None)
        assert (self.root.find("input").find("net-file") is not None)
        assert (self.root.find("input").find("route-files") is not None)

    # ------------------------------------------ Setters ------------------------------------------

    def set_network_name(self, network_name: str) -> None:
        """
        :param network_name: sumo road network (.net.xml)
        :return: None
        """
        if not file_exists(PATH.NETWORK_SUMO_MAPS.format(network_name)):
            return
        self.root.find("input").find("net-file").attrib["value"] = PATH.NETWORK_SUMO_MAPS.format(network_name)

    def set_routes_file(self, routes_file_path: str) -> None:
        """
        :param routes_file_path: path to sumo routes file (.rou.xml)
        :return: None
        """
        self.root.find("input").find("route-files").attrib["value"] = routes_file_path

    # ------------------------------------------ Getters ------------------------------------------

    def get_network_name(self) -> str:
        """
        :return: full path to sumo road network (".net.xml")
        """
        if not self.root.find("input").find("net-file").attrib["value"]:
            return ""
        return self.root.find("input").find("net-file").attrib["value"]

    def get_routes_file(self) -> str:
        """
        :return: full path to sumo routes file (".rou.xml")
        """
        return self.root.find("input").find("route-files").attrib["value"]

    def get_problem_files(self) -> Optional[List[str]]:
        """
        :return: names (with extension) of pddl problem files (generated from this scenario),
        None if directory does not exist
        """
        if dir_exist(PATH.CWD + f"/data/scenarios/problems/{self.name}", message=False):
            return listdir(PATH.CWD + f"/data/scenarios/problems/{self.name}")
        return None

    def get_result_files(self) -> Optional[List[str]]:
        """
        :return: names of pddl result files (that generated this simulation),
        None if directory does not exist
        """
        if dir_exist(PATH.CWD + f"/data/scenarios/results/{self.name}", message=False):
            return listdir(PATH.CWD + f"/data/scenarios/results/{self.name}")
        return None

    # ------------------------------------------ Load & Save ------------------------------------------

    def load(self, file_path: str) -> None:
        if not file_path.endswith(".sumocfg") and file_path != PATH.SUMO_CONFIG_TEMPLATE:
            print(f"Error, expect file type to be: '.sumocfg', got: {file_path}")
            return
        super().load(file_path)

    def save(self, file_path: str) -> None:
        """
        :param file_path: where file should be saved
        :return: None
        """
        if not self.root.find("input").find("net-file").attrib["value"]:
            print("Network file for SUMO config is not set!")
            return
        elif not self.root.find("input").find("route-files").attrib["value"]:
            print("Route file for SUMO config is not set!")
            return
        super().save(file_path)


# For testing purposes
if __name__ == "__main__":
    temp: ConfigGenerator = ConfigGenerator()
