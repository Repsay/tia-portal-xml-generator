from typing import Optional
from tia_xml_generator.elements.attribute_list import AttributeList
from tia_xml_generator.elements.basis import Basis
import xml.etree.ElementTree as ET
from tia_xml_generator.elements.multilingual_text import MultilingualText
from tia_xml_generator.elements.network_source import NetworkSource

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

class CompileUnit(Basis):
    element_name = "SW.Blocks.CompileUnit"

    def __init__(self, title: str, programming_language: ProgrammingLanguage, comment: str = ""):
        super().__init__()

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

    def add_part(self, name: str, version: str):
        self.network_source.add_part(name, version)

    @property
    def programming_language(self) -> Optional[ProgrammingLanguage]:
        return self.attribute_list.programming_language

    @programming_language.setter
    def programming_language(self, programming_language: ProgrammingLanguage) -> None:
        self.attribute_list.programming_language = programming_language
