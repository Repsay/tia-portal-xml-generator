from tia_xml_generator.elements.basis import Basis
import xml.etree.ElementTree as ET

from tia_xml_generator.elements.parts import Parts
from tia_xml_generator.elements.wires import Wires

class FlgNet(Basis):
    element_name = "FlgNet"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name, {"xmlns": "http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v3"})

        self.load_parts()
        self.load_wires()

    def load_parts(self) -> None:
        self.parts = Parts()
        self.add(self.parts)

    def load_wires(self) -> None:
        self.wires = Wires()
        self.add(self.wires)

    def build(self) -> ET.Element:
        if len(self.parts.children) == 0:
            self.remove(self.parts)
        if len(self.wires.children) == 0:
            self.remove(self.wires)
        return super().build()

    def add_part(self, name: str, version: str):
        self.parts.add_part(name, version)