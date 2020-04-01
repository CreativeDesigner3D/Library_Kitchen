import bpy
import os
from .bp_lib import bp_utils
from . import kitchen_ui
from . import kitchen_props
from . import kitchen_ops
from . import data_cabinets

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

def register():
    lib = bpy.context.window_manager.bp_lib.script_libraries.add()
    lib.name = "Kitchen Library"
    lib.library_path = LIBRARY_PATH
    lib.panel_id = PANEL_ID

    bp_utils.load_library_items_from_module(lib,data_cabinets)


def unregister():
    for i, lib in enumerate(bpy.context.window_manager.bp_lib.script_libraries):
        if lib.name == "Kitchen Library":
            bpy.context.window_manager.bp_lib.script_libraries.remove(i)