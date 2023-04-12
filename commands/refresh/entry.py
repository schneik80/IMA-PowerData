import adsk.core
import os
from ...lib import fusion360utils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface


# TODO *** Specify the command identity information. ***
CMD_ID = 'PT-Refresh'
CMD_NAME = 'Refresh Active Document'
CMD_Description = 'Close and reopen the active document to get new versions from Team Hub'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

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
    #this handles the document close and reopen
    id=app.activeDocument.dataFile.id
    sF = app.data.findFileById(id)
    doc_a = app.activeDocument
    doc_a.close(False)
    app.documents.open(sF)
        
# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Destroy Event')

    global local_handlers
    local_handlers = []
