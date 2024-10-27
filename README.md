# Power Tools for Fusion v0.5

Make working as a team, cloud data, and with assemblies more productive.

## Configuration

There are several json files that need to be configured. Documentation on how to configure is TODO.

## Data Workflow

**[Create Related Data](./docs/Related%20Data.md)**

Essential for Teams working in multiple disciplines allowing users to create  related documents (as an Assembly) to contain different discipline work, like CAM or Simulation. The Assembly document is copied from a cloud project/folder allowing for the new documents to have already saved information to automate workflows.

**[New Document](./docs/New%20Document.md)**

Adds a QAT (Quick Access Toolbar) command to open a pallet to create new documents. Documents are auto-named and saved to the active project folder in Team.

---

## Manage Document References

**[Document References](./docs/Document%20References.md)**

Displays the active documents relationships. Four types of relationships are supported:

- Parents - Other documents that references the active document. These would be incoming relationships.
- Children - Documents the active Document references. These would be outgoing relationships
- Drawings - Drawings of the active Document.
- Related Data - Documents created with the IMA Power Tools related data command. These are separated from other standard Fusion relationships.

**[Reference Manager](./docs/Reference%20Manager.md)**

Show all references in the active document and their status. Provides utilities to work with references.

- Update all references or individually.
- Allow the selection of versions per reference.
- Open a reference in a new tab.

**[Get and Update](./docs/Get%20and%20Update.md)**

Typical x-ref assemblies will use assembly contexts to create associativity across parts. When new versions of x-refs are available one must load the new versions and then manually update the out of date contexts. Data Power Tools adds a QAT command to automatically get all latests and then update contexts.

**[Data Refresh](./docs/Data%20Refresh.md)**

When working in a team it can be necessary to reload the active assembly to load new versions created by other team members. Int he file menu the Refresh command will automatically close, get new versions and then reload the active document, saving you time and nuisance of doing this manually

---

## Information tools

**[Assembly Statistics](./docs/Assembly%20Statistics.md)**

Provide assembly information on the active document. Reports on components, references and joints.

**[Document Information](./docs/Document%20Information.md)**

Provide Cloud Data information on the active document. Reports on Hub, Project and Folder location including Fusion Manufacturing Cloud Data mode unique identifiers.

**[Document History](./docs/Document%20History.md)**

Show the history of the active document.

---

## UI Tweaks

**[Toggle Data Pane](./docs/Toggle%20Data%20Pane.md)**

Toggling the data pane is buried three level menu or a keyboard shortcut. This adds a button to the navbar to make toggling easier.


**[Recovery Save](./docs/Recovery%20Save.md)**

This creates an entry in the file menu to manually save a local recovery save.

**[Insert STEP](./docs/Insert%20Step.md)**

Browse the local device and insert a STEP file into the active document.

----

## Export Document information

**[Export BOM](./docs/Export%20BOM.md)**

Export the active document's component information as a CSV file.

**[Export Graphviz](./docs/Export%20Graphviz.md)**

Export the active document's component relationships as a Graphviz DOT file.

**[Export Mermaid](./docs/Export%20Mermaid.md)**

Export the active document's component relationships as a mermaid flowchart md file.

---

## Tools to automate special tasks

**[Make Project Default Folders](./docs/Default%20Folders.md)**

Creates three folders in the active project if they do not already exist. Folders are:

- Obit - Folder to store documents not to be used. These may include obit lifecycle documents or documents that can not be deleted due to historical references.
- Archive - Folder for documents that are not active but should not be deleted.
- Quarantine - Folder for imported documents that need to be cleaned up prior to general use.
  

**[Install a dedicated Assembly Tab](.docs/Install%20Assembly%20Tab.md)**

Installs a new Assembly tab in the Fusion design toolbar. Restructures toolbar for better design workflows.  
