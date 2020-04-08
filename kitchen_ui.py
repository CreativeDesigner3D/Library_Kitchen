import bpy
from .bp_lib import bp_types, bp_unit, bp_utils
from . import kitchen_utils

class KITCHEN_PT_library_settings(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_label = "Library"
    bl_region_type = 'HEADER'
    bl_ui_units_x = 32

    def draw(self, context):
        layout = self.layout
        props = kitchen_utils.get_kitchen_scene_props()
        props.draw(layout)        


class KITCHEN_OT_cabinet_prompts(bpy.types.Operator):
    bl_idname = "kitchen.cabinet_prompts"
    bl_label = "Cabinet Prompts"

    cabinet = None

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        bp = kitchen_utils.get_cabinet_bp(context.object)
        self.cabinet = bp_types.Assembly(bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout

        # wall_thickness = self.assembly.get_prompt("Wall Thickness")

        col = layout.column(align=False)
        col.prop(self.cabinet.obj_x,'location',index=0,text="Width")
        col.prop(self.cabinet.obj_y,'location',index=1,text="Depth")
        col.prop(self.cabinet.obj_z,'location',index=2,text="Height")

        col = layout.column(align=True)
        col.prop(self.cabinet.obj_bp,'location',index=0,text="Location X")
        col.prop(self.cabinet.obj_bp,'location',index=1,text="Location Y")
        col.prop(self.cabinet.obj_bp,'location',index=2,text="Location Z")

        # wall_thickness.draw(layout)

def register():
    bpy.utils.register_class(KITCHEN_PT_library_settings)        
    bpy.utils.register_class(KITCHEN_OT_cabinet_prompts)     

def unregister():
    bpy.utils.unregister_class(KITCHEN_PT_library_settings)        
    bpy.utils.unregister_class(KITCHEN_OT_cabinet_prompts)        