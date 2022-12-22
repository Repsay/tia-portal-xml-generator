from typing import Optional, Union
from tia_xml_generator.elements.attribute_list import AttributeList
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET
from tia_xml_generator.elements.multilingual_text import MultilingualText
from tia_xml_generator.elements.network_source import NetworkSource
from tia_xml_generator.elements.parts.call import Call
from tia_xml_generator.elements.parts.part import Part
from tia_xml_generator.elements.wire import Wire

from tia_xml_generator.enums import ProgrammingLanguage
from tia_xml_generator.elements.object_list import ObjectList

class AttributeListCompileUnit(AttributeList):
    def __init__(self):
        super().__init__()
        self.__programming_language = ET.Element("ProgrammingLanguage")

    @property
    def programming_language(self) -> Optional[ProgrammingLanguage]:
        if self.__programming_language.text is None:
            return None
        return ProgrammingLanguage[self.__programming_language.text]

    @programming_language.setter
    def programming_language(self, programming_language: ProgrammingLanguage) -> None:
        self.__programming_language.text = programming_language.name

class ObjectListCompileUnit(ObjectList):
    def __init__(self, name: str, description: str):
        super().__init__()
        self.__title = MultilingualText("Title")
        self.__comment = MultilingualText("Comment")

        self.add(self.__title)
        self.add(self.__comment)

        self.__title.add_text(name)
        self.__comment.add_text(description)

class CompileUnit(XMLBase):
    element_name = "SW.Blocks.CompileUnit"

    def __init__(self, title: str, programming_language: ProgrammingLanguage, comment: str = ""):
        super().__init__()
        self.name = title
        self.element = ET.Element(self.element_name, {"ID": self.global_id.next(), "CompositionName": "CompileUnits"})

        self.load_attribute_list()
        self.programming_language = programming_language
        self.load_network_source()
        self.load_object_list(title, comment)

    def load_attribute_list(self) -> None:
        self.attribute_list = AttributeListCompileUnit()
        self.add(self.attribute_list)

    def load_network_source(self) -> None:
        self.network_source = NetworkSource()
        self.attribute_list.add(self.network_source)

    def load_object_list(self, title: str, comment: str) -> None:
        self.object_list = ObjectListCompileUnit(title, comment)
        self.add(self.object_list)

    def add_part(self, name: str, version: Optional[str] = None) -> Part:
        return self.network_source.add_part(name, version)

    def add_call(self, name: str, block_type: str) -> Call:
        return self.network_source.add_call(name, block_type)

    def add_wire(self, type: str, source: Optional[int], target: Optional[str]):
        return self.network_source.add_wire(type, source, target)

    def get_part(self, name: str) -> Optional[list[Part]]:
        return self.network_source.get_part(name)

    def get_call(self, name: str) -> Optional[list[Call]]:
        return self.network_source.get_call(name)

    def get_wires(self, element: Union[Part, Call]) -> Optional[list[Wire]]:
        return self.network_source.get_wires(element)

    @property
    def programming_language(self) -> Optional[ProgrammingLanguage]:
        return self.attribute_list.programming_language

    @programming_language.setter
    def programming_language(self, programming_language: ProgrammingLanguage) -> None:
        self.attribute_list.programming_language = programming_language
