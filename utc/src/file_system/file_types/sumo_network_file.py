from utc.src.file_system.file_types.xml_file import XmlFile
from xml.etree.ElementTree import Element
from utc.src.file_system.file_constants import FileExtension, FilePaths
from typing import Iterator, Optional


class SumoNetworkFile(XmlFile):
    """
    File class handling ".net.xml" files,
    provides utility methods
    """

    def __init__(self, file_path: str):
        """
        :param file_path: to ".net.xml" file, can be name (in such case
        directory utc/data/maps/osm  will be search for corresponding file)
        """
        super().__init__(file_path, extension=FileExtension.SUMO_NETWORK)

    # ------------------------------------------ Getters ------------------------------------------

    def get_junctions(self) -> Optional[Iterator[Element]]:
        """
        :return: generator of non-internal
        Junction xml elements, none if file is not loaded
        """
        # File is not loaded
        if not self.is_loaded():
            print(f"Xml file of sumo road network is not loaded, cannot return junctions!")
            return None
        # Find all xml elements named "junction"
        for junction in self.root.findall("junction"):
            # Filter internal junctions
            if ("type" in junction.attrib) and (junction.attrib["type"] != "internal"):
                yield junction

    def get_connections(self) -> Optional[Iterator[Element]]:
        """
        :return: generator of non-internal
        Connection xml elements, none if file is not loaded
        """
        # File is not loaded
        if not self.is_loaded():
            print(f"Xml file of sumo road network is not loaded, cannot return connections!")
            return None
        # Find all xml elements named "connection"
        for connection in self.root.findall("connection"):
            # Filter internal connections
            if connection.attrib["from"][0] != ":":
                yield connection

    def get_edges(self) -> Optional[Iterator[Element]]:
        """
        :return: generator of non-internal
        Edge xml elements, none if file is not loaded
        """
        # File is not loaded
        if not self.is_loaded():
            print(f"Xml file of sumo road network is not loaded, cannot return edges!")
            return None
        # Find all xml elements named "edge"
        for edge in self.root.findall("edge"):
            # Filter internal edges
            if not ("function" in edge.attrib):
                yield edge

    def get_roundabouts(self) -> Optional[Iterator[Element]]:
        """
        :return: generator of non-internal
        Roundabout xml elements, none if file is not loaded
        """
        # File is not loaded
        if not self.is_loaded():
            print(f"Xml file of sumo road network is not loaded, cannot return roundabouts!")
            return None
        # Find all xml elements named "roundabout"
        yield from self.root.findall("roundabout")  # No need to check for internal

    # ------------------------------------------ Utils  ------------------------------------------

    def get_known_path(self, file_name: str) -> str:
        # Search  utc/data/maps/osm
        if self.file_exists(FilePaths.NETWORK_SUMO_MAPS.format(file_name), message=False):
            return FilePaths.NETWORK_SUMO_MAPS.format(file_name)
        return file_name
