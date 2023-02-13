from typing import Optional
from tia_xml_generator.elements.basis import XMLBase
import xml.etree.ElementTree as ET


class Connection(XMLBase):
    def __init__(self, type: str, source: Optional[int], target: Optional[str]):
        super().__init__()
        self.element = ET.Element(type)
        self.source = source
        self.target = target

        if source is not None:
            self.element.set("UId", str(source))

        if target is not None:
            self.element.set("Name", target)


class Wire(XMLBase):
    element_name = "Wire"

    def __init__(self, id: int, type: str, source: int, target: Optional[str]):
        super().__init__()
        self.element = ET.Element(self.element_name, {"UId": str(id)})
        self.source = source
        self.add_connection(type, source, target)

    def add_connection(self, type: str, source: int, target: Optional[str] = None) -> Connection:
        connection = Connection(type, source, target)
        self.add(connection)
        return connection

    def add_powerrail(self) -> Connection:
        connection = Connection("Powerrail", None, None)
        self.add(connection)
        return connection

    def get_connections(self) -> list[Connection]:
        temp: list[Connection] = []
        for child in self.children:
            if isinstance(child, Connection):
                temp.append(child)
        return temp

    def get_connections_description(self) -> str:
        connections = self.get_connections()
        if len(connections) == 0:
            return ""
        else:
            text = ""
            for i, connection in enumerate(connections):
                text += f"{i}: {connection.source} -> {connection.target}\n"
            return text
