from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET

class AttributeList(XMLBase):
    element_name = "AttributeList"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)
