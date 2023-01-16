from typing import Optional
import xml.etree.ElementTree as ET
from tia_xml_generator.elements.multilingual_text import MultilingualText
from tia_xml_generator.enums import ProgrammingLanguage
from tia_xml_generator.elements.attribute_list import AttributeList

from tia_xml_generator.elements.basis import XMLBase
from tia_xml_generator.elements.blocks import Block
from tia_xml_generator.elements.interface import InterfaceDB
from tia_xml_generator.elements.member import Member
from tia_xml_generator.elements.object_list import ObjectList


class AttributeListDB(AttributeList):
    def __init__(self):
        super().__init__()
        self.__name = ET.Element("Name")
        self.__auto_number = ET.Element("AutoNumber")
        self.__author = ET.Element("HeaderAuthor")
        self.__family = ET.Element("HeaderFamily")
        self.__header_name = ET.Element("HeaderName")
        self.__version = ET.Element("HeaderVersion")
        self.__memory_layout = ET.Element("MemoryLayout")
        self.__number = ET.Element("Number")
        self.__programming_language = ET.Element("ProgrammingLanguage")
        # TODO: Add all attributes
        self.__assigned_prodiag_fb = ET.Element("AssignedProDiagFB")
        self.__supervisions = ET.Element("Supervisions")
        self.__is_iec_check_enabled = ET.Element("IsIECCheckEnabled")
        self.__is_retain_mem_res_enabled = ET.Element("IsRetainMemResEnabled")
        self.__memory_reserve = ET.Element("MemoryReserve")
        self.__retain_memory_reserve = ET.Element("RetainMemoryReserve")
        self.__parameter_passing = ET.Element("ParameterPassing")
        self.__uda_block_properties = ET.Element("UDABlockProperties")
        self.__uda_enable_tag_readback = ET.Element("UDAEnableTagReadback")
        self.__library_conformance_status = ET.Element("LibraryConformanceStatus")
        self.element.extend([self.__name, self.__programming_language])
        self.auto_number = True
        self.load_interface()

    def load_interface(self) -> None:
        self.interface = InterfaceDB()
        self.add(self.interface)

    @property
    def name(self) -> str:
        if self.__name.text is None:
            return ""
        return self.__name.text

    @name.setter
    def name(self, name: str) -> None:
        self.__name.text = name

    @property
    def programming_language(self) -> Optional[ProgrammingLanguage]:
        if self.__programming_language.text is None:
            return None
        return ProgrammingLanguage[self.__programming_language.text]

    @programming_language.setter
    def programming_language(self, programming_language: ProgrammingLanguage) -> None:
        self.__programming_language.text = programming_language.name

    @property
    def auto_number(self) -> bool:
        if self.__auto_number.text is None:
            return False
        return self.__auto_number.text == "true"

    @auto_number.setter
    def auto_number(self, auto_number: bool) -> None:
        self.__auto_number.text = "true" if auto_number else "false"
        if self.element.find("AutoNumber") is None:
            self.element.append(self.__auto_number)

        if auto_number and self.element.find("Number") is not None:
            self.element.remove(self.__number)

        if not auto_number and self.number != "":
            self.element.append(self.__number)

        if not auto_number and self.number == "":
            raise ValueError("Number must be set if auto_number is False")

    @property
    def author(self) -> str:
        if self.__author.text is None:
            return ""
        return self.__author.text

    @author.setter
    def author(self, author: str) -> None:
        self.__author.text = author
        if self.element.find("HeaderAuthor") is None:
            self.element.append(self.__author)

    @property
    def family(self) -> str:
        if self.__family.text is None:
            return ""
        return self.__family.text

    @family.setter
    def family(self, family: str) -> None:
        self.__family.text = family
        if self.element.find("HeaderFamily") is None:
            self.element.append(self.__family)

    @property
    def header_name(self) -> str:
        if self.__header_name.text is None:
            return ""
        return self.__header_name.text

    @header_name.setter
    def header_name(self, header_name: str) -> None:
        self.__header_name.text = header_name
        if self.element.find("HeaderName") is None:
            self.element.append(self.__header_name)

    @property
    def version(self) -> str:
        if self.__version.text is None:
            return ""
        return self.__version.text

    @version.setter
    def version(self, version: str) -> None:
        self.__version.text = version
        if self.element.find("HeaderVersion") is None:
            self.element.append(self.__version)

    @property
    def memory_layout(self) -> str:
        if self.__memory_layout.text is None:
            return ""
        return self.__memory_layout.text

    @memory_layout.setter
    def memory_layout(self, memory_layout: str) -> None:
        self.__memory_layout.text = memory_layout
        if self.element.find("MemoryLayout") is None:
            self.element.append(self.__memory_layout)

    @property
    def number(self) -> str:
        if self.__number.text is None:
            return ""
        return self.__number.text

    @number.setter
    def number(self, number: str) -> None:
        self.__number.text = number
        if self.element.find("Number") is None and self.auto_number is False:
            self.element.append(self.__number)


class ObjectListDB(ObjectList):
    def __init__(self):
        super().__init__()
        self.title = MultilingualText("Title")
        self.comment = MultilingualText("Comment")

        self.add(self.title)
        self.add(self.comment)

        self.title.add_text("")
        self.comment.add_text("")


class DB(XMLBase, Block):
    element_name = "SW.Blocks.GlobalDB"
    attribute_list: AttributeListDB

    def __init__(self, name: str):
        super().__init__()
        self.load_attribute_list()
        self.id = self.global_id.next()
        self.name = name
        self.programming_language = ProgrammingLanguage.DB
        self.element = ET.Element(self.element_name, {"ID": self.id})
        self.load_object_list()

    def load_attribute_list(self) -> None:
        self.attribute_list = AttributeListDB()
        self.add(self.attribute_list)

    def load_object_list(self) -> None:
        self.object_list = ObjectListDB()
        self.add(self.object_list)

    def add_static(self, name: str, data_type: str) -> Member:
        return self.attribute_list.interface.sections.static.add_member(name, data_type)

    def get_static(self, name: str) -> Optional[Member]:
        return self.attribute_list.interface.sections.static.get_member(name)

    @property
    def author(self) -> str:
        return self.attribute_list.author

    @author.setter
    def author(self, author: str) -> None:
        self.attribute_list.author = author

    @property
    def family(self) -> str:
        return self.attribute_list.family

    @family.setter
    def family(self, family: str) -> None:
        self.attribute_list.family = family

    @property
    def header_name(self) -> str:
        return self.attribute_list.header_name

    @header_name.setter
    def header_name(self, header_name: str) -> None:
        self.attribute_list.header_name = header_name

    @property
    def version(self) -> str:
        return self.attribute_list.version

    @version.setter
    def version(self, version: str) -> None:
        self.attribute_list.version = version

    @property
    def memory_layout(self) -> str:
        return self.attribute_list.memory_layout

    @memory_layout.setter
    def memory_layout(self, memory_layout: str) -> None:
        self.attribute_list.memory_layout = memory_layout

    @property
    def auto_number(self) -> bool:
        return self.attribute_list.auto_number

    @auto_number.setter
    def auto_number(self, auto_number: bool) -> None:
        self.attribute_list.auto_number = auto_number

    @property
    def number(self) -> str:
        return self.attribute_list.number

    @number.setter
    def number(self, number: str) -> None:
        self.attribute_list.number = number

    @property
    def programming_language(self) -> Optional[ProgrammingLanguage]:
        return self.attribute_list.programming_language

    @programming_language.setter
    def programming_language(self, programming_language: ProgrammingLanguage) -> None:
        self.attribute_list.programming_language = programming_language

    @property
    def name(self) -> str:
        return self.attribute_list.name

    @name.setter
    def name(self, name: str) -> None:
        self.attribute_list.name = name

    @property
    def statics(self) -> list[Member]:
        return self.attribute_list.interface.sections.static.members

    @statics.setter
    def statics(self, statics: list[Member]) -> None:
        raise AttributeError("Statics cannot be set")
