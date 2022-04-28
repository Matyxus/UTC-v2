import xml.etree.ElementTree as ET

class RoutesGenerator:
    """ Class that generates '.route.xml' files for SUMO """
    def __init__(self):
        self.tree = ET.ElementTree()



if __name__ == "__main__":
    tree = ET.ElementTree()
    attrib = {"hello":"bye", "hey": 1}
    temp = ET.fromstring(f'<route id="{5}" edges="{1}" />')
    ET.SubElement(tree, temp)
    print(temp.tag, temp.attrib)
    ET.dump(temp)


