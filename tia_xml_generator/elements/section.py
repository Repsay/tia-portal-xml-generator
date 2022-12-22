from typing import Optional
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET

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
        for member in self.members:
            self.add(member)

        return super().build()
