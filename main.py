from tia_xml_generator.enums import MemoryLayout, ProgrammingLanguage, SecondaryType
from tia_xml_generator.elements import document


def make_general_fb_temp():
    doc = document.Document()
    fb = doc.add_fb("", ProgrammingLanguage.FBD, "The block is used to control EM{} and all its associated CMs.")
    fb.add_input("Mode Settings", "BOOL")
    fb.add_output("Mode FB", "BOOL")
    fb.add_in_out("Type Lookup", "BOOL")
    fb.add_temp("Pause Command", "BOOL")
    fb.add_static("End of Cycle Reached / End of Production", "BOOL")
    fb.add_constant("Reset", "BOOL")
    fb.author = "Jasper"
    fb.family = "DAF"
    fb.version = "1.0"
    fb.add_network_group("Mode", "")
    fb.add_network_group("TYPE", "")
    fb.add_network_group("Process status", "")
    mode_settings = fb.add_network("Mode Settings", "Setting holding to held", "Mode")
    mode_fb = fb.add_network("Mode FB", "Setting held to holding", "Mode")
    type_lookup = fb.add_network("Type Lookup", "Setting holding to held", "TYPE")
    pause_command = fb.add_network("Pause Command", "Setting holding to held", "Process status")
    end_of_cycle = fb.add_network(
        "End of Cycle Reached / End of Production", "Setting holding to held", "Process status", 1
    )
    move_1 = mode_settings.add_part("MOVE")
    move_2 = mode_settings.add_part("MOVE")
    move_3 = mode_settings.add_part("MOVE")
    mode_fb.add_part("GetBlockName", "1.1")
    reset_1 = end_of_cycle.add_part("RCoil")
    reset_2 = end_of_cycle.add_part("RCoil")
    pause_command.add_part("RCoil")
    doc.save_template("DAF_FB_template", True)


def make_general_db_temp():
    doc = document.Document()
    db = doc.add_db("__NAME__")
    db.add_static("Mode Settings", "BOOL")
    db.add_static("Mode FB", "BOOL")
    db.add_static("Type Lookup", "BOOL")
    db.add_static("Pause Command", "BOOL")
    db.author = "Jasper"
    db.family = "DAF"
    db.version = "1.0"
    db.memory_layout = MemoryLayout.Standard.name
    doc.save_template("DAF_DB_template", True)


def make_general_ob_temp():
    doc = document.Document()
    ob = doc.add_ob("__NAME__", ProgrammingLanguage.LAD, "Organizational block for DAF", SecondaryType.ProgramCycle)
    ob.add_temp("Mode FB", "BOOL")
    ob.add_constant("Type Lookup", "BOOL")

    ob.author = "Jasper"
    ob.family = "DAF"
    ob.version = "1.0"

    doc.save_template("DAF_OB_template", True)


if __name__ == "__main__":
    make_general_fb_temp()
    make_general_db_temp()
    make_general_ob_temp()
