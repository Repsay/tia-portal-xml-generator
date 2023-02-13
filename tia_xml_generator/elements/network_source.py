from typing import Optional, Union
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET
from copy import deepcopy

from tia_xml_generator.elements.flg_net import FlgNet
from tia_xml_generator.elements.parts.call import Call
from tia_xml_generator.elements.parts.part import Part
from tia_xml_generator.elements.wire import Wire


class NetworkSource(XMLBase):
    element_name = "NetworkSource"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)

        self.load_flg_net()

    def load_flg_net(self) -> None:
        self.flg_net = FlgNet()
        self.add(self.flg_net)

    def build(self) -> ET.Element:
        self_ = deepcopy(self)
        self_.flg_net.check_children()
        if len(self_.flg_net.children) == 0:
            self_.remove(self_.flg_net)
        self_.element.extend([child.build() for child in self_.children])
        return self_.element

    def build_no_call(self) -> ET.Element:
        self_ = deepcopy(self)
        self_.flg_net.check_children_no_call()
        if len(self_.flg_net.children) == 0:
            self_.remove(self_.flg_net)
        self_.element.extend([child.build_no_call() for child in self_.children])
        return self_.element

    def add_part(self, name: str, version: Optional[str]) -> Part:
        return self.flg_net.add_part(name, version)

    def get_part(self, name: str) -> Optional[list[Part]]:
        return self.flg_net.get_part(name)

    def add_call(self, name: str, block_type: str, instance_db_name: str, current_block_type: str) -> Call:
        return self.flg_net.add_call(name, block_type, instance_db_name, current_block_type)

    def get_call(self, name: str) -> Optional[list[Call]]:
        return self.flg_net.get_call(name)

    def add_wire(self, type: str, source: Optional[int], target: Optional[str]):
        return self.flg_net.add_wire(type, source, target)

    def get_wires(self, element: Union[Part, Call]) -> Optional[list[Wire]]:
        return self.flg_net.get_wires(element)
