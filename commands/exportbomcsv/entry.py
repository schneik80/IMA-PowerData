import adsk.core, adsk.fusion
import os, traceback
from ...lib import fusion360utils as futil
from ... import config

app = adsk.core.Application.get()
ui = app.userInterface

showversion = True  # show versions in xref component names, default is on
showsubs = False  # show the subassemblies in list, for flat BOM default is off. Children are still displayed this only affects the sub itself
docname = ""  # a default name

CMD_NAME = "Export BOM as CSV"
CMD_ID = "PT-exportbom"
CMD_Description = "Export active assembly structure and quantities as a CSV file"
IS_PROMOTED = False

# Global variables by referencing values from /config.py
WORKSPACE_ID = config.design_workspace
TAB_ID = config.tools_tab_id
TAB_NAME = config.my_tab_name

PANEL_ID = config.my_panel_id
PANEL_NAME = config.my_panel_name
PANEL_AFTER = config.my_panel_after

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "")

# Holds references to event handlers
local_handlers = []


# Executed when add-in is run.
def start():
    # ******************************** Create Command Definition ********************************
    cmd_def = ui.commandDefinitions.addButtonDefinition(
        CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER
    )

    # Add command created handler. The function passed here will be executed when the command is executed.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******************************** Create Command Control ********************************
    # Get target workspace for the command.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get target toolbar tab for the command and create the tab if necessary.
    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    if toolbar_tab is None:
        toolbar_tab = workspace.toolbarTabs.add(TAB_ID, TAB_NAME)

    # Get target panel for the command and and create the panel if necessary.
    panel = toolbar_tab.toolbarPanels.itemById(PANEL_ID)
    if panel is None:
        panel = toolbar_tab.toolbarPanels.add(PANEL_ID, PANEL_NAME, PANEL_AFTER, False)

    # Create the command control, i.e. a button in the UI.
    control = panel.controls.addCommand(cmd_def)

    # Now you can set various options on the control such as promoting it to always be shown.
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()

    # Delete the panel if it is empty
    if panel.controls.count == 0:
        panel.deleteMe()

    # Delete the tab if it is empty
    if toolbar_tab.toolbarPanels.count == 0:
        toolbar_tab.deleteMe()


# # Function to be called when a user clicks the corresponding button in the UI.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f"{CMD_NAME} Command Created Event")

    # Connect to the events that are needed by this command.
    futil.add_handler(
        args.command.execute, command_execute, local_handlers=local_handlers
    )
    futil.add_handler(
        args.command.destroy, command_destroy, local_handlers=local_handlers
    )


def command_execute(args: adsk.core.CommandCreatedEventArgs):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        global docname
        global showversion
        global showsubs

        command = args.firingEvent.sender
        inputs = command.commandInputs

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox("A Design Must be Active.", "BOM Export")
            return

        # Get all occurrences in the rootComp component of the active design
        rootComp = design.rootComponent
        occs = rootComp.allOccurrences

        for input in inputs:
            if input.id == "docname_":
                docname = input.value
            elif input.id == "showversion_":
                showversion = input.value
            elif input.id == "showsubs_":
                showsubs = input.value

        # Gather information about each unique component
        bom = []
        for occ in occs:
            comp = occ.component
            refocc = occ.isReferencedComponent
            occtype = occ.childOccurrences.count
            # print (occtype)
            jj = 0
            for bomI in bom:
                if bomI["component"] == comp:
                    # Increment the instance count of the existing row.
                    bomI["instances"] += 1
                    break
                jj += 1

            if jj == len(bom):
                # Modify the name if versions are OFF and an occurrence is an xref
                if showversion == False and refocc == True:
                    longname = comp.name
                    shortname = " v".join(longname.split(" v")[:-1])
                else:
                    shortname = comp.name

                mat = ""
                bodies = comp.bRepBodies
                for bodyK in bodies:
                    if bodyK.isSolid:
                        mat += bodyK.material.name

                # Add this component to the BOM
                bom.append(
                    {
                        "component": comp,
                        "name": shortname,
                        "pn": comp.partNumber,
                        "material": mat,
                        "instances": 1,
                        "sub": occtype,
                    }
                )

        # collect BOM data
        parentOcc = design.parentDocument.name
        resultString = parentOcc + " BOM\n"
        resultString += "Display Name," + "Part Number," + "Material," + "Count\n"
        resultString += traverseAssembly(bom)

        # Display the BOM in the console
        print(resultString)

        # Set styles of file dialog.
        folderDlg = ui.createFolderDialog()
        folderDlg.title = "Choose Folder to save BOM CSV"

        # Show file save dialog
        dlgResult = folderDlg.showDialog()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            filepath = os.path.join(folderDlg.folder, parentOcc + ".csv")
            # Write the results to the file
            with open(filepath, "w") as f:
                f.write(resultString)
            ui.messageBox("BOM saved at: " + filepath, parentOcc, 0, 2)
            futil.log(f"BOM Saved at {filepath}")
        else:
            return

    except:
        if ui:
            ui.messageBox(
                ("command executed failed: {}").format(traceback.format_exc())
            )


# This function will be called when the user completes the command.
def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f"{CMD_NAME} Command Destroy Event")


# walk thru the assembly
def traverseAssembly(bom):
    mStr = ""
    if showsubs == False:
        for item in bom:
            if item["sub"] < 1:
                mStr += (
                    '"'
                    + item["name"]
                    + '","'
                    + str(item["pn"])
                    + '","'
                    + str(item["material"])
                    + '",'
                    + str(item["instances"])
                    + ",EA"
                    + "\n"
                )
        return mStr
    if showsubs == True:
        for item in bom:
            mStr += (
                '"'
                + item["name"]
                + '","'
                + str(item["pn"])
                + '","'
                + str(item["material"])
                + '",'
                + str(item["instances"])
                + ",EA"
                + "\n"
            )
        return mStr
