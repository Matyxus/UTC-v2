from utc.src.file_system.file_types.xml_file import XmlFile
from utc.src.file_system.file_types.sumo_network_file import SumoNetworkFile
from utc.src.file_system.file_types.sumo_routes_file import SumoRoutesFile
from utc.src.file_system.my_directory import MyDirectory
from utc.src.file_system.file_constants import FileExtension, FilePaths
from typing import List, Optional, Tuple, Union


class SumoConfigFile(XmlFile):
    """
    File class handling ".sumocfg" files, provides
    utility methods (setters, getters, ..)
    """

    def __init__(self, file_path: str = FilePaths.SUMO_CONFIG_TEMPLATE):
        """
        :param file_path: to ".sumocfg" file, can be name (in such case
        directories 'generated' & 'planned' in utc/data/scenarios/simulation
        will be search for corresponding file, default is template of ".sumocfg" file
        """
        super().__init__(file_path, extension=FileExtension.SUMO_CONFIG)
        # Relative paths (so that simulation can be run on any OS)
        self.relative_network_path: str = "../../../../maps/sumo/{0}.net.xml"  # Maps made from osm or by user
        self.relative_scenario_network_path: str = "../../maps/{0}.net.xml"  # Maps made by session
        self.relative_routes_path: str = "../../routes/{0}.rou.xml"

    def save(self, file_path: str = "default") -> bool:
        if not self.check_file():
            return False
        elif file_path == "default" and self.file_path == FilePaths.SUMO_CONFIG_TEMPLATE:
            print(f"Cannot overwrite template for '.sumocfg' files!")
            return False
        return super().save(file_path)

    # ------------------------------------------ Setters ------------------------------------------

    def set_network_name(self, network_name: str, scenario_network: bool = False) -> None:
        """
        :param network_name: sumo road network name ('.net.xml')
        :param scenario_network: true if network files is located in scenario folder
        (relative path to it will be used), otherwise relative path to data/maps/osm will be used
        :return: None
        """
        path: str = self.relative_network_path
        if scenario_network:
            path = self.relative_scenario_network_path
        self.root.find("input").find("net-file").attrib["value"] = path.format(network_name)

    def set_routes_file(self, routes_name: str) -> None:
        """
        :param routes_name: name of routes file (.rou.xml)
        :return: None
        """
        self.root.find("input").find("route-files").attrib["value"] = self.relative_routes_path.format(
            routes_name
        )

    # ------------------------------------------ Getters ------------------------------------------

    def get_network(self, as_file: bool = False) -> Union[SumoNetworkFile, str]:
        """
        :param as_file: true if return value should be SumoNetworkFile, otherwise string
        :return: name of sumo road network (".net.xml")
        """
        network_name: str = self.get_file_name(self.root.find("input").find("net-file").attrib["value"])
        if as_file:
            return SumoNetworkFile(network_name)
        return network_name

    def get_routes(self, as_file: bool = False) -> Union[SumoRoutesFile, str]:
        """
        :param as_file: true if return value should be SumoRoutesFile, otherwise string
        :return: name of sumo routes file (".rou.xml")
        """
        routes_name: str = self.get_file_name(self.root.find("input").find("route-files").attrib["value"])
        if as_file:
            return SumoRoutesFile(routes_name)
        return routes_name

    # ------------------------------------------ Utils ------------------------------------------

    def check_file(self) -> bool:
        """
        :return: True if file has correct structure and files used in <input> exist
        """
        # Checks ".sumocfg" file structure
        if self.tree is None:
            return False
        elif self.root is None:
            return False
        elif self.root.find("input") is None:
            print(f"Unable to find xml element <input> in file: '{self.file_path}' !")
            return False
        """
        # Check elements in "input"
        required_elements: List[Tuple[str, str]] = [
            ("net-file", FilePaths.NETWORK_SUMO_MAP), ("route-files", FilePaths.SCENARIO_ROUTES)
        ]
        for required_element in required_elements:
            if self.root.find("input").find(required_element[0]) is None:
                print(f"Unable to find xml element <input>{required_element[0]}<input/> in file: '{self.file_path}' !")
                return False
            elif not ("value" in self.root.find("input").find(required_element[0]).attrib):
                print(
                    "Unable to find attribute 'value' in xml element "
                    f" <input>{required_element}<input/> in file: '{self.file_path}' !"
                )
                return False
            # Check if file already exists (is not template), then check if net-file and routes-files exist
            elif self.file_path != FilePaths.SUMO_CONFIG_TEMPLATE and self.file_exists(self, message=False):
                file_name: str = self.get_file_name(self.root.find("input").find(required_element[0]).attrib["value"])
                if not self.file_exists(required_element[1].format(file_name), message=False):
                    print(
                        f"Unable to find file used in <input><{required_element[0]}/><input/> -> "
                        f"'{required_element[1].format(file_name)}' !"
                    )
                    return False
        """
        return True

    def get_known_path(self, file_name: str) -> str:
        # Does not exist, return original value
        return file_name
