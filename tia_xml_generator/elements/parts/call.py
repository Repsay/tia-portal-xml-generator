from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET


class CallInfo(XMLBase):
    element_name = "CallInfo"

    def __init__(self, name: str, type: str):
        super().__init__()
        self.element = ET.Element(self.element_name, {"Name": name, "BlockType": type})

class Call(XMLBase):
    element_name = "Call"

    def __init__(self, id: int, name: str, block_type: str):
        super().__init__()
        self.element = ET.Element(self.element_name, {"UId": str(id)})
        self.id: int = id
        self.name = name

        self.load_call_info(name, block_type)

    def load_call_info(self, name: str, block_type: str) -> None:
        self.call_info = CallInfo(name, block_type)
        self.add(self.call_info)
