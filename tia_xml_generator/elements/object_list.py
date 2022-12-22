from typing import TypeVar
from tia_xml_generator.elements.basis import XMLBase, XMLElement
import xml.etree.ElementTree as ET

T = TypeVar("T", bound=XMLElement)

class ObjectList(XMLBase):
    element_name = "ObjectList"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)