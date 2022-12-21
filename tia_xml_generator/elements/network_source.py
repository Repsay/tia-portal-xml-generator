from tia_xml_generator.elements.basis import Basis
import xml.etree.ElementTree as ET

from tia_xml_generator.elements.flg_net import FlgNet

class NetworkSource(Basis):
    element_name = "NetworkSource"

    def __init__(self):
        super().__init__()
        self.element = ET.Element(self.element_name)

        self.load_flg_net()

    def load_flg_net(self) -> None:
        self.flg_net = FlgNet()
        self.add(self.flg_net)

    def build(self) -> ET.Element:
        self.flg_net.build()
        if len(self.flg_net.children) == 0:
            self.remove(self.flg_net)
        return super().build()

    def add_part(self, name: str, version: str):
        self.flg_net.add_part(name, version)