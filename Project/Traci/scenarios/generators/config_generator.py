from Project.Traci.scenarios.generators.generator import Generator
from Project.Utils.constants import PATH, file_exists


class ConfigGenerator(Generator):
    """ Class that generates '.sumocfg' files for SUMO """
    def __init__(self, config_path: str = PATH.SUMO_CONFIG_TEMPLATE):
        """
        :param config_path: path to '.sumocfg' file
        """
        # super().__init__(config_path)
        super().__init__(config_path)
        # Checks template
        print("Cheking template")
        assert (self.tree is not None)
        assert (self.root is not None)
        assert (self.root.find("input") is not None)
        assert (self.root.find("input").find("net-file") is not None)
        assert (self.root.find("input").find("route-files") is not None)
        assert ("value" in self.root.find("input").find("net-file").attrib)
        assert ("value" in self.root.find("input").find("route-files").attrib)

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

    # ------------------------------------------Load & Save ------------------------------------------

    def load(self, file_path: str) -> None:
        if ".sumocfg" not in file_path and file_path != PATH.SUMO_CONFIG_TEMPLATE:
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
