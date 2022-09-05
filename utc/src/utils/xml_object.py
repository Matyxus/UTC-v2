from typing import Dict, Optional
import xml.etree.ElementTree as ET


class XmlObject:
    """ Class representing xml objects """

    def __init__(self, tag: str):
        self.tag = tag
        self.attributes: Dict[str, str] = {"id": ""}  # All xml object must have 'id'

    def get_id(self) -> str:
        """
        :return: id of objects (empty string if it does not exist)
        :raises ValueError if 'id' is not present in attributes dictionary
        """
        return self.attributes["id"]

    def get_attribute(self, attribute: str) -> Optional[str]:
        """
        :param attribute: name of attribute present in attributes dictionary
        :return: value associated with attribute name (None if it does not exist)
        """
        return self.attributes.get(attribute, None)

    def to_xml(self) -> ET.Element:
        """
        :return: xml Element representing this object
        """
        return ET.Element(self.tag, self.attributes)

    # ------------------------------------- Magic methods -------------------------------------

    def __hash__(self) -> int:
        """
        :return: Hash of attribute 'id'
        """
        return hash(self.get_id())

    def __eq__(self, other) -> bool:
        """
        :param other: class to compare against self
        :return: true if classes are of same type and have same id, false otherwise
        """
        if not isinstance(other, type(self)):
            return False
        elif not self.get_id() and not other.get_id():
            print(f"Uninitialized id's of objects cannot be compared !")
            return False
        return self.get_id() == other.get_id()

    def __str__(self) -> str:
        return f"<{self.tag} {' '.join(['{0}={1}'.format(k, v) for k,v in self.attributes.items()])}/>"
