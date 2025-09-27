import ifcopenshell
import ifcopenshell.geom
import collections

def get_area_from_properties(element):
    # Try common property names
    for prop_name in ["Area", "NetSideArea", "NetArea"]:
        if hasattr(element, prop_name):
            value = getattr(element, prop_name)
            if isinstance(value, (int, float)):
                return value
    # Try property sets
    if hasattr(element, "IsDefinedBy"):
        for rel in element.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                props = rel.RelatingPropertyDefinition
                if props.is_a("IfcPropertySet"):
                    for p in props.HasProperties:
                        if p.Name in ["Area", "NetSideArea", "NetArea"]:
                            if hasattr(p, "NominalValue"):
                                return float(p.NominalValue.wrappedValue)
    return 0

def is_external_wall(wall):
    excluded_names = [
        "ifcWall/ Basic Wall: Exterior - 515mm Woood/ Insulation- fa.004",
        "ifcWall/ Basic Wall: Exterior -50 mm Wood/ Wood - facade red.001",
        "ifcWall/Basic Wall: Exterior- 50 mm Wood/ Wood - facade:1523234",
        "ifcWall/ Basic Wall: Exterior- 515mm Woood/ Insulation - fa.003",
        "ifcWall/ Basic Wall: Exterior- 515mm Woood/ Insulation - fa.005",
        "ifcWall/ Basic Wall: Exterior -50 mm Wood/ Wood - facade 15158984",
        "IfcWall/ Basic Wall: Exterior- 50mm Wood/ Wood- facade 1494517"
    ]
    if hasattr(wall, "Name") and wall.Name in excluded_names:
        return False
    # Check property sets for IsExternal
    if hasattr(wall, "IsDefinedBy"):
        for rel in wall.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                props = rel.RelatingPropertyDefinition
                if props.is_a("IfcPropertySet"):
                    for p in props.HasProperties:
                        if p.Name == "IsExternal":
                            if hasattr(p, "NominalValue"):
                                if bool(p.NominalValue.wrappedValue):
                                    return True
    # Check wall name for 'Exterior'
    if hasattr(wall, "Name") and wall.Name:
        if "exterior" in wall.Name.lower():
            return True
    return False

def get_bounding_box(element):
    try:
        settings = ifcopenshell.geom.settings()
        shape = ifcopenshell.geom.create_shape(settings, element)
        bbox = shape.geometry.bbox
        return bbox # (min_x, min_y, min_z, max_x, max_y, max_z)
    except Exception:
        return None

def bboxes_overlap(b1, b2):
    return (
        b1[0] < b2[3] and b1[3] > b2[0] and # x overlap
        b1[1] < b2[4] and b1[4] > b2[1] and # y overlap
        b1[2] < b2[5] and b1[5] > b2[2]     # z overlap
    )

def checkRule(model):
    external_walls = [wall for wall in model.by_type("IfcWall") if is_external_wall(wall)]
    unique_walls = []
    wall_bboxes = []
    for wall in external_walls:
        bbox = get_bounding_box(wall)
        if bbox is None:
            unique_walls.append(wall)
            continue
        overlap = False
        for other_bbox in wall_bboxes:
            if bboxes_overlap(bbox, other_bbox):
                overlap = True
                break
        if not overlap:
            unique_walls.append(wall)
            wall_bboxes.append(bbox)

    facade_area = sum(get_area_from_properties(wall) for wall in unique_walls)
    window_area = sum(get_area_from_properties(window) for window in model.by_type("IfcWindow"))

    if facade_area > 0:
        transparency = (window_area / facade_area) * 100
    else:
        transparency = 0

    return {
        "Facade surface area": facade_area,
        "Window surface area": window_area,
        "Average facade transparency (%)": round(transparency, 2)
    }