# Install Assembly Tab to Design Toolbar

[Back to Readme](../README.md)

## Description 

- Introduce a dedicate Assembly Experience
  - Add **Assembly** tab to Fusion design documents
  - New **Assemble** panel in the Assembly tab
  - Moves all Assembly tools to an Assemble panel.
  - New **Motion** panel in the Assembly tab
  - Move motion tools to Motion panel
  - Removes **Assemble** panel from other domain specific ( i.e. Sheetmetal, Plastic, others ) Modeling tabs.
    > NOTE: To remove Assemble from the Mesh tab requires an additional xml document to be modified.
  - Moves **As Built Joint** and **Joint Origin** into an **Advanced** sub menu
  - Removes **Align** from all menus except the Solid tab Modify Panel
  - Joint Origin command is now also in the Construct panel menu across all tabs
- Adds a **PCB** Tab for creation for 3D PCB boards in context of design
- Reorder the **Manage** tab
  - Manage Tab is now before the Utilities tab
  - BOM panel moved to the start of the manage tab tools
- Remove Automated modeling panel
  - **Automated modeling** now appears in Solid Tab's Create panel menu

Assembly Tab Preview:

![Assembly  tab preview](/docs/assets/asm-tab.png)

NOTE that when you install the assembly tab a backup is made in the fusion application folder.

## Access

From the Fusion **File** dropdown menu **Install Assembly Tab** and follow prompts.

## Uninstall

To uninstall, restore the original file you archived and restart Fusion 360.

## Special instructions for Mesh tab

(These steps are completely optional and unless you frequently use the mesh tools can be skipped with)

To remove Assemble tools from Mesh Tab toolbar:

**!!! Backup your original TabToolbar.xml before modifying !!!**

On **Mac OS**, edit the existing file here:

> /Users/ <Your User Name> /Library/Application Support/Autodesk/webdeploy/production/ <Current deployment GUID> /Autodesk Fusion 360.app/Contents/Libraries/Applications/Paramesh//UI/ParaMeshUI/Resources/Toolbar/TabToolbars.xml

On **Windows**, edit the existing file here:

> \Users\ <Your User Name> \AppData\Local\Autodesk\webdeploy\production\ <Current deployment GUID> \ParaMesh\UI\ParaMeshUI\Resources\Toolbar\TabToolbars.xml

From `Tab Id="ParaMeshOuterTab"`  

Remove `"AssemblePanel;"`  

So the line now reads: `"Panels="ParaMeshCreatePanel;ParaMeshPreparePanel;ParaMeshModifyPanel;ConfigurePanel;ConstructionPanel;InspectPanel;InsertPanel;ParaMeshSelectPanel;ParaMeshExportPanel;SnapshotPanel"`

From `Tab Id="ParaMeshBaseFeatureTab"`  

Remove `"AssemblePanel;"`  

So the line now reads: `Panels="ParaMeshCreateBaseFeature;ParaMeshPreparePanel;ParaMeshModifyPanel;ConstructionPanel;InspectPanel;ParaMeshSelectPanel;ParaMeshExportPanel;ParaMeshBaseFeatureStopPanel"`

[Back to Readme](../README.md)

IMA LLC Copyright
