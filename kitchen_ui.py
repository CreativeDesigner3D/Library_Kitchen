import bpy
from .bp_lib import bp_types, bp_unit, bp_utils

class KITCHEN_PT_library_settings(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_label = "Library"
    bl_region_type = 'HEADER'
    bl_ui_units_x = 18

    def draw(self, context):
        layout = self.layout

bpy.utils.register_class(KITCHEN_PT_library_settings)        