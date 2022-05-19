import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element
from Project.Utils.constants import PATH, file_exists


class ConfigGenerator:
    """ Class that generates '.sumocfg' files for SUMO """
    def __init__(self):
        self.tree: ElementTree = ET.parse(PATH.SUMO_CONFIG_TEMPLATE)
        self.root: Element = self.tree.getroot()
        # Checks for template
        assert (self.root.find("input") is not None)
        assert (self.root.find("input").find("net-file") is not None)
        assert (self.root.find("input").find("route-files") is not None)
        assert ("value" in self.root.find("input").find("net-file").attrib)
        assert ("value" in self.root.find("input").find("route-files").attrib)

    def load_config(self, config_path: str) -> None:
        """
        :param config_path: path to '.sumocfg' file
        :return: None
        """
        if not file_exists(config_path):
            return
        self.tree = ET.parse(config_path)
        self.root = self.tree.getroot()

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
        self.tree.write(file_path, encoding="UTF-8", xml_declaration=True)
