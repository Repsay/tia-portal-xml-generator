from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET

class MultiLanguageText(XMLBase):
    element_name = "MultiLanguageText"

    def __init__(self, text: str, language: str = "en-US"):
        super().__init__()
        self.element = ET.Element(self.element_name, {"Lang": language})
        self.element.text = text
