from datetime import datetime
import os
import pickle
from typing import Self
import xml.etree.ElementTree as ET
from tia_xml_generator.enums import ProgrammingLanguage, SecondaryType
from tia_xml_generator.elements.basis import XMLBase
from tia_xml_generator.elements.blocks.fb import FB
from tia_xml_generator.elements.blocks.db import DB
from tia_xml_generator.elements.blocks.ob import OB


class Document(XMLBase):
    element_name = "Document"

    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.global_id_saved = None
        self.element = ET.Element(self.element_name)
        self.load_document_info()

        if not os.path.exists(self.template_path):
            os.mkdir(self.template_path)

        if not os.path.exists(self.import_path):
            os.mkdir(self.import_path)

        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)

    @property
    def fbs(self) -> list[FB]:
        """Returns all FBs in the document."""
        return [child for child in self.children if isinstance(child, FB)]

    @property
    def dbs(self) -> list[DB]:
        """Returns all DBs in the document."""
        return [child for child in self.children if isinstance(child, DB)]

    @property
    def obs(self) -> list[OB]:
        """Returns all OBs in the document."""
        return [child for child in self.children if isinstance(child, OB)]

    def load_document_info(self) -> None:
        """Loads the document info."""
        document_info = ET.SubElement(self.element, "DocumentInfo")
        document_info_created = ET.SubElement(document_info, "Created")
        document_info_created.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        document_info_export_settings = ET.SubElement(document_info, "ExportSettings")
        document_info_export_settings.text = "None"

        # It is not necessary to add the InstalledProducts to the DocumentInfo

    def add_fb(self, name: str, programming_language: ProgrammingLanguage, description: str) -> FB:
        """Adds a FB to the document."""
        fb = FB(name, programming_language, description)
        self.add(fb)
        return fb

    def get_fb(self, name: str) -> FB:
        """Returns a FB from the document."""
        for child in self.children:
            if isinstance(child, FB):
                if child.name == name:
                    return child

        raise ValueError(f"The FB '{name}' does not exist in the document.")

    def add_db(self, name: str) -> DB:
        """Adds a DB to the document."""
        db = DB(name)
        self.add(db)
        return db

    def get_db(self, name: str) -> DB:
        """Returns a DB from the document."""
        for child in self.children:
            if isinstance(child, DB):
                if child.name == name:
                    return child

        raise ValueError(f"The DB '{name}' does not exist in the document.")

    def add_ob(
        self, name: str, programming_language: ProgrammingLanguage, description: str, secondary_type: SecondaryType
    ) -> OB:
        """Adds a OB to the document."""
        ob = OB(name, programming_language, description, secondary_type)
        self.add(ob)
        return ob

    def get_ob(self, name: str) -> OB:
        """Returns a OB from the document."""
        for child in self.children:
            if isinstance(child, OB):
                if child.name == name:
                    return child

        raise ValueError(f"The OB '{name}' does not exist in the document.")

    def save_template(self, name: str, overwrite: bool = False, temp: bool = False) -> None:
        """Saves the document as a template."""
        self.global_id_saved = self.global_id.id
        if not temp:
            path = os.path.join(self.template_path, f"{name}.pkl")
        else:
            path = os.path.join(self.temp_path, f"{name}.pkl")

        if os.path.exists(path) and not (overwrite or temp):
            raise FileExistsError(f"The file '{path}' already exists.")

        with open(path, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load_template(cls, name: str, temp: bool = False) -> Self:
        """Loads a template."""
        if not name.endswith(".pkl"):
            name = f"{name}.pkl"

        if not os.path.isfile(name):
            if not temp:
                path = os.path.join(cls.template_path, name)
            else:
                path = os.path.join(cls.temp_path, name)

            if not os.path.exists(path) and not temp:
                path = os.path.join(cls.temp_path, name)

            if not os.path.exists(path) and temp:
                path = os.path.join(cls.template_path, name)

            if not os.path.exists(path):
                raise FileNotFoundError(f"The file '{path}' does not exist.")
        else:
            path = name

        with open(path, "rb") as f:
            doc: Self = pickle.load(f)

            if not os.path.exists(doc.template_path):
                os.mkdir(doc.template_path)

            if not os.path.exists(doc.import_path):
                os.mkdir(doc.import_path)

            doc.global_id.reset(doc.global_id_saved)
            doc.global_id_saved = None

            return doc

    # @classmethod
    # def load_from_file(cls, path: str) -> Self:
    #     """Loads a document from a file."""
    #     if not path.endswith(".xml"):
    #         path = f"{path}.xml"
    #     if not os.path.exists(path):
    #         raise FileNotFoundError(f"The file '{path}' does not exist.")

    #     tree = ET.parse(path)
    #     root = tree.getroot()
    #     if root is None:
    #         raise ValueError(f"The file '{path}' does not contain a document.")
    #     document = cls()

    #     for child in root:
    #         if child.tag == "DocumentInfo":
    #             old_document_info = document.element.find("DocumentInfo")
    #             if not old_document_info is None:
    #                 document.element.remove(old_document_info)
    #             document.element.append(child)
    #         elif child.tag == "SW.Blocks.FB":
    #             fb_name = child.find("AttributeList/Name")
    #             fb_name = fb_name.text if not fb_name is None else None
    #             if fb_name is None:
    #                 raise ValueError("The FB does not have a name.")
    #             fb_language = child.find("AttributeList/ProgrammingLanguage")
    #             fb_language = fb_language.text if not fb_language is None else None
    #             if fb_language is None:
    #                 raise ValueError("The FB does not have a programming language.")
    #             fb_language = ProgrammingLanguage[fb_language]
    #             fb_description = child.find(
    #                 "ObjectList/MultilingualText[@CompositionName='Comment']/ObjectList/MultilingualTextItem/AttributeList/Text"
    #             )
    #             fb_description = fb_description.text if not fb_description is None else None
    #             if fb_description is None:
    #                 fb_description = ""
    #             fb = document.add_fb(fb_name, fb_language, fb_description)

    #             fb_attributes = child.find("AttributeList")
    #             fb_objects = child.find("ObjectList")

    #             if fb_attributes is None:
    #                 raise ValueError("The FB does not have any attributes.")

    #             for fb_attribute in fb_attributes:
    #                 if fb_attribute.tag == "Name" or fb_attribute.tag == "ProgrammingLanguage":
    #                     continue
    #                 if fb_attribute.tag == "AutoNumber":
    #                     fb.auto_number = True if fb_attribute.text == "true" else False
    #                 elif fb_attribute.tag == "HeaderAuthor":
    #                     fb.author = fb_attribute.text if not fb_attribute.text is None else ""
    #                 elif fb_attribute.tag == "HeaderVersion":
    #                     fb.version = fb_attribute.text if not fb_attribute.text is None else ""
    #                 elif fb_attribute.tag == "HeaderFamily":
    #                     fb.family = fb_attribute.text if not fb_attribute.text is None else ""
    #                 elif fb_attribute.tag == "Interface":
    #                     sections = fb_attribute.find(
    #                         "xmlns:Sections", {"xmlns": "http://www.siemens.com/automation/Openness/SW/Interface/v3"}
    #                     )

    #                     if sections is None:
    #                         raise ValueError("The FB interface does not have any sections.")

    #                     for section in sections.findall(
    #                         "xmlns:Section", {"xmlns": "http://www.siemens.com/automation/Openness/SW/Interface/v3"}
    #                     ):
    #                         members = section.findall(
    #                             "xmlns:Member", {"xmlns": "http://www.siemens.com/automation/Openness/SW/Interface/v3"}
    #                         )
    #                         for member in members:
    #                             member_name = member.get("Name")
    #                             member_type = member.get("Datatype")
    #                             if member_name is None or member_type is None:
    #                                 raise ValueError("The FB interface does not have a name or a type.")

    #                             if section.get("Name") == "Input":
    #                                 fb.add_input(member_name, member_type)
    #                             elif section.get("Name") == "Output":
    #                                 fb.add_output(member_name, member_type)
    #                             elif section.get("Name") == "InOut":
    #                                 fb.add_in_out(member_name, member_type)
    #                             elif section.get("Name") == "Static":
    #                                 fb.add_static(member_name, member_type)
    #                             elif section.get("Name") == "Temp":
    #                                 fb.add_temp(member_name, member_type)
    #                             elif section.get("Name") == "Constant":
    #                                 fb.add_constant(member_name, member_type)
    #                             else:
    #                                 raise ValueError("The FB interface does not have a valid section.")
    #                 elif fb_attribute.tag == "MemoryLayout":
    #                     fb.memory_layout = fb_attribute.text if not fb_attribute.text is None else ""
    #                 elif fb_attribute.tag == "Number":
    #                     fb.number = fb_attribute.text if not fb_attribute.text is None else ""

    #             if fb_objects is None:
    #                 raise ValueError("The FB does not have any objects.")

    #             fb_compile_units = fb_objects.findall("SW.Blocks.CompileUnit")

    #             networks: list[tuple[str, str]] = []

    #             for fb_compile_unit in fb_compile_units:
    #                 is_group = False
    #                 unit_name = fb_compile_unit.find(
    #                     "ObjectList/MultilingualText[@CompositionName='Title']/ObjectList/MultilingualTextItem/AttributeList/Text"
    #                 )
    #                 unit_name = unit_name.text if not unit_name is None else None
    #                 if unit_name is None:
    #                     raise ValueError("The FB compile unit does not have a name.")
    #                 if unit_name.startswith("***"):
    #                     is_group = True
    #                     unit_name = unit_name.replace("***", "")

    #                 unit_description = fb_compile_unit.find(
    #                     "ObjectList/MultilingualText[@CompositionName='Comment']/ObjectList/MultilingualTextItem/AttributeList/Text"
    #                 )

    #                 unit_description = unit_description.text if not unit_description is None else ""
    #                 unit_description = unit_description if not unit_description is None else ""

    #                 if is_group:
    #                     fb.add_network_group(unit_name, unit_description)
    #                     continue

    #                 networks.append((unit_name, unit_description))

    #             print("Networks needs groups to be added")
    #             print(f"group options are: {'-'.join(fb.network_groups)}")
    #             for network in networks:
    #                 group = input(f"Group for network {network[0]}: ")
    #                 fb.add_network(network[0], network[1], group)

    #             for fb_compile_unit in fb_compile_units:
    #                 unit_name = fb_compile_unit.find(
    #                     "ObjectList/MultilingualText[@CompositionName='Title']/ObjectList/MultilingualTextItem/AttributeList/Text"
    #                 )
    #                 unit_name = unit_name.text if not unit_name is None else None
    #                 if unit_name is None:
    #                     raise ValueError("The FB compile unit does not have a name.")
    #                 if unit_name.startswith("***"):
    #                     continue

    #                 network = fb.get_network(unit_name)

    #                 if network is None:
    #                     raise ValueError("The FB compile unit does not have a network.")

    #                 attributes = fb_compile_unit.find("AttributeList")
    #                 if attributes is None:
    #                     raise ValueError("The FB compile unit does not have any attributes.")
    #                 network_source = attributes.find("NetworkSource")
    #                 if network_source is None:
    #                     raise ValueError("The FB compile unit does not have a network source.")

    #                 ns = {"xmlns": "http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v3"}
    #                 flg_net = network_source.find("xmlns:FlgNet", ns)

    #                 if flg_net is None:
    #                     continue

    #                 parts = flg_net.find("xmlns:Parts", ns)

    #                 if not parts is None:
    #                     parts_list = parts.findall("xmlns:Part", ns)

    #                     for part in parts_list:
    #                         part_name = part.get("Name")
    #                         part_version = part.get("Version")

    #                         if part_name is None:
    #                             raise ValueError("The FB network part does not have a name.")

    #                         network.add_part(part_name, part_version)

    #                     call_list = parts.findall("xmlns:Call", ns)

    #                     for call in call_list:
    #                         call_info = call.find("xmlns:CallInfo", ns)
    #                         if call_info is None:
    #                             raise ValueError("The FB network call does not have call info.")
    #                         call_name = call_info.get("Name")
    #                         call_block_type = call_info.get("BlockType")

    #                         if call_name is None or call_block_type is None:
    #                             raise ValueError("The FB network call does not have a name or a block type.")

    #                         # network.add_call(call_name, call_block_type)

    #     return document

    def save(self, file_name: str) -> str:
        """Saves the document."""
        tree = ET.ElementTree(self.build())
        path = os.path.join(self.import_path, f"{file_name}.xml")
        if os.path.isfile(path):
            os.remove(path)
        tree.write(path, encoding="utf-8", xml_declaration=True)

        return path

    def save_no_call(self, file_name: str) -> str:
        """Saves the document without the calls."""
        tree = ET.ElementTree(self.build_no_call())
        path = os.path.join(self.import_path, f"{file_name}_no_call.xml")
        if os.path.isfile(path):
            os.remove(path)
        tree.write(path, encoding="utf-8", xml_declaration=True)

        return path
