# Fire Evacuation Compliance Checking Tool

## Summary

**Title:** Checking Fire Evacuation Routes in Public Buildings

**Description:** The script extracts the relevant fire evacuation elements from a building model in IFC format. It evaluates the requirements listed in BR18 for the width, compartmentation and whether a corridor is a 'fire-proof hallway' or not.

## Introduction

This tutorial introduces a Python-based tool for checking fire evacuation routes in public buildings using IFC models. The main purpose is to show how a BIM model can be analyzed geometrically when some explicit dimensions are not provided. The tool focuses on extracting geometry from IFC elements to calculate widths of doors, corridors, and stair flights, and on connectivity analysis, verifying how hallways connect to other hallways and to staircases. By combining geometric extraction with connectivity checks, the tutorial demonstrates how to assess fire safety and evacuation compliance even in incomplete or inconsistent BIM models, providing a practical workflow for designers and BIM practitioners.

## Role: OpenBIM Analyst

This tutorial corresponds to **Analyst Level 3**, as it involves developing a standalone Python tool using IfcOpenShell to check fire evacuation in IFC models. The script extracts geometry, analyzes connectivity between hallways and stairs, and verifies widths when dimensions are missing. It had to handle real-world model issues—naming inconsistencies, missing geometry, and modelling errors—by implementing custom extraction, heuristics, and fallback strategies, making it robust across imperfect IFC models. However, minimal conventions are required (e.g., hallways named "Hallway"), but the tool works reliably even with incomplete data.

## Problem/claim:

The tool verifies the claim that a public building design provides safe and compliant fire evacuation routes, as required by the BR18 Danish Building Regulations.

It evaluates critical evacuation components such as doors, corridors, stair flights, and staircase enclosures, checking their clear widths, connectivity, and geometric validity.

The claim was found in the section 'Focus Area' in the course website. We chose this claim because of its architectural relevance. In architectural design, these requirements are critical because evacuation safety is a legal, ethical, and functional responsibility. Building layouts must support fast, unobstructed escape during fires or other emergencies. Architects, BIM modelers, and fire safety engineers must ensure that early design decisions (corridor layout, door placement, staircase configuration) do not create unsafe evacuation conditions.

## Description of the tool:

The evacuation compliance checking tool is a Python-based application designed to automatically verify whether an IFC building model meets the evacuation and escape route requirements specified in BR18. It was developed using IfcOpenShell inside Visual Studio, allowing it to extract and process both geometric and semantic information from BIM models. Instead of relying on manually entered parameters or human interpretation, the tool reads the entire 3D model directly and performs its analysis using the raw geometry.

Once an IFC model is provided, the tool begins by identifying all relevant building components, such as doors, corridors, spaces, walls, staircases, and stair flights. It calculates door widths using the actual opening geometry rather than relying solely on a declared property, ensuring higher accuracy. The tool also measures the widths of corridors and stair flights based on their bounding box geometries. For staircases, it reconstructs the enclosure by checking whether the surrounding elements are walls, as required for the compartmentation (which is part of the fire safety).

Another key capability of the tool is its validation of hallway spaces. Instead of assuming that spaces named Hallway are correct, the script checks whether they truly function as circulation corridors by verifying their connection with stairs and minimum width (to be fire-safe). The tool mainly focusses on the connectivity between spaces. Together, these checks ensure that escape routes in the model are geometrically correct, fire-safe, and logically connected.

After completing its analysis, the tool generates a structured Excel report that clearly summarizes all findings. It displays the number of passing and failing doors, staircases, and hallways, along with the IDs of the failing elements and their corresponding failure reasons.

## Procedural Overview of Tutorial
The tutorial is divided into 10 sections:

1. **Imports and Configuration** - Required libraries and BR18 threshold constants
2. **Utility Functions - Caching and Unit Conversion** - Performance optimization and unit handling
3. **Geometry Extraction Functions** - Extract vertices, dimensions, and centroids from IFC elements
4. **Property Extraction Functions** - Retrieve element properties and attributes
5. **Space Connectivity and Linkage Analysis** - Build relationships between spaces via doors
6. **Compliance Analysis Functions - Doors, Stairs, Corridors** - Check BR18 requirements
7. **Staircase Grouping and Enclosure Analysis** - Analyze stair compartmentation
8. **Bounding Box and Geometric Helper Functions** - Spatial intersection and proximity checks
9. **Stair Flight Enclosure & Geometry Helpers** - 4-wall enclosure verification
10. **Main Analysis Function** - Orchestrates all checks and generates Excel report

At the end of the tutorial, you'll find a brief explanation of the results (Excel file) and guidance on how to interpret them using the IFC model.

## Focus Area: Architecture

### Goal of the Tutorial and its BIM Use

The BIM relevance of this tutorial lies in teaching how to extract and analyze data from IFC models. The tutorial explains each part of the Python code, showing how to work with BIM geometry, compute dimensions when they are not explicitly provided, and verify connectivity between hallways and staircases for fire safety. By guiding students through the process of accessing IFC properties, handling imperfect models (because for some objects the dimensions are not given), and performing spatial analysis, it demonstrates practical BIM skills that can be applied in real-world projects. The tutorial helps learners understand how to leverage BIM not just as a design tool, but as a data-rich environment for analysis, validation, and decision-making.

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

## Conclusions

Throughout this project, we encountered several challenges that influenced both our workflow and the development of our tool. One of the main difficulties was related to the IFC model itself. Initially, we wanted to determine whether a space should be classified as a hallway by checking if it was connected to multiple rooms (like in the BPMN flowchart). However, this approach turned out to be impossible because the IFC model did not correctly represent the spatial connections. For example, a single door, normally acting as a link between two spaces, was assigned to only one room, illustrating why the overall connection data was unreliable.

If we look at the failing objects from the results in the Excel file and analyse them in the model, we see that for example most of the hallways fail probably because they are misnamed, misplaced or they are maybe only connected to an elevator instead of the stairs. In this way, the tutorial learns how to interpret models and that you always have to be critic about the model to understand the output.

We also faced limitations within our own code. Our tool relies heavily on IFC element names, which means that models using different naming conventions are difficult to check. To make such models compatible, their element names would have to be adjusted to match the ones used in our code.

Despite these issues, we learned a great deal. Even though the model contained errors, we tried to work around them using creative solutions. For instance, some elements had no dimensions defined, so we programmed "bounding boxes" around them to calculate their dimensions ourselves. This project truly pushed us to think outside the box, both literally and figuratively, and taught us how to adapt our approach when working with imperfect data.


