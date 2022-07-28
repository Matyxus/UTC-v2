from utc.src.file_system.file_types.xml_file import XmlFile
from utc.src.file_system.my_file import MyFile
from utc.src.file_system.my_directory import MyDirectory
from utc.src.utils.constants import PATH
from typing import List, Optional


class SumoConfigFile(XmlFile):
    """
    File class handling ".sumocfg" files, provides
    utility methods (setters, getters, ..)
    """

    def __init__(self, file_path: str = PATH.SUMO_CONFIG_TEMPLATE):
        """
        :param file_path: to ".sumocfg" file, can be name (in such case
        directories 'generated' & 'planned' in utc/data/scenarios/simulation
        will be search for corresponding file, default is template of ".sumocfg" file
        """
        super().__init__(file_path)

    def save(self, file_path: str = "default") -> bool:
        if not self.check_file():
            return False
        elif file_path == "default" and self.file_path == PATH.SUMO_CONFIG_TEMPLATE:
            print(f"Cannot overwrite template for '.sumocfg' files!")
            return False
        elif not file_path.endswith(MyFile.Extension.SUMO_CONFIG):
            print(f"SumoConfig file must be of type: {MyFile.Extension.SUMO_CONFIG}, received: {file_path} !")
            return False
        return super().save(file_path)

    # ------------------------------------------ Setters ------------------------------------------

    def set_network_name(self, network_name: str) -> None:
        """
        :param network_name: sumo road network (.net.xml)
        :return: None
        """
        if not self.file_exists(PATH.NETWORK_SUMO_MAPS.format(network_name)):
            return
        self.root.find("input").find("net-file").attrib["value"] = PATH.NETWORK_SUMO_MAPS.format(network_name)

    def set_routes_file(self, routes_name: str) -> None:
        """
        :param routes_name: name of routes file (.rou.xml)
        :return: None
        """
        self.root.find("input").find("route-files").attrib["value"] = PATH.SCENARIO_ROUTES.format(routes_name)

    # ------------------------------------------ Getters ------------------------------------------

    def get_network(self) -> str:
        """
        :return: full path to sumo road network (".net.xml")
        """
        return self.root.find("input").find("net-file").attrib["value"]

    def get_routes(self) -> str:
        """
        :return: full path to sumo routes file (".rou.xml")
        """
        return self.root.find("input").find("route-files").attrib["value"]

    def get_problem_files(self, as_string: bool = True) -> Optional[List[str]]:
        """
        :param as_string: true if file names should be return as string, PddlFile otherwise
        :return: names (with extension) of pddl problem files (generated from this scenario),
        None if directory does not exist
        """
        # TODO as_string parameter!
        return MyDirectory.list_directory(PATH.PDDL_PROBLEMS + f"/{self.get_file_name(self)}")

    def get_result_files(self, as_string: bool = True) -> Optional[List[str]]:
        """
        :param as_string: true if file names should be return as string, PddlFile otherwise
        :return: names of pddl result files (that generated this simulation),
        None if directory does not exist
        """
        # TODO as_string parameter!
        return MyDirectory.list_directory(PATH.PDDL_RESULTS + f"/{self.get_file_name(self)}")

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
            print(f"Unable to find xml element <input> in file: {self.file_path} !")
            return False
        # Check elements in "input"
        required_elements: List[str] = ["net-file", "route-files"]
        for required_element in required_elements:
            if self.root.find("input").find(required_element) is None:
                return False
            elif not ("value" in self.root.find("input").find(required_element).attrib):
                return False
            # Check if file already exists (is not template), then check if net-file and routes-files exist
            elif self.file_path != PATH.SUMO_CONFIG_TEMPLATE and self.file_exists(self, message=False):
                if not self.file_exists(self.root.find("input").find(required_element).attrib["value"], message=False):
                    print(
                        f"Unable to find file used in <input><{required_element}/><input/> -> "
                        f"{self.root.find('input').find(required_element).attrib['value']} !"
                    )
                    return False
        return True

    def get_file_path(self, file_name: str) -> str:
        # Quick check
        if not file_name:
            return file_name
        # Remove extension
        file_name = file_name.replace(MyFile.Extension.SUMO_CONFIG, "")
        # Search  uts/data/scenarios/generated
        if self.file_exists(PATH.SCENARIO_SIM_GENERATED.format(file_name), message=False):
            return PATH.SCENARIO_SIM_GENERATED.format(file_name)
        # Search uts/data/scenarios/planned
        elif self.file_exists(PATH.SCENARIO_SIM_PLANNED.format(file_name), message=False):
            return PATH.SCENARIO_SIM_PLANNED.format(file_name)
        # Does not exist, return original value
        return file_name


# For testing purposes
if __name__ == "__main__":
    pass
