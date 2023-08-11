import adsk.core
import os
from ...lib import fusion360utils as futil
from ... import config

app = adsk.core.Application.get()
ui = app.userInterface


# TODO *** Specify the command identity information. ***
CMD_ID = 'PT-Exportmermaid'
CMD_NAME = 'Export Mermaid'
CMD_Description = 'Export active document as Mermaid mmd Diagram'