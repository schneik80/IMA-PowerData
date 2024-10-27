import adsk.core, adsk.fusion
import html, traceback
from ...lib import fusion360utils as futil
from ... import config

app = adsk.core.Application.get()
ui = app.userInterface

CMD_NAME = "Document Refrences"
CMD_ID = "PT-docrefs"
CMD_Description = "List Active Document References"


# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


# Executed when add-in is run.
def start():
    # ******************************** Create Command Definition ********************************
    cmd_def = ui.commandDefinitions.addButtonDefinition(
        CMD_ID, CMD_NAME, CMD_Description
    )

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # **************** Add a button into the UI so the user can run the command. ****************
    # Get the target workspace the button will be created in.

    qat = ui.toolbars.itemById("QAT")

    # Get the drop-down that contains the file related commands.
    fileDropDown = qat.controls.itemById("FileSubMenuCommand")

    # Add a new button before the 3D Print control.
    control = fileDropDown.controls.addCommand(cmd_def, "UploadCommand", True)


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    qat = ui.toolbars.itemById("QAT")
    fileDropDown = qat.controls.itemById("FileSubMenuCommand")
    command_control = fileDropDown.controls.itemById(CMD_ID)
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
    futil.log(f"{CMD_NAME} Command Created Event")

    # Connect to the events that are needed by this command.
    futil.add_handler(
        args.command.execute, command_execute, local_handlers=local_handlers
    )
    futil.add_handler(
        args.command.destroy, command_destroy, local_handlers=local_handlers
    )


def command_execute(args: adsk.core.CommandCreatedEventArgs):
    # this handles the document close and reopen
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct

        if not design:
            ui.messageBox('No active Fusion design')
            return

        activeDoc = app.activeDocument
        parentDataFiles = activeDoc.designDataFile.parentReferences
        childDataFiles = activeDoc.designDataFile.childReferences
        docParents = []
        docChildren = []
        docDrawings = []
        docRelated = []
        subString = " <-- "

        # Process parent and related data files
        if parentDataFiles:
            for file in parentDataFiles:

                if subString in file.name:
                    target_list = docRelated

                elif file.fileExtension == 'f2d':
                    target_list = docDrawings

                else:
                    target_list = docParents

                target_list.append({
                        "name": file.name,
                        "id": file.id,
                        "url": file.fusionWebURL
                    })

        # Process child data files
        if childDataFiles:
            docChildren = [{
                "name": file.name,
                "id": file.id,
                "url": file.fusionWebURL
            } for file in childDataFiles]

        # Links String to report references
        links = f'<h1>Source document: {html.escape(activeDoc.name)}</h1>'
        links += f'<h3>Parents ({len(docParents)}):</h3>'

        if docParents:
            for item in docParents:
                links += f'<a href="{item["url"]}">{html.escape(item["name"])}</a><br>'
        else:
            links += f'No Parent Relationships'

        links += f'<h3>Children ({len(docChildren)}):</h3>'

        if docChildren:
            for item in docChildren:
                links += f'<a href="{item["url"]}">{html.escape(item["name"])}</a><br>'
        else:
            links += f'No Child Relationships<br>'


        links += f'<h3>Drawings ({len(docDrawings)}):</h3>'

        if docDrawings:
            for item in docDrawings:
                links += f'<a href="{item["url"]}">{html.escape(item["name"])}</a><br>'
        else:
            links += f'No Drawings<br>'


        links += f'<h3>Related Data ({len(docRelated)}):</h3>'

        if docRelated:
            for item in docRelated:
                links += f'<a href="{item["url"]}">{html.escape(item["name"])}</a><br>'
        else:
            links += f'No Related Data Relationships'
        
        relationshipCount = len(docParents) + len(docChildren) + len(docDrawings) + len(docRelated)
        relationsTitle = f"References ({relationshipCount})"

        ui.messageBox(links, relationsTitle)
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# This function will be called when the user completes the command.
def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f"{CMD_NAME} Command Destroy Event")
