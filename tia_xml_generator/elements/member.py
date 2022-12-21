from tia_xml_generator.elements.attribute_list import AttributeList
from tia_xml_generator.elements.basis import Basis
import xml.etree.ElementTree as ET

from tia_xml_generator.elements.comment import Comment

class AttributeListMember(AttributeList):
    __external_accessible = ET.Element("BooleanAttribute", {"Name": "ExternalAccessible", "SytemDefined": "true"})
    __external_visible = ET.Element("BooleanAttribute", {"Name": "ExternalVisible", "SytemDefined": "true"})
    __external_writable = ET.Element("BooleanAttribute", {"Name": "ExternalWritable", "SytemDefined": "true"})

    def __init__(self, external_accessible: bool = False, external_visible: bool = False, external_writable: bool = False):
        super().__init__()
        self.element.extend([self.__external_accessible, self.__external_visible, self.__external_writable])
        self.external_accessible = external_accessible
        self.external_visible = external_visible
        self.external_writable = external_writable

    @property
    def external_accessible(self) -> bool:
        if self.__external_accessible.text is None:
            return False
        return self.__external_accessible.text == "true"

    @external_accessible.setter
    def external_accessible(self, external_accessible: bool) -> None:
        self.__external_accessible.text = "true" if external_accessible else "false"

    @property
    def external_visible(self) -> bool:
        if self.__external_visible.text is None:
            return False
        return self.__external_visible.text == "true"

    @external_visible.setter
    def external_visible(self, external_visible: bool) -> None:
        self.__external_visible.text = "true" if external_visible else "false"

    @property
    def external_writable(self) -> bool:
        if self.__external_writable.text is None:
            return False
        return self.__external_writable.text == "true"

    @external_writable.setter
    def external_writable(self, external_writable: bool) -> None:
        self.__external_writable.text = "true" if external_writable else "false"

class Member(Basis):
    element_name = "Member"

    __comment = None

    def __init__(self, name: str, type: str):
        super().__init__()
        self.element = ET.Element(self.element_name, {"Name": name, "Datatype": type})
        self.load_attribute_list()

    def load_attribute_list(self) -> None:
        self.attribute_list = AttributeListMember()
        self.add(self.attribute_list)

    def add_comment(self, comment: str, language: str = "en-US") -> None:
        if self.__comment is None:
            self.__comment = Comment(comment, language)
            self.add(self.__comment)
        else:
            self.__comment.add(comment, language)
