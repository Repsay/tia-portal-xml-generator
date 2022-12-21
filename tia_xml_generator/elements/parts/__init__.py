import os
from tia_xml_generator.elements.basis import Basis
import xml.etree.ElementTree as ET
import pandas as pd
import json

class Parts(Basis):
    element_name = "Parts"
    path = "data/parts.xlsx"
    part_path = "data/parts"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)
        self.part_id = 21

        if not os.path.exists(self.path):
            os.makedirs(os.path.join(os.path.dirname(self.path), "parts"), exist_ok=True)
            df = pd.DataFrame(columns=["Name", "Version"])
            df.to_excel(self.path, index=False) # type: ignore

        self.part_options: pd.DataFrame = pd.read_excel(self.path) # type: ignore



    def add_part(self, name: str, version: str):
        self.part_id += 1
        if not self.part_options.loc[(self.part_options["Name"] == name) & (self.part_options["Version"] == version)].empty:
            # part = Part(name, version, self.part_id)
            # self.add(part)
            pass
        else:
            self.part_options: pd.DataFrame = self.part_options.append({"Name": name, "Version": version}, ignore_index=True) # type: ignore
            print("Part is not defined")
            information = {"inputs": [], "outputs": []}
            while True:
                new_input = input("Give the name of the input:")
                if new_input == "q":
                    break
                information["inputs"].append(new_input.strip())

            while True:
                new_output = input("Give the name of the output:")
                if new_output == "q":
                    break
                information["outputs"].append(new_output.strip())

            part_file = os.path.join(self.part_path, f"{name}_{version}.json")

            with open(part_file, "w") as f:
                f.write(json.dumps(information))

            raise ValueError("Part does not exist in the excel file")
