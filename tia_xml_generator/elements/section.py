from tia_xml_generator.elements.basis import Basis
import xml.etree.ElementTree as ET

from tia_xml_generator.elements.member import Member

class Section(Basis):
    element_name = "Section"

    members: list[Member]

    def __init__(self, name: str):
        super().__init__()
        self.members = []
        self.element = ET.Element(self.element_name, {"Name": name})

    def add_member(self, name: str, type: str) -> Member:
        member = Member(name, type)
        self.members.append(member)
        return member

    def build(self) -> ET.Element:
        for member in self.members:
            self.add(member)

        return super().build()
