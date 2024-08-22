import adsk.core, adsk.fusion, adsk.cam, adsk.drawing
import os, traceback, json
from ...lib import fusion360utils as futil
from ... import config
from datetime import datetime

CMD_NAME = "New Documnet"
CMD_ID = "PT-new"
CMD_Description = "Create new Document"
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
app = adsk.core.Application.cast(None)
ui = adsk.core.UserInterface.cast(None)
num = 0


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
    #pallet = 
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


# Function to be called when a user clicks the corresponding button in the UI.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f"{CMD_NAME} Command Created Event")

    # Connect to the events that are needed by this command.
    futil.add_handler(
        args.command.execute, command_execute, local_handlers=local_handlers
    )
    futil.add_handler(
        args.command.inputChanged, command_input_changed, local_handlers=local_handlers
    )
    futil.add_handler(
        args.command.destroy, command_destroy, local_handlers=local_handlers
    )
    futil.add_handler(
        args.command.incomingFromHTML, browser_incoming, local_handlers=local_handlers
    )

    inputs = args.command.commandInputs

    palette = ui.palettes.add(
        "myPalette",
        "New_Document",
        "index1.html",
        True,
        True,
        True,
        400,
        800,
        True,
    )
    palette.isVisible = True
    palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight


# Create a browser input (cleanup for windows)
    browser_input_url = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "resources", "html", "index.html"
    )
    browser_input_url = browser_input_url.replace("\\", "/")

    # Create a browser input
    minimum_height = 300
    browser_input = inputs.addBrowserCommandInput(
        "browser_input", "Browser Input", browser_input_url, minimum_height
    )
    browser_input.isFullWidth = True


# This function will be called when the user clicks the OK button in the command dialog.
def command_execute(args: adsk.core.CommandEventArgs):
    futil.log(f"{CMD_NAME} Command Execute Event")


# This function will be called when the user changes anything in the command dialog.
def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    inputs = args.inputs
    futil.log(
        f"{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}"
    )

    selection_input: adsk.core.SelectionCommandInput = inputs.itemById(
        "selection_input"
    )
    browser_input: adsk.core.BrowserCommandInput = inputs.itemById("browser_input")

    action = None
    data = {}
    if changed_input.id == "selection_input":
        action = "updateSelection"
        if selection_input.selectionCount > 0:
            selected_entity = selection_input.selection(0).entity
            data = {
                "selection_name": selected_entity.name,
                "selection_type": selected_entity.objectType,
            }
        else:
            data = {
                "selection_name": "Nothing Selected",
                "selection_type": "Nothing Selected",
            }
    elif changed_input.id == "input_box":
        action = "updateMessage"
        data = {
            "message": input_box.value,
        }

    if action is not None:
        response = browser_input.sendInfoToHTML(action, json.dumps(data))


# Use this to handle events sent from javascript in your palette.
def browser_incoming(html_args: adsk.core.HTMLEventArgs):

    # Read message sent from browser input javascript function
    message_data = json.loads(html_args.data)
    message_action = html_args.action

    # Get Command Inputs
    browser_input = html_args.browserCommandInput
    inputs = browser_input.commandInputs
    incoming_box: adsk.core.TextBoxCommandInput = inputs.itemById("incoming_box")

    # Update Command UI from form value from HTML/Javascript
    if message_action == "formMessage":
        formInputValue = message_data.get("formInputValue", "textBoxValue not sent")
        timeStamp = message_data.get("timeStamp", "timeStamp not sent")

        msg = f"<b>Form Input Value</b>: {formInputValue}<br/><b>Time Stamp</b>: {timeStamp}"
        incoming_box.formattedText = msg

    # Javascript is expecting a response
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    html_args.returnData = f"OK - {currentTime}"


# This function will be called when the user completes the command.
def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f"{CMD_NAME} Command Destroy Event")
