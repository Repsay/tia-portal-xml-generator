from typing import Optional, Union
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET
from tia_xml_generator.elements.parts.call import Call
from tia_xml_generator.elements.parts.part import Part

from tia_xml_generator.elements.wire import Wire

class Wires(XMLBase):
    element_name = "Wires"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)
        self.wire_id = 21

    def add_wire(self, type: str, source: Optional[int], target: Optional[str]) -> Wire:
        if source is None:
            source = self.wire_id
            self.wire_id += 1
        wire_id = self.wire_id
        self.wire_id += 1
        wire = Wire(wire_id, type, source, target)
        self.add(wire)
        return wire

    def get_wire_id(self) -> int:
        value = self.wire_id
        self.wire_id += 1
        return value

    def get_wires(self, element: Union[Part, Call]) -> Optional[list[Wire]]:
        temp: list[Wire] = []
        for child in self.children:
            if isinstance(child, Wire):
                for connection in child.get_connections():
                    if connection.source == element.id:
                        temp.append(child)
        if len(temp) == 0:
            return None
        return temp