from tia_xml_generator.elements.basis import XMLBase

import xml.etree.ElementTree as ET

from tia_xml_generator.elements.section import Section


class InterfaceSections(XMLBase):
    element_name = "Sections"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(
            self.element_name, {"xmlns": "http://www.siemens.com/automation/Openness/SW/Interface/v3"}
        )

        self.input = Section("Input")
        self.output = Section("Output")
        self.in_out = Section("InOut")
        self.static = Section("Static")
        self.temp = Section("Temp")
        self.constant = Section("Constant")

        self.add([self.input, self.output, self.in_out, self.static, self.temp, self.constant])


class InterfaceSectionsDB(XMLBase):
    element_name = "Sections"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(
            self.element_name, {"xmlns": "http://www.siemens.com/automation/Openness/SW/Interface/v3"}
        )

        self.static = Section("Static")

        self.add([self.static])


class InterfaceSectionsOB(XMLBase):
    element_name = "Sections"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(
            self.element_name, {"xmlns": "http://www.siemens.com/automation/Openness/SW/Interface/v3"}
        )

        self.input = Section("Input")
        self.temp = Section("Temp")
        self.constant = Section("Constant")

        self.add([self.input, self.temp, self.constant])


class Interface(XMLBase):
    element_name = "Interface"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)
        self.load_sections()

    def load_sections(self) -> None:
        self.sections = InterfaceSections()
        self.add(self.sections)


class InterfaceDB(XMLBase):
    element_name = "Interface"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)
        self.load_sections()

    def load_sections(self) -> None:
        self.sections = InterfaceSectionsDB()
        self.add(self.sections)


class InterfaceOB(XMLBase):
    element_name = "Interface"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)
        self.load_sections()

    def load_sections(self) -> None:
        self.sections = InterfaceSectionsOB()
        self.add(self.sections)
