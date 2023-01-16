from typing import Optional
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET
from copy import deepcopy

from tia_xml_generator.elements.member import Member


class Section(XMLBase):
    element_name = "Section"

    members: list[Member]

    def __init__(self, name: str):
        super().__init__()
        self.members = []
        self.element = ET.Element(self.element_name, {"Name": name})

    def add_member(self, name: str, type: str) -> Member:
        if self.get_member(name) is not None:
            raise ValueError(f"Member {name} already exists in section {self.element.get('Name')}")
        member = Member(name, type)
        self.members.append(member)
        return member

    def get_member(self, name: str) -> Optional[Member]:
        for member in self.members:
            if member.name == name:
                return member
        return None

    def build(self) -> ET.Element:
        self_ = deepcopy(self)
        for member in self_.members:
            self_.add(member)

        self_.element.extend([child.build() for child in self_.children])
        return self_.element

    def build_no_call(self) -> ET.Element:
        self_ = deepcopy(self)
        for member in self_.members:
            self_.add(member)

        self_.element.extend([child.build_no_call() for child in self_.children])
        return self_.element
