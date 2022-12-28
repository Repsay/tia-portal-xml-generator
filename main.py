from tia_xml_generator.enums import ProgrammingLanguage
from tia_xml_generator.elements import document

doc = document.Document()
fb = doc.add_fb("DAF_EM_template", ProgrammingLanguage.FBD, "The block is used to control EM{} and all its associated CMs.")

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
mode_fb = fb.add_network("Mode FB", "Depending on the inputs preconditions, commands, alarms, HMI and input from Safety Area (SA) Determine the current function, mode of operandi, and state.", "Mode")

type_lookup = fb.add_network("Type Lookup", "Lookup the type of the block", "TYPE")

pause_command = fb.add_network("Pause Command", "Pause command received", "Process status")
end_of_cycle = fb.add_network("End of Cycle Reached / End of Production", "No Phase Active", "Process status", 1)


move_1 = mode_settings.add_part("MOVE")
move_2 = mode_settings.add_part("MOVE")
move_3 = mode_settings.add_part("MOVE")

mode_fb.add_part("GetBlockName", "1.1")
mode_fb.add_call("Mode_EM_FB", "FB")

type_lookup.add_call("Type_Lookup_FB", "FB")

reset_1 = end_of_cycle.add_part("RCoil")
reset_2 = end_of_cycle.add_part("RCoil")

pause_command.add_part("RCoil")

doc.save_template("DAF_EM_template", True)
doc.save("test")

# doc = document.Document.load_template("DAF_EM_template")
# fb = doc.get_fb("DAF_EM_template")

# mode_settings = fb.get_network("Mode Settings")
# mode_settings.add_part("MOVE")

# mode_settings_moves = mode_settings.get_part("MOVE")

# if not mode_settings_moves is None:
#     mode_settings_move = mode_settings_moves[0]

#     wires_move = mode_settings.get_wires(mode_settings_move)

#     if not wires_move is None:
#         for wire in wires_move:
#             connections = wire.get_connections()

# mode_fb = fb.get_network("Mode FB")
# mode_fb_call = mode_fb.get_call("Mode_EM_FB")

# doc.save("test")


doc = document.Document.load_from_file("test")
fb = doc.get_fb("DAF_EM_template")

doc.save("test2")