from tia_xml_generator.enums import MemoryLayout, ProgrammingLanguage, SecondaryType
from tia_xml_generator.elements import document


def make_general_fb_temp():
    doc = document.Document()
    fb = doc.add_fb(
        "__NAME__", ProgrammingLanguage.FBD, "This block is used to control EM__EM__ and all its associated CMs."
    )
    fb.add_network_group("Mode", "In this group the mode of the EM is controlled.")
    fb.add_network_group("Safety", "In this group the safety of the EM is controlled.")
    fb.add_network_group("Type", "In this group the type of the EM is controlled.")
    fb.add_network_group("CM", "In this group the CMs are controlled.")
    fb.add_network_group("Process Status", "In this group the process status of the EM is controlled.")
    fb.add_network_group("Phases", "In this group the phases of the EM are controlled.")
    fb.add_network_group("HMI", "In this group the HMI is controlled.")
    fb.add_network_group("Other", "In this group other functions are controlled.")

    mode_settings_network = fb.add_network("Mode Settings", "Setting pausing to holding and holding to held ", "Mode")
    mode_fb_network = fb.add_network(
        "Call Mode FB",
        "Depending on the inputs preconditions, commands, alarms, HMI and inputs from the Safety Area (SA). Determine the current function, mode of operandi and state of the EM.",
        "Mode",
    )
    blocked_starved_network = fb.add_network(
        "Blocked and Starved Conditions", "Blocked and Starved Conditions\nBlocked -> \nStarved -> ", "Mode"
    )
    mode_master_network = fb.add_network("EM Mode to Master", "Call the EM Mode to Master FB.", "Mode")

    mode_settings_network.add_part("MOVE")
    mode_settings_network.add_part("MOVE")

    mode_fb_network.add_part("GetBlockName")
    mode_fb_network.add_call("Mode_EM_FB", "FB", "FB", "Mode", "Variable")

    mode_master_network.add_call(
        "EMModeToMaster",
        "FB",
        "FB",
        "EMtoMaster",
        "Variable",
    )

    type_lookup_network = fb.add_network("Call Type Lookup __NAME__", "Call the Type Lookup __NAME__", "Type")
    type_lookup_network.add_call("Type_Lookup_FB", "FB")

    end_cycle_network = fb.add_network("End of Cycle (EOC) / End of Production (EOP)", "EOC / EOP", "Process Status")
    pause_command_network = fb.add_network("Pause Command", "Pause Command", "Process Status")


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
