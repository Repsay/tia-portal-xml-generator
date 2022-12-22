import json
from typing import Any, Optional
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET

class TemplateValue(XMLBase):
    element_name = "TemplateValue"

    def __init__(self, name: str, type: str, value: Any):
        super().__init__()
        self.element = ET.Element(self.element_name)
        self.element.set("Name", name)
        self.element.set("Type", type)
        self.element.text = str(value)

class Part(XMLBase):
    element_name = "Part"
    part_info_path = "data/parts.json"

    def __init__(self, name: str, version: Optional[str], id: int):
        super().__init__()
        self.id: int = id
        self.name = name
        self.element = ET.Element(self.element_name)
        self.element.set("Name", name)

        if version is not None:
            self.element.set("Version", version)

        self.element.set("UId", str(id))

        self.part_info = self.get_part_info(name, version)

        if self.part_info["multiple_outputs"]:
            self.add(TemplateValue("Card", "Cardinality", 1))

            outputs = []
            for i, output in enumerate(self.part_info["outputs"]):
                outputs.append(f"{output}{i+1}")

            self.part_info["outputs"] = outputs

    def get_part_info(self, name: str, version: Optional[str]) -> dict[str, list[str]]:
        with open(self.part_info_path, "r") as f:
            part_options = json.load(f)

        if version is None:
            return part_options[name]["None"]
        else:
            return part_options[name][version]