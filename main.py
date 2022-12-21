from tia_xml_generator.enums import ProgrammingLanguage
from tia_xml_generator.elements import document

doc = document.Document()
fb = doc.add_fb("test_fb", ProgrammingLanguage.LAD, "This is a test FB")

fb.author = "Jasper"
fb.family = "test_family"

in1 = fb.add_input("in1", "BOOL")
in1.add_comment("This is a comment")

test_network = fb.add_network("test_network", "this is a test network")
test_network.add_part("GetBlockName", "1.1")

doc.save("test.xml")