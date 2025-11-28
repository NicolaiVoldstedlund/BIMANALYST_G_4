# Fire Evacuation Compliance Checking Tool

## Problem/claim:

The tool verifies the claim that a public building design provides safe and compliant fire evacuation routes, as required by the BR18 Danish Building Regulations.

It evaluates critical evacuation components such as doors, corridors, stair flights, and staircase enclosures, checking their clear widths, connectivity, and geometric validity.

The claim was found in the section 'Focus Area' in the course website. We chose this claim because of its architectural relevance. In architectural design, these requirements are critical because evacuation safety is a legal, ethical, and functional responsibility. Building layouts must support fast, unobstructed escape during fires or other emergencies. Architects, BIM modelers, and fire safety engineers must ensure that early design decisions (corridor layout, door placement, staircase configuration) do not create unsafe evacuation conditions.

## Description of the tool:

The evacuation compliance checking tool is a Python-based application designed to automatically verify whether an IFC building model meets the evacuation and escape route requirements specified in BR18. It was developed using IfcOpenShell inside Visual Studio, allowing it to extract and process both geometric and semantic information from BIM models. Instead of relying on manually entered parameters or human interpretation, the tool reads the entire 3D model directly and performs its analysis using the raw geometry.

Once an IFC model is provided, the tool begins by identifying all relevant building components, such as doors, corridors, spaces, walls, staircases, and stair flights. It calculates door widths using the actual opening geometry rather than relying solely on a declared property, ensuring higher accuracy. The tool also measures the widths of corridors and stair flights based on their bounding box geometries. For staircases, it reconstructs the enclosure by checking whether the surrounding elements are walls, as required for the compartmentation (which is part of the fire safety).

Another key capability of the tool is its validation of hallway spaces. Instead of assuming that spaces named Hallway are correct, the script checks whether they truly function as circulation corridors by verifying their connection with stairs and minimum width (to be fire-safe). The tool mainly focusses on the connectivity between spaces. Together, these checks ensure that escape routes in the model are geometrically correct, fire-safe, and logically connected.

After completing its analysis, the tool generates a structured Excel report that clearly summarizes all findings. It displays the number of passing and failing doors, staircases, and hallways, along with the IDs of the failing elements and their corresponding failure reasons.

## Instructions to run the tool:

- Download all the necessary softwares such as Visual Studio Code, Blender and Github.
- Open the Visual Studio solution containing the tool.
- Ensure required Python libraries are installed:
  - ifcopenshell
  - pandas
  - numpy
  - openpyxl
- Place the IFC model in the input folder, together with the tool
- Update the file path in the script to the path on your computer to open the model.
- Run the main script.
- Open the generated Excel report through the links printed in the console and check the results.

## What Advanced Building Design Stage (A,B,C or D) would your tool be useful?

The tool would be useful in stage B, because this is the part where all the spaces (inclusive circulation) are being defined. In this stage, fire-safety requirements can have a big influence on design choices.

The tool would also (maybe even mostly) be useful in stage C, because here is the exact geometry of the doors, stairs,… being defined. In a way, the tool is also useful for stage D, since there is a final compliance verification and clash detection. The tool can eliminate wrongly defined (or drawn) spaces and can be used as a check if the model is 'complete' (no missing objects).

## Which subjects might use it?

This tool can support several subjects and disciplines involved in architectural design, regulatory compliance, and digital modeling. It is particularly relevant in courses or professional fields that focus on:

- **Fire Safety Engineering** – to verify that evacuation routes, stair enclosures, and door widths meet regulatory safety standards.
- **Architectural Design** – especially studio projects where circulation, escape routes, and space planning are part of the evaluation.
- **BIM (Building Information Modelling)** – for understanding how IFC data structures can be analyzed and validated.

## What information is required in the model for your tool to work?

### Required IFC Entities
- IfcSpace
- IfcDoor
- IfcStairFlight
- IfcWall
- IfcOpeningElement
- IfcRelSpaceBoundary

### Required Geometry
- Valid 3D geometry
- Extractable vertices
- Bounding boxes
- Positioning that enables connectivity detection

## IDS check:

The model must contain all objects required for the fire-safety check. Each object needs to have a name and a type, such as IfcStairs, IfcDoor, IfcWall, or IfcSpace/Hallway. To use this tool effectively, these exact names must be applied so the elements can be correctly identified and checked.

These objects also need to have a geometry to measure it from.
