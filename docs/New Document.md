# New Document

[Back to Readme](../README.md)

## Description

WARNING - Advanced Configuration required

Fusion has limited tools to control new document creation. The New Document powertool adds a pallet to allow more customization to creating new documents. This tool currently requires advanced configuration and customizations. You will need to edit multiple documents for this command to work correctly.

New Document Dialog:

![dialog](/docs/assets/new_001.png)

Fusion Application with new Dialog:
![application](/docs/assets/new_003.png)

With this tool, you can easily create new Inch or metric documents as well as other supported Fusion Documents. Complex and completely custom new document UI is possible. This can include start parts where  pre-existing saved data has been added.

When a new document is selected from the pallet, the source document is copied to the active project and folder. It is given a new name with a date and time stamp to ensure uniqueness. You can then use the new document to begin to design.

### To customize

Two steps are required to use this power tool.

1. Configure your hub ID
2. Create your own new documents and modify HTML

#### 1. Hub ID

You will need to modify and rename the json document located in the PowerTools add-in directory:

>./Sample Hub.json

Make sure you are in the Hub which you want to configure your data.

Turn on the Fusion Text command window.

Click the New Document powertool command in the QAT (Quick Access Toolbar).

In the Fusion Text Command window an error will report an expected Hub ID is missing. It will also display the current Hub ID.

```active hub is a.YRdvewrTSFV3M6Y2Gybb3A.```

Copy this value and paste it into the Sample Hub.json.

```{"HUB_ID":"Enter your own HUB ID HERE"}``` Should then read ```{"HUB_ID":"a.YRdvewrTSFV3M6Y2Gybb3A"}``` keeping in mind that your Hub ID will be different. **Use your HUB id not the values shown here.**

Rename Sample Hub.json to hub.json. **Case matters.**

Reload the PowerTool add-in.

#### 2. Modify HTML

Create a project and folder to contain the new documents you want to have quick access to.

Using the [Document Information](/docs/Document%20Information.md) command collect the document IDs for each.

Modify the HTML document located in the PowerTools add-in directory:

>./commands\new\resources\index.html

Adjust the table however needed. **Most important** is to adjust the "onclick" urn information in quotes within the html to match the corresponding document IDs.

onclick="sendInfoToFusion('<< insert your urn here >>')

See example html code here:

```<td>
    <div class="container">
        <img src="html/comp.png" alt="" class="image" width="96px">
        <div class="overlay">
            <div class="text"><div class="tooltip"><img src="html/open.png" onclick="sendInfoToFusion('urn:adsk.wipprod:dm.lineagefevwevf-j6C3-H')" alt="open" hspace="5" ><span class="tooltiptext">New mm Component</span></a></div></div>
        </div>
    </div>    
</td>
```

As the pallet is HTML you can create as simple or complex a UI as you like. The onlcick URN value is passed to Fusion and used to create the new document.

NOTE. You may be able to try this command without customization but it will incorrectly create new documents

## Access

Access to the **New Document** command is from the **QAT** (Quick Access Toolbar).

![access](/docs/assets/new_002.png)

[Back to Readme](../README.md)

IMA LLC Copyright
