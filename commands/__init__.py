# Here you define the commands that will be added to your add-in.

# If you want to add an additional command, duplicate one of the existing directories and import it here.
# You need to use aliases (import "entry" as "my_module") assuming you have the default module named "entry".
from .assemblystats import entry as assemblystats
from .autosave import entry as autosave
from .docinfo import entry as docinfo
from .exportbomcsv import entry as exportbomcsv
from .exportgraphviz import entry as exportgraphviz
from .exportmermaid import entry as exportmermaid
from .externalizeComps import entry as externalize
from .getandupdate import entry as getandupdate
from .history import entry as history
from .insertSTEP import entry as insertSTEP
from .refresh import entry as refresh
from .relateddata import entry as relateddata
from .tabToolbar import entry as tabToolbar

# Fusion will automatically call the start() and stop() functions.
commands = [
    assemblystats,
    autosave,
    docinfo,
    exportbomcsv,
    exportgraphviz,
    exportmermaid,
    externalize,
    getandupdate,
    history,
    refresh,
    insertSTEP,
    relateddata,
    tabToolbar,
]


# Assumes you defined a "start" function in each of your modules.
# The start function will be run when the add-in is started.
def start():
    for command in commands:
        command.start()


# Assumes you defined a "stop" function in each of your modules.
# The stop function will be run when the add-in is stopped.
def stop():
    for command in commands:
        command.stop()
