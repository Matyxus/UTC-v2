from typing import Dict, Any
import xml.etree.ElementTree as ET


class XmlObject:
    """ Class representing xml objects """

    def __init__(self, tag: str):
        self.tag = tag
        self.attributes: Dict[str, Any] = {"id": ""}  # All xml object must have 'id'

    def __str__(self) -> str:
        return f"<{self.tag} {' '.join(['{0}={1}'.format(k, v) for k,v in self.attributes.items()])}/>"

    def to_xml(self) -> ET.Element:
        """
        :return: xml Element representing this object
        """
        return ET.Element(self.tag, self.attributes)

