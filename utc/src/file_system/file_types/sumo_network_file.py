from utc.src.file_system.file_types.xml_file import XmlFile
from xml.etree.ElementTree import Element
from utc.src.file_system.file_constants import FileExtension
from typing import Iterator, Dict, List, Optional


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

    def get_subgraphs(self) -> Optional[Iterator[Element]]:
        """
        :return: generator of Subgraph xml elements, none if file is not loaded or
        subgraphs xml element does not exist
        """
        # File is not loaded
        if not self.is_loaded():
            print(f"Xml file of sumo road network is not loaded, cannot return edges!")
            return None
        subgraphs = self.root.findall("subgraphs")
        if not subgraphs:
            return None
        yield from list(subgraphs[0].iter(tag="subgraph"))

    # ------------------------------------------ Utils  ------------------------------------------

    def insert_subgraphs(self, subgraphs: List[Dict[str, str]]) -> None:
        """
        :param subgraphs:
        :return:
        """
        if not self.is_loaded():
            print(f"File is not loaded, cannot insert subgraphs!")
            return
        elif not subgraphs:
            return
        temp: Element = Element("subgraphs")
        # Used existing element to append new subgraphs
        if len(self.root.findall("subgraphs")) != 0:
            temp = self.root.findall("subgraphs")[0]
        # Append new subgraphs
        for attributes in subgraphs:
            temp.append(Element("subgraph", attributes))
        # Add element to tree if it does not exists
        if len(self.root.findall("subgraphs")) == 0:
            self.root.insert(1, temp)

    def get_known_path(self, file_name: str) -> str:
        return file_name
