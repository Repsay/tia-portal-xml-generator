from typing import Optional, Protocol, Self, Union
import xml.etree.ElementTree as ET

class ID:
    """Global ID class."""
    id: int

    def __init__(self) -> None:
        self.id = 0

    def next(self) -> str:
        r_value = self.id
        self.id += 1

        if r_value == 0:
            return str(0)
        else:
            return hex(r_value).lstrip("0x").rstrip("L").upper()


class XMLElement(Protocol):
    element_name: str
    """The name of the XML element."""
    element: ET.Element
    """The XML element."""
    id: Optional[str]
    """The ID of the XML element."""
    children: list[Self]

    def build(self) -> ET.Element:
        """Builds the XML element."""
        ...

class Basis(XMLElement):
    """Protocol for all basis classes."""
    element_name: str
    """The name of the XML element."""
    element: ET.Element
    """The XML element."""
    children: list[XMLElement]
    """The child elements of the XML element."""
    id: Optional[str]
    """The ID of the XML element."""
    global_id: ID = ID()

    def __init__(self) -> None:
        self.children = []

    def build(self) -> ET.Element:
        """Builds the XML element."""
        self.element.extend([child.build() for child in self.children])
        return self.element

    def add(self, child: Union[list[XMLElement], XMLElement]) -> None:
        """Adds a child element to the XML element."""
        if isinstance(child, list):
            self.children.extend(child)
        else:
            self.children.append(child)

    def remove(self, child: XMLElement) -> None:
        """Removes a child element from the XML element."""
        self.children.remove(child)