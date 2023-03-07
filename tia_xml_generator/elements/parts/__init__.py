from copy import deepcopy
import os
from typing import Any, Optional
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET
import json
from tia_xml_generator.elements.parts.call import Call

from tia_xml_generator.elements.parts.part import Part


class Parts(XMLBase):
    element_name = "Parts"

    def __init__(self):
        super().__init__()
        self.path = os.path.join(self.home_path, "parts.json")
        self.element = ET.Element(self.element_name)
        self.part_id = 21
        self.part_options: dict[str, Any] = {}

        if not os.path.exists(self.path):
            os.makedirs(os.path.join(os.path.dirname(self.path), "parts"), exist_ok=True)
            with open(self.path, "w") as f:
                f.write(json.dumps({}))

        with open(self.path, "r") as f:
            self.part_options = json.load(f)

    def add_part(self, name: str, version: Optional[str] = None) -> Part:
        part_not_found = False
        if version is None:
            if not self.part_options.get(name, None) is None:
                part = Part(name, version, self.part_id)
                self.add(part)
                self.part_id += 1
                return part
            else:
                part_not_found = True
        else:
            if not self.part_options.get(name, {}).get(version, None) is None:
                part = Part(name, version, self.part_id)
                self.add(part)
                self.part_id += 1
                return part
            else:
                part_not_found = True

        if part_not_found:
            print(f"Part '{name}' is not defined")
            information: dict[str, Any] = {"inputs": [], "outputs": []}

            while True:
                new_input = input("Give the name of the input (send q to exit): ")
                if new_input == "q":
                    break
                information["inputs"].append(new_input.strip())

            multiple_out = input("Is it possible to add more outputs (y/n): ")
            if multiple_out == "y":
                information["multiple_outputs"] = True
            else:
                information["multiple_outputs"] = False

            while True:
                new_output = input("Give the name of the output (send q to exit): ")
                if new_output == "q":
                    break
                information["outputs"].append(new_output.strip())

            if not self.part_options.get(name, None) is None:
                if version is None:
                    self.part_options[name]["None"] = information
                else:
                    self.part_options[name][version] = information
            else:
                if version is None:
                    self.part_options[name] = {"None": information}
                else:
                    self.part_options[name] = {version: information}

            with open(self.path, "w") as f:
                f.write(json.dumps(self.part_options))

            part = Part(name, version, self.part_id)
            self.add(part)

            self.part_id += 1
            return part
        else:
            raise Exception("Something went wrong, very wrong")

    def get_part(self, name: str) -> Optional[list[Part]]:
        temp: list[Part] = []
        for child in self.children:
            if isinstance(child, Part):
                if child.name == name:
                    temp.append(child)
        if len(temp) == 0:
            return None
        else:
            return temp

    def add_call(
        self, name: str, block_type: Optional[str], reference: Optional[str], reference_type: Optional[str]
    ) -> Call:
        call = Call(self.part_id, name, block_type)
        self.part_id += 1
        if not reference is None and not reference_type is None:
            if reference_type == "DB":
                call.add_instance_db(self.part_id, reference)
            elif reference_type == "Variable":
                call.add_instance_variable(self.part_id, reference)
            else:
                raise ValueError(f"Reference type '{reference_type}' is not supported")
            self.part_id += 1
        self.add(call)
        return call

    def get_call(self, name: str) -> Optional[list[Call]]:
        temp: list[Call] = []
        for child in self.children:
            if isinstance(child, Call):
                if child.name == name:
                    temp.append(child)
        if len(temp) == 0:
            return None
        else:
            return temp

    def build_no_call(self) -> ET.Element:
        self_ = deepcopy(self)
        self_.element.extend([child.build_no_call() for child in self.children if not isinstance(child, Call)])
        return self_.element
