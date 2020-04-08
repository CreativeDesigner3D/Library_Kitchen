import bpy
import os
from .bp_lib.xml import XML

def get_kitchen_scene_props():
    return bpy.context.scene.kitchen

def get_cabinet_bp(obj):
    if "IS_CABINET_BP" in obj:
        return obj
    elif obj.parent:
        return get_cabinet_bp(obj.parent)

def flip_normals(assembly):
    for child in assembly.obj_bp.children:
        if child.type == 'MESH':
            for polygon in child.data.polygons:
                polygon.flip()
            child.data.update()

def get_material_path():
    return os.path.join(os.path.dirname(__file__),'assets','Materials') 

def get_material(category,material_name):
    if material_name in bpy.data.materials:
        return bpy.data.materials[material_name]

    material_path = os.path.join(get_material_path(),category,material_name + ".blend")

    print('PATH',material_path)

    if os.path.exists(material_path):

        with bpy.data.libraries.load(material_path, False, False) as (data_from, data_to):
            for mat in data_from.materials:
                if mat == material_name:
                    data_to.materials = [mat]
                    break    
        
        for mat in data_to.materials:
            return mat

def assign_materials_to_assembly(assembly):
    props = get_kitchen_scene_props()

    for child in assembly.obj_bp.children:
        if child.type == 'MESH':
            for index, pointer in enumerate(child.material_pointer.slots):
                if index <= len(child.material_slots) and pointer.name in props.material_pointers:
                    p = props.material_pointers[pointer.name]
                    slot = child.material_slots[index]
                    slot.material = get_material(p.category,p.material_name)

def get_default_material_pointers():
    pointers = []
    pointers.append(("Wood Core Surfaces","Core","PB Small"))
    pointers.append(("Wood Core Edges","Core","PB Small"))
    pointers.append(("Exposed Cabinet Surfaces","Wood Colors","Autumn Leaves"))
    pointers.append(("Exposed Cabinet Edges","Wood Colors","Autumn Leaves"))
    pointers.append(("Interior Cabinet Surfaces","Wood Colors","Autumn Leaves"))
    pointers.append(("Interior Cabinet Edges","Wood Colors","Autumn Leaves"))
    pointers.append(("Door Surface","Wood Colors","Autumn Leaves"))
    pointers.append(("Door Edge","Wood Colors","Autumn Leaves"))
    pointers.append(("Countertop Surface","Wood Colors","Autumn Leaves"))
    pointers.append(("Drawer Box Surface","Wood Colors","Autumn Leaves"))
    pointers.append(("Drawer Box Edge","Wood Colors","Autumn Leaves"))
    pointers.append(("Pull Finish","Metal","Polished Chrome"))
    pointers.append(("Glass","Misc","Glass"))
    pointers.append(("Molding","Wood Colors","Autumn Leaves"))
    return pointers

def get_xml_path():
    path = os.path.join(os.path.dirname(__file__),'material_pointers')
    return os.path.join(path,"material_pointers.xml")

def write_xml_file():
    '''
    This writes the XML file from the current props. 
    This file gets written everytime a property changes.
    '''
    pointer_list = get_default_material_pointers()
    xml = XML()
    root = xml.create_tree()
    for pointer_item in pointer_list:
        pointer = xml.add_element(root,'MaterialPointer')
        xml.add_element_with_text(pointer,'Name',pointer_item[0])
        xml.add_element_with_text(pointer,'Category',pointer_item[1])
        xml.add_element_with_text(pointer,'Material',pointer_item[2])
    
    filepath = get_xml_path()

    xml.write(filepath)

    xml.format_xml_file(filepath)

def update_props_from_xml_file():
    '''
    This gets read on startup and sets the window manager props
    '''
    scene_props = get_kitchen_scene_props()

    if os.path.exists(get_xml_path()):
        xml = XML()
        root = xml.read_file(get_xml_path())

        for elm in root.findall("MaterialPointer"):
            pointer = scene_props.material_pointers.add()
            items = elm.getchildren()
            for item in items:
                if item.tag == 'Name':
                    pointer.name = item.text
                if item.tag == 'Category':
                    pointer.category = item.text
                if item.tag == 'Material':
                    pointer.material_name = item.text          

def add_bevel(assembly):
    for child in assembly.obj_bp.children:
        if child.type == 'MESH':
            bevel = child.modifiers.new('Bevel','BEVEL')    
            bevel.width = .0005            

def assign_material_pointers(assembly):
    for child in assembly.obj_bp.children:
        if child.type == 'MESH':
            for index, pointer in enumerate(child.material_pointer.slots):
                if pointer.name == 'Top':
                    pointer.name = "Interior Cabinet Surfaces"
                if pointer.name == 'Bottom':
                    pointer.name = "Wood Core Surfaces"
                if pointer.name == 'L1':
                    pointer.name = "Wood Core Edges"
                if pointer.name == 'L2':
                    pointer.name = "Exposed Cabinet Edges"
                if pointer.name == 'W1':
                    pointer.name = "Wood Core Edges"
                if pointer.name == 'W2':
                    pointer.name = "Wood Core Edges"                                