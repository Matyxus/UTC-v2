from typing import Dict, Any


class XmlObject:
    """ Class representing xml objects """

    def __init__(self, tag: str):
        self.tag = tag
        self.attributes: Dict[str, Any] = {"id": ""}  # All xml object must have 'id' at least

    def to_xml(self) -> str:
        """
        :return: string representing XML object, <tag, attributes../> (starting with tab space, ending with new line)
        """
        ret_val: str = f"\t<{self.tag}"
        for key, val in self.attributes.items():
            if val:
                ret_val += f' {key}="{val}"'
        return ret_val + "/>\n"
