from copy import deepcopy
from typing import Optional, Union
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET

from tia_xml_generator.elements.parts import Parts
from tia_xml_generator.elements.parts.call import Call
from tia_xml_generator.elements.parts.part import Part
from tia_xml_generator.elements.wire import Wire
from tia_xml_generator.elements.wires import Wires


class FlgNet(XMLBase):
    element_name = "FlgNet"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(
            self.element_name, {"xmlns": "http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v3"}
        )

        self.load_parts()
        self.load_wires()

    def load_parts(self) -> None:
        self.parts = Parts()
        self.add(self.parts)

    def load_wires(self) -> None:
        self.wires = Wires()
        self.add(self.wires)

    def check_children(self) -> None:
        if len(self.parts.children) == 0:
            if self.children.count(self.parts) == 1:
                self.remove(self.parts)
        if len(self.wires.children) == 0:
            if self.children.count(self.wires) == 1:
                self.remove(self.wires)

    def check_children_no_call(self) -> None:
        for child in self.parts.children:
            if isinstance(child, Call):
                wires = self.wires.get_wires(child)
                if not wires is None:
                    for wire in wires:
                        self.wires.remove(wire)
                self.parts.remove(child)

        if len(self.parts.children) == 0:
            if self.children.count(self.parts) == 1:
                self.remove(self.parts)
        if len(self.wires.children) == 0:
            if self.children.count(self.wires) == 1:
                self.remove(self.wires)

    def build(self) -> ET.Element:
        self_ = deepcopy(self)
        self_.check_children()
        self_.element.extend([child.build() for child in self_.children])
        return self_.element

    def build_no_call(self) -> ET.Element:
        self_ = deepcopy(self)
        self_.check_children_no_call()
        self_.element.extend([child.build_no_call() for child in self_.children])
        return self_.element

    def add_part(self, name: str, version: Optional[str]) -> Part:
        if self.parts.part_id < self.wires.wire_id:
            self.parts.part_id = self.wires.wire_id

        part = self.parts.add_part(name, version)

        for input_value in part.part_info["inputs"]:
            wire = self.add_wire("NameCon", part.id, input_value)
            wire.add_connection("OpenCon", self.wires.get_wire_id())

        for output in part.part_info["outputs"]:
            wire = self.add_wire("NameCon", part.id, output)
            wire.add_connection("OpenCon", self.wires.get_wire_id())

        return part

    def get_part(self, name: str) -> Optional[list[Part]]:
        return self.parts.get_part(name)

    def add_call(
        self,
        name: str,
        current_block_type: str,
        block_type: Optional[str],
        reference: Optional[str],
        reference_type: Optional[str],
    ) -> Call:
        if self.parts.part_id < self.wires.wire_id:
            self.parts.part_id = self.wires.wire_id

        call = self.parts.add_call(name, block_type, reference, reference_type)

        wire = self.add_wire("NameCon", call.id, "en")
        if current_block_type == "FB":
            wire.add_connection("OpenCon", self.wires.get_wire_id())
        elif current_block_type == "OB":
            wire.add_powerrail()

        return call

    def get_call(self, name: str) -> Optional[list[Call]]:
        return self.parts.get_call(name)

    def add_wire(self, wire_type: str, source: Optional[int], target: Optional[str]) -> Wire:
        if self.wires.wire_id < self.parts.part_id:
            self.wires.wire_id = self.parts.part_id
        return self.wires.add_wire(wire_type, source, target)

    def get_wires(self, element: Union[Part, Call]) -> Optional[list[Wire]]:
        return self.wires.get_wires(element)
