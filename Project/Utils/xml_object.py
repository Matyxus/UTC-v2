from typing import Dict, Any
from xml.etree.ElementTree import Element


class XmlObject:
    """ Class representing xml objects """

    def __init__(self, tag: str):
        self.tag = tag
        self.attributes: Dict[str, Any] = {"id": ""}  # All xml object must have 'id' at least

    def to_xml(self) -> Element:
        """
        :return: xml Element representing this object
        """
        return Element(self.tag, self.attributes)
