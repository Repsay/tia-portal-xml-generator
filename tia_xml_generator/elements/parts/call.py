from typing import Optional
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET


class CallInstance(XMLBase):
    element_name = "Instance"

    def __init__(self, id: int, scope: str):
        super().__init__()
        self.element = ET.Element(self.element_name, {"UId": str(id), "Scope": scope})

    def add_component(self, name: str) -> None:
        component = CallInstanceComponent(name)
        self.add(component)


class CallInstanceComponent(XMLBase):
    element_name = "Component"

    def __init__(self, name: str):
        super().__init__()
        self.element = ET.Element(self.element_name, {"Name": name})


class CallInfo(XMLBase):
    element_name = "CallInfo"

    def __init__(self, name: str, type: Optional[str]):
        super().__init__()
        if type is None:
            self.element = ET.Element(self.element_name, {"Name": name})
        else:
            self.element = ET.Element(self.element_name, {"Name": name, "BlockType": type})

    def add_instance(self, id: int, scope: str, name: str) -> None:
        instance = CallInstance(id, scope)
        instance.add_component(name)
        self.add(instance)


class Call(XMLBase):
    element_name = "Call"

    def __init__(self, id: int, name: str, block_type: Optional[str]):
        super().__init__()
        self.element = ET.Element(self.element_name, {"UId": str(id)})
        self.id: int = id
        self.name = name

        self.load_call_info(name, block_type)

    def load_call_info(self, name: str, block_type: Optional[str]) -> CallInfo:
        self.call_info = CallInfo(name, block_type)
        self.add(self.call_info)
        return self.call_info

    def add_instance_db(self, id: int, name: str) -> None:
        self.call_info.add_instance(id, "GlobalVariable", name)

    def add_instance_variable(self, id: int, name: str) -> None:
        self.call_info.add_instance(id, "LocalVariable", name)
