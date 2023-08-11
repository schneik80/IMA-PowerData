# Author - Kevin S
# Description - Export an assembly as a graphviz graph
# Performs a recursive traversal of an entire assembly structure.

import adsk.core
import os
import traceback
from ...lib import fusion360utils as futil
from ... import config


app = adsk.core.Application.get()
ui = app.userInterface

# TODO *** Specify the command identity information. ***
CMD_ID = 'PT-Exportgraphviz'
CMD_NAME = 'Graphiz Export'
CMD_Description = 'Export Active Document as Graphviz dot diagram'

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description )

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.

    qat = ui.toolbars.itemById('QAT')

    # Get the drop-down that contains the file related commands.
    fileDropDown = qat.controls.itemById('FileSubMenuCommand')

    # Add a new button before the 3D Print control.
    control = fileDropDown.controls.addCommand(cmd_def, 'UploadCommand', True)


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    qat = ui.toolbars.itemById('QAT')
    fileDropDown = qat.controls.itemById('FileSubMenuCommand')
    command_control = fileDropDown.commandControlByIdForPanel(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()

# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
 
    ui = None
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox("Active document is not a Fusion design document", "Incorrect Document Type")
            return

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create the title for the output.
        parentOcc = design.parentDocument.name

        resultString = (
            'digraph "' + parentOcc + '" {' + "\n"
        )  # Change layout engine here
        resultString += 'layout="dot";' + "\n"
        resultString += "node[width=.75,height=.5,fontsize=9]" + "\n"
        resultString += "nodesep=.2" + "\n"
        resultString += "ranksep=3" + "\n"
        resultString += "concentrate=false" + "\n"
        resultString += 'mode="ipsep"' + "\n"
        resultString += "diredgeconstraints=true" + "\n"
        resultString += 'overlap="false"' + "\n"

        # Call the recursive function to traverse the assembly and build the output string.
        resultString = traverseAssembly(
            parentOcc, rootComp.occurrences.asList, 1, resultString
        )

        resultString += "}"

        # Set styles of file dialog.
        folderDlg = ui.createFolderDialog()
        folderDlg.title = "Choose Folder to save Graphviz Graph"

        # Show file save dialog
        dlgResult = folderDlg.showDialog()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            filepath = os.path.join(folderDlg.folder, parentOcc + ".dot")
            # Write the results to the file
            with open(filepath, "w") as f:
                f.write(resultString)
            ui.messageBox("Graph dot file saved at: " + filepath)

        else:
            return

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
        
# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Destroy Event')

    global local_handlers
    local_handlers = []

def traverseAssembly(parent, occurrences, currentLevel, inputString):
    for i in range(0, occurrences.count):
        occ = occurrences.item(i)

        foo1 = occ.name
        foo2 = foo1.rsplit(" ", 1)[0]  # trim version

        parent1 = parent.rsplit(" ", 1)[0]  # trim version

        foo = '"' + parent1 + '"->"' + foo2 + '"' + " ;" + "\n"

        inputString += foo

        if occ.childOccurrences:
            inputString = traverseAssembly(
                occ.name, occ.childOccurrences, currentLevel + 1, inputString
            )
    return inputString