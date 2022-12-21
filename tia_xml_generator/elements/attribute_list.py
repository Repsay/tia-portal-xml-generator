from tia_xml_generator.elements.basis import Basis
import xml.etree.ElementTree as ET

class AttributeList(Basis):
    element_name = "AttributeList"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)
