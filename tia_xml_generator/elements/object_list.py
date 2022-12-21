from typing import TypeVar
from tia_xml_generator.elements.basis import Basis, XMLElement
import xml.etree.ElementTree as ET

T = TypeVar("T", bound=XMLElement)

class ObjectList(Basis):
    element_name = "ObjectList"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)