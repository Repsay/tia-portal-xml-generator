from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET

from tia_xml_generator.elements.multi_language_text import MultiLanguageText

class Comment(XMLBase):
    element_name = "Comment"

    def __init__(self, comment: str, language: str = "en-US"):
        super().__init__()
        self.element = ET.Element(self.element_name)

        self.add(comment, language)

    def add(self, comment: str, language: str = "en-US") -> None:
        self.children.append(MultiLanguageText(comment, language))
