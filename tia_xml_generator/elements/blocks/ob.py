from copy import deepcopy
from typing import Optional
import xml.etree.ElementTree as ET
from tia_xml_generator.elements.compile_unit import CompileUnit
from tia_xml_generator.elements.multilingual_text import MultilingualText
from tia_xml_generator.enums import ProgrammingLanguage, SecondaryType
from tia_xml_generator.elements.attribute_list import AttributeList

from tia_xml_generator.elements.basis import XMLBase
from tia_xml_generator.elements.blocks import Block
from tia_xml_generator.elements.interface import InterfaceOB
from tia_xml_generator.elements.member import Member
from tia_xml_generator.elements.object_list import ObjectList


class AttributeListOB(AttributeList):
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
        self.__secondary_type = ET.Element("SecondaryType")
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
        self.element.extend([self.__name, self.__programming_language, self.__secondary_type])
        self.load_interface()

    def load_interface(self) -> None:
        self.interface = InterfaceOB()
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

    @property
    def secondary_type(self) -> str:
        if self.__secondary_type.text is None:
            return ""
        return self.__secondary_type.text

    @secondary_type.setter
    def secondary_type(self, secondary_type: SecondaryType) -> None:
        self.__secondary_type.text = secondary_type.name
        if self.element.find("SecondaryType") is None:
            self.element.append(self.__secondary_type)


class ObjectListOB(ObjectList):

    network_groups: dict[str, int]

    networks: dict[str, dict[int, CompileUnit]]

    def __init__(self, name: str, description: str):
        self.network_groups = {}
        self.networks = {}
        super().__init__()
        self.title = MultilingualText("Title")
        self.comment = MultilingualText("Comment")

        self.add(self.title)
        self.add(self.comment)

        self.title.add_text(name)
        self.comment.add_text(description)

    def add_network(
        self, name: str, comment: str, group: str, order: int, programming_language: ProgrammingLanguage
    ) -> CompileUnit:
        if group not in self.network_groups:
            raise ValueError(f"Group {group} not found")
        if group not in self.networks:
            self.networks[group] = {}

        if order in self.networks[group]:
            for i in range(max(self.network_groups.values()), order, -1):
                self.networks[group][i] = self.networks[group][i - 1]

        network = CompileUnit(name, programming_language, comment)
        self.networks[group][order] = network

        return network

    def add_network_group(self, name: str, comment: str, order: int, programming_language: ProgrammingLanguage) -> None:
        if name in self.network_groups:
            raise ValueError(f"Group {name} already exists")
        if order in self.network_groups.values():
            for i in range(max(self.network_groups.values()), order, -1):
                for key, value in self.network_groups.items():
                    if value == i:
                        self.network_groups[key] = i + 1
        self.network_groups[name] = order

        self.add_network(f"***{name}***", comment, name, 0, programming_language)

    def build(self) -> ET.Element:
        self_ = deepcopy(self)
        for group in dict(sorted(self_.network_groups.items(), key=lambda x: x[1])):
            for network in dict(sorted(self_.networks[group].items(), key=lambda x: x[0])).values():
                self_.element.append(network.build())
        self_.element.extend([self_.title.build(), self_.comment.build()])

        return self_.element

    def build_no_call(self) -> ET.Element:
        self_ = deepcopy(self)
        for group in dict(sorted(self_.network_groups.items(), key=lambda x: x[1])):
            for network in dict(sorted(self_.networks[group].items(), key=lambda x: x[0])).values():
                self_.element.append(network.build_no_call())
        self_.element.extend([self_.title.build_no_call(), self_.comment.build_no_call()])

        return self_.element


class OB(XMLBase, Block):
    element_name = "SW.Blocks.OB"
    attribute_list: AttributeListOB

    def __init__(
        self, name: str, programming_language: ProgrammingLanguage, description: str, secondary_type: SecondaryType
    ):
        super().__init__()
        self.load_attribute_list()
        self.id = self.global_id.next()
        self.description = description
        self.name = name
        self.programming_language = programming_language
        self.secondary_type = secondary_type
        self.element = ET.Element(self.element_name, {"ID": self.id})
        self.load_object_list()

    def load_attribute_list(self) -> None:
        self.attribute_list = AttributeListOB()
        self.add(self.attribute_list)

    def load_object_list(self) -> None:
        self.object_list = ObjectListOB(self.name, self.description)
        self.add(self.object_list)

    def add_temp(self, name: str, data_type: str) -> Member:
        return self.attribute_list.interface.sections.temp.add_member(name, data_type)

    def add_constant(self, name: str, data_type: str) -> Member:
        return self.attribute_list.interface.sections.constant.add_member(name, data_type)

    def get_input(self, name: str) -> Optional[Member]:
        return self.attribute_list.interface.sections.input.get_member(name)

    def get_temp(self, name: str) -> Optional[Member]:
        return self.attribute_list.interface.sections.temp.get_member(name)

    def get_constant(self, name: str) -> Optional[Member]:
        return self.attribute_list.interface.sections.constant.get_member(name)

    def add_network(
        self,
        name: str,
        comment: str,
        group: str,
        order: Optional[int] = None,
        programming_language: Optional[ProgrammingLanguage] = None,
    ) -> CompileUnit:
        programming_language = programming_language if programming_language is not None else self.programming_language
        if programming_language is None:
            raise ValueError("Programming language is not defined")
        if order is None:
            order = len(self.object_list.networks[group])
        return self.object_list.add_network(name, comment, group, order, programming_language)

    def add_network_group(
        self,
        name: str,
        comment: str,
        order: Optional[int] = None,
        programming_language: Optional[ProgrammingLanguage] = None,
    ) -> None:
        programming_language = programming_language if programming_language is not None else self.programming_language
        if programming_language is None:
            raise ValueError("Programming language is not defined")
        if order is None:
            order = len(self.object_list.network_groups)
        self.object_list.add_network_group(name, comment, order, programming_language)

    def get_network(self, name: str) -> CompileUnit:
        for group in self.object_list.networks.values():
            for network in group.values():
                if network.name == name:
                    return network
        raise ValueError(f"Network {name} not found")

    def get_networks_in_group(self, group: str) -> list[CompileUnit]:
        if group not in self.object_list.network_groups:
            raise ValueError(f"Network group {group} not found")
        return list(self.object_list.networks[group].values())

    @property
    def network_groups(self) -> list[str]:
        return list(self.object_list.network_groups.keys())

    @network_groups.setter
    def network_groups(self, network_groups: list[str]) -> None:
        raise AttributeError("Network groups cannot be set")

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
    def secondary_type(self) -> str:
        return self.attribute_list.secondary_type

    @secondary_type.setter
    def secondary_type(self, secondary_type: SecondaryType) -> None:
        self.attribute_list.secondary_type = secondary_type

    @property
    def name(self) -> str:
        return self.attribute_list.name

    @name.setter
    def name(self, name: str) -> None:
        self.attribute_list.name = name

    @property
    def inputs(self) -> list[Member]:
        return self.attribute_list.interface.sections.input.members

    @inputs.setter
    def inputs(self, inputs: list[Member]) -> None:
        raise AttributeError("Inputs cannot be set")

    @property
    def temps(self) -> list[Member]:
        return self.attribute_list.interface.sections.temp.members

    @temps.setter
    def temps(self, temps: list[Member]) -> None:
        raise AttributeError("Temps cannot be set")

    @property
    def constants(self) -> list[Member]:
        return self.attribute_list.interface.sections.constant.members

    @constants.setter
    def constants(self, constants: list[Member]) -> None:
        raise AttributeError("Constants cannot be set")

    @property
    def networks(self) -> list[CompileUnit]:
        networks: list[CompileUnit] = []
        for group in self.object_list.networks.values():
            networks.extend(group.values())
        return networks

    @networks.setter
    def networks(self, networks: list[CompileUnit]) -> None:
        raise AttributeError("Networks cannot be set")
