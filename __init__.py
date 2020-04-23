import bpy
import os
from .bp_lib import bp_utils
from . import kitchen_utils
from . import kitchen_ui
from . import kitchen_props
from . import kitchen_ops
from . import data_cabinets
from bpy.app.handlers import persistent

bl_info = {
    "name": "Kitchen Library",
    "author": "Andrew Peel",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Asset Library",
    "description": "Library that adds the ability to design kitchens",
    "warning": "",
    "wiki_url": "",
    "category": "Asset Library",
}

LIBRARY_PATH = os.path.join(os.path.dirname(__file__),"library")
PANEL_ID = 'KITCHEN_PT_library_settings'

@persistent
def load_library_on_file_load(scene=None):
    libraries = bpy.context.window_manager.bp_lib.script_libraries
    if "Kitchen Library" not in libraries:
        lib = libraries.add()
        lib.name = "Kitchen Library"
        lib.library_path = LIBRARY_PATH
        lib.panel_id = PANEL_ID

        bp_utils.load_library_items_from_module(lib,data_cabinets)

@persistent
def load_pointers(scene=None):
    kitchen_utils.write_pointer_files()
    kitchen_utils.update_pointer_properties()

def register():
    kitchen_props.register()
    kitchen_ui.register()
    kitchen_ops.register()

    load_library_on_file_load()
    bpy.app.handlers.load_post.append(load_library_on_file_load)
    bpy.app.handlers.load_post.append(load_pointers)

def unregister():
    kitchen_props.unregister()
    kitchen_ui.unregister()
    kitchen_ops.unregister()

    bpy.app.handlers.load_post.remove(load_library_on_file_load)  
    bpy.app.handlers.load_post.remove(load_pointers)  

    for i, lib in enumerate(bpy.context.window_manager.bp_lib.script_libraries):
        if lib.name == "Kitchen Library":
            bpy.context.window_manager.bp_lib.script_libraries.remove(i)