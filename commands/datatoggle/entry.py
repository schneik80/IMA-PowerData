import adsk.core, adsk.fusion
import os, traceback
from ...lib import fusion360utils as futil
from ... import config

app = adsk.core.Application.get()
ui = app.userInterface

CMD_NAME = "Toggle Data"
CMD_ID = "PT-toggledata"
CMD_Description = "Hide or show the data pane"
IS_PROMOTED = False

# Global variables by referencing values from /config.py
TAB_ID = config.tools_tab_id
TAB_NAME = config.my_tab_name

PANEL_ID = config.my_panel_id
PANEL_NAME = config.my_panel_name
PANEL_AFTER = config.my_panel_after


# Declare constants
_navBarBtnID = "NavBarBtn"
_navBarBtnName = "NavBarBtn"
_toolbar = "NavToolbar"

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "")

# Holds references to event handlers
local_handlers = []


# Executed when add-in is run.
def start():
    # ******************************** Create Command Definition ********************************
    cmd_def = ui.commandDefinitions.itemById(_navBarBtnID)
    if not navBarBtnCmdDef:
        navBarBtnCmdDef = _ui.commandDefinitions.addButtonDefinition(
            _navBarBtnID, CMD_NAME, CMD_Description, ICON_FOLDER
        )

    # Add command created handler. The function passed here will be executed when the command is executed.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******************************** Create Command Control ********************************

    navToolbar = ui.toolbars.itemById(_toolbar)
    navToolbarControls = navToolbar.controls
    control = navToolbarControls.addCommand(cmd_def, "", False)

    # ****************
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


# Function to be called when a user clicks the corresponding button in the UI.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f"{CMD_NAME} Command Started Event")
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # Check a Design document is active.
        if not design:
            ui.messageBox("No active Fusion design", "No Design")
            return

        # Set styles of file dialog.
        fileDlg = ui.createFileDialog()
        fileDlg.isMultiSelectEnabled = False
        fileDlg.title = "Fusion Insert STEP"
        fileDlg.filter = "STEP Files(*.stp;*.STP;*.step;*.STEP);;All files (*.*)"

        # Show file open dialog
        dlgResult = fileDlg.showOpen()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            filename = fileDlg.filename
        else:
            return

        filename = '"' + filename + '"'
        command = f"Fusion.ImportComponent {filename}"
        app.executeTextCommand(command)

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))

    futil.log(f"{CMD_NAME} Command Completed Event")
