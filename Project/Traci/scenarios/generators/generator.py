from Project.Utils.constants import file_exists
from xml.dom import minidom
from xml.etree.ElementTree import Element, ElementTree
import xml.etree.ElementTree as ET


class Generator:
    """ Parent class for loading '.xml' files """
    def __init__(self, xml_path: str):
        self.tree: ElementTree = None
        self.root: Element = None
        self.load(xml_path)

    def check(self) -> None:
        print(self.tree is None)

    # ------------------------------------------Load & Save ------------------------------------------

    def load(self, file_path: str) -> None:
        """
        :param file_path: of xml file to be loaded
        :return: None
        """
        print(f"Loading xml file: {file_path}")
        if not file_exists(file_path):
            return
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        print("Success")

    def save(self, file_path: str) -> None:
        """
        :param file_path: where xml file should be saved
        :return: None
        """
        if self.root is None:
            print(f"Error, xml file is not loaded!")
            return
        with open(file_path, 'w') as output:
            output.write(self.prettify(self.root))
        print(f"Successfully created file: {file_path}")

    # ------------------------------------------ Utils ------------------------------------------

    def prettify(self, root: ET.Element) -> str:
        """
        :param root: of xml tree
        :return: pretty print version of xml file
        """
        rough_string = ET.tostring(root, 'utf-8', xml_declaration=True)
        re_parsed = minidom.parseString(rough_string)
        return re_parsed.toprettyxml(indent="  ")
