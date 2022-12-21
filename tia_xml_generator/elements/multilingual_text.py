from tia_xml_generator.elements.attribute_list import AttributeList
from tia_xml_generator.elements.basis import Basis
import xml.etree.ElementTree as ET

from tia_xml_generator.elements.object_list import ObjectList

class _MulitilingualTextItem(Basis):
    element_name = "MultiLingualTextItem"

    def __init__(self, text: str, language: str):
        super().__init__()
        self.element = ET.Element(self.element_name, {"ID": self.global_id.next(), "CompositionName": "Items"})
        self.load_attribute_list()
        self.__text = ET.Element("Text")
        self.__language = ET.Element("Culture")
        self.attribute_list.element.extend([self.__text, self.__language])

        self.text = text
        self.language = language

    def load_attribute_list(self) -> None:
        self.attribute_list = AttributeList()
        self.add(self.attribute_list)

    @property
    def text(self) -> str:
        if self.__text.text is None:
            return ""
        return self.__text.text

    @text.setter
    def text(self, text: str) -> None:
        self.__text.text = text

    @property
    def language(self) -> str:
        if self.__language.text is None:
            return ""
        return self.__language.text

    @language.setter
    def language(self, language: str) -> None:
        self.__language.text = language

class MultilingualText(Basis):
    element_name = "MultilingualText"

    def __init__(self, composition_name: str):
        super().__init__()
        self.element = ET.Element(self.element_name, {"ID": self.global_id.next(), "CompositionName": composition_name})
        self.load_object_list()

    def load_object_list(self) -> None:
        self.object_list = ObjectList()
        self.add(self.object_list)

    def add_text(self, text: str, language: str = "en-US") -> None:
        self.object_list.add(_MulitilingualTextItem(text, language))