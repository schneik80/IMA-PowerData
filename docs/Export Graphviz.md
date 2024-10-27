# Export Graphviz

[Back to Readme](../README.md)

## Description

Export an assembly to [Grapviz](https://www.graphviz.org/) as a diagram

Open an assembly. select the Export Graphviz Diagram... 
Browse to the folder where you want to save the Graphviz DOT file and click OK.
A dialog will confirm the name and location where the file was exported.

Power tools will writes out DOT file diagram with basic info needed from Graphiviz. The diagram shows the root assembly and then all components and sub-assemblies by name. Only unique (local or remote) components are show. Components will only appear once even if used multiple times.

Example Diagram:

![diagram](/docs/assets/graphviz_001.png)

You can use [online](https://dreampuf.github.io/GraphvizOnline) or [download](https://www.graphviz.org/download/) local tools and viewers. 

NOTE: If a local graphviz viewer is installed on MAC PowerTools will attempt to open the diagram after export automatically. (Windows is still TODO).

## Access

From the Design Document's **File** dropdown menu select **Export Graphviz Diagram...**.

![access](/docs/assets/graphviz_002.png)

[Back to Readme](../README.md)

IMA LLC Copyright
