from datetime import datetime
import xml.etree.ElementTree as ET
from tia_xml_generator.enums import ProgrammingLanguage
from tia_xml_generator.elements.basis import Basis
from tia_xml_generator.elements.blocks.fb import FB

class Document(Basis):
    element_name = "Document"

    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.element = ET.Element(self.element_name)
        self.load_document_info()

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

    def save(self, path: str) -> None:
        """Saves the document."""
        tree = ET.ElementTree(self.build())
        tree.write(path, encoding="utf-8", xml_declaration=True)