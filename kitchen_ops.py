import bpy
import os
import math
from .bp_lib import bp_types, bp_unit, bp_utils
from . import kitchen_utils

class KITCHEN_OT_place_cabinet(bpy.types.Operator):
    bl_idname = "kitchen.place_cabinet"
    bl_label = "Place Cabinet"
    
    filepath: bpy.props.StringProperty(name="Filepath",default="Error")

    obj_bp_name: bpy.props.StringProperty(name="Obj Base Point Name")
    
    cabinet = None
    selected_cabinet = None

    drawing_plane = None

    next_wall = None
    current_wall = None
    previous_wall = None

    starting_point = ()
    placement = ''

    assembly = None
    obj = None
    exclude_objects = []

    class_name = ""

    def execute(self, context):
        self.create_drawing_plane(context)
        self.get_cabinet(context)
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def position_cabinet(self,mouse_location,selected_obj):
        cabinet_bp = kitchen_utils.get_cabinet_bp(selected_obj)
        wall_bp = kitchen_utils.get_wall_bp(selected_obj)
        if cabinet_bp:
            self.selected_cabinet = bp_types.Assembly(cabinet_bp)

            sel_cabinet_world_loc = (self.selected_cabinet.obj_bp.matrix_world[0][3],
                                     self.selected_cabinet.obj_bp.matrix_world[1][3],
                                     self.selected_cabinet.obj_bp.matrix_world[2][3])
            
            sel_cabinet_x_world_loc = (self.selected_cabinet.obj_x.matrix_world[0][3],
                                       self.selected_cabinet.obj_x.matrix_world[1][3],
                                       self.selected_cabinet.obj_x.matrix_world[2][3])

            dist_to_bp = bp_utils.calc_distance(mouse_location,sel_cabinet_world_loc)
            dist_to_x = bp_utils.calc_distance(mouse_location,sel_cabinet_x_world_loc)
            rot = self.selected_cabinet.obj_bp.rotation_euler.z
            x_loc = 0
            y_loc = 0

            if wall_bp:
                self.current_wall = bp_types.Assembly(wall_bp)
                rot += self.current_wall.obj_bp.rotation_euler.z      

            if dist_to_bp < dist_to_x:
                self.placement = 'LEFT'
                add_x_loc = 0
                add_y_loc = 0
                # if sel_product.obj_bp.mv.placement_type == 'Corner':
                #     rot += math.radians(90)
                #     add_x_loc = math.cos(rot) * sel_product.obj_y.location.y
                #     add_y_loc = math.sin(rot) * sel_product.obj_y.location.y
                x_loc = self.selected_cabinet.obj_bp.matrix_world[0][3] - math.cos(rot) * self.cabinet.obj_x.location.x + add_x_loc
                y_loc = self.selected_cabinet.obj_bp.matrix_world[1][3] - math.sin(rot) * self.cabinet.obj_x.location.x + add_y_loc

            else:
                self.placement = 'RIGHT'
                x_loc = self.selected_cabinet.obj_bp.matrix_world[0][3] + math.cos(rot) * self.selected_cabinet.obj_x.location.x
                y_loc = self.selected_cabinet.obj_bp.matrix_world[1][3] + math.sin(rot) * self.selected_cabinet.obj_x.location.x

            self.cabinet.obj_bp.rotation_euler.z = rot
            self.cabinet.obj_bp.location.x = x_loc
            self.cabinet.obj_bp.location.y = y_loc

        elif wall_bp:
            self.placement = 'WALL'
            self.current_wall = bp_types.Assembly(wall_bp)
            self.cabinet.obj_bp.rotation_euler = self.current_wall.obj_bp.rotation_euler
            self.cabinet.obj_bp.location.x = mouse_location[0]
            self.cabinet.obj_bp.location.y = mouse_location[1]

        else:
            self.cabinet.obj_bp.location = mouse_location

    def get_cabinet(self,context):
        self.exclude_objects = []
        obj = bpy.data.objects[self.obj_bp_name]
        cabinet_bp = kitchen_utils.get_cabinet_bp(obj)
        self.cabinet = bp_types.Assembly(cabinet_bp)
        self.set_child_properties(self.cabinet.obj_bp)
        self.refresh_data(False)      

    def set_child_properties(self,obj):
        obj["PROMPT_ID"] = "kitchen.cabinet_prompts"   
        if obj.type == 'EMPTY':
            obj.hide_viewport = True    
        if obj.type == 'MESH':
            obj.display_type = 'WIRE'            
        if obj.name != self.drawing_plane.name:
            self.exclude_objects.append(obj)    
        for child in obj.children:
            self.set_child_properties(child)

    def set_placed_properties(self,obj):
        if obj.type == 'MESH':
            obj.display_type = 'TEXTURED'          
        for child in obj.children:
            self.set_placed_properties(child) 

    def create_drawing_plane(self,context):
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        plane.location = (0,0,0)
        self.drawing_plane = context.active_object
        self.drawing_plane.display_type = 'WIRE'
        self.drawing_plane.dimensions = (100,100,1)

    def confirm_placement(self,context):
        if self.current_wall:
            x_loc = bp_utils.calc_distance((self.cabinet.obj_bp.location.x,self.cabinet.obj_bp.location.y,0),
                                           (self.current_wall.obj_bp.matrix_local[0][3],self.current_wall.obj_bp.matrix_local[1][3],0))

            self.cabinet.obj_bp.location = (0,0,self.cabinet.obj_bp.location.z)
            self.cabinet.obj_bp.rotation_euler = (0,0,0)
            self.cabinet.obj_bp.parent = self.current_wall.obj_bp
            self.cabinet.obj_bp.location.x = x_loc

        if self.placement == 'LEFT':
            self.cabinet.obj_bp.parent = self.selected_cabinet.obj_bp.parent
            constraint_obj = self.cabinet.obj_x
            constraint = self.selected_cabinet.obj_bp.constraints.new('COPY_LOCATION')
            constraint.target = constraint_obj
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = True

        if self.placement == 'RIGHT':
            self.cabinet.obj_bp.parent = self.selected_cabinet.obj_bp.parent
            constraint_obj = self.selected_cabinet.obj_x
            constraint = self.cabinet.obj_bp.constraints.new('COPY_LOCATION')
            constraint.target = constraint_obj
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = True

    def modal(self, context, event):
        context.area.tag_redraw()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y

        selected_point, selected_obj = bp_utils.get_selection_point(context,event,exclude_objects=self.exclude_objects)

        self.position_cabinet(selected_point,selected_obj)

        if self.event_is_place_first_point(event):
            self.confirm_placement(context)
            return self.finish(context)
            
        if self.event_is_cancel_command(event):
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'} 

        return {'RUNNING_MODAL'}

    def event_is_place_next_point(self,event):
        if self.starting_point == ():
            return False
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
            return True
        elif event.type == 'RET' and event.value == 'PRESS':
            return True
        else:
            return False

    def event_is_place_first_point(self,event):
        if self.starting_point != ():
            return False
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
            return True
        elif event.type == 'RET' and event.value == 'PRESS':
            return True
        else:
            return False

    def event_is_cancel_command(self,event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            return True
        else:
            return False
    
    def event_is_pass_through(self,event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return True
        else:
            return False

    def position_object(self,selected_point,selected_obj):
        self.cabinet.obj_bp.location = selected_point

    def cancel_drop(self,context):
        bp_utils.delete_object_and_children(self.cabinet.obj_bp)
        bp_utils.delete_object_and_children(self.drawing_plane)
        return {'CANCELLED'}

    def refresh_data(self,hide=True):
        ''' For some reason matrix world doesn't evaluate correctly
            when placing cabinets next to this
        '''
        self.cabinet.obj_x.hide_viewport = hide
        self.cabinet.obj_y.hide_viewport = hide
        self.cabinet.obj_z.hide_viewport = hide
        self.cabinet.obj_x.empty_display_size = .01
        self.cabinet.obj_y.empty_display_size = .01
        self.cabinet.obj_z.empty_display_size = .01
 
    def finish(self,context):
        self.refresh_data(True)
        context.window.cursor_set('DEFAULT')
        if self.drawing_plane:
            bp_utils.delete_obj_list([self.drawing_plane])
        self.set_placed_properties(self.cabinet.obj_bp) 
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        return {'FINISHED'}


class KITCHEN_OT_update_scene_materials(bpy.types.Operator):
    bl_idname = "kitchen.update_scene_materials"
    bl_label = "Update Scene Materials"
    
    def execute(self, context):
        for obj in context.visible_objects:
            print(obj)
        return {'FINISHED'}


class KITCHEN_OT_update_material_pointer(bpy.types.Operator):
    bl_idname = "kitchen.update_material_pointer"
    bl_label = "Update Material Pointer"
    
    pointer_name: bpy.props.StringProperty(name="Pointer Name")

    def execute(self, context):
        for obj in context.visible_objects:
            print(obj)
        return {'FINISHED'}


class KITCHEN_OT_update_scene_pulls(bpy.types.Operator):
    bl_idname = "kitchen.update_scene_pulls"
    bl_label = "Update Scene Pulls"
    
    def execute(self, context):
        for obj in context.visible_objects:
            print(obj)
        return {'FINISHED'}


class KITCHEN_OT_update_pull_pointer(bpy.types.Operator):
    bl_idname = "kitchen.update_pull_pointer"
    bl_label = "Update Pull Pointer"
    
    pointer_name: bpy.props.StringProperty(name="Pointer Name")

    def execute(self, context):
        for obj in context.visible_objects:
            print(obj)
        return {'FINISHED'}


class KITCHEN_OT_disconnect_cabinet_constraint(bpy.types.Operator):
    bl_idname = "kitchen.disconnect_cabinet_constraint"
    bl_label = "Disconnect Cabinet Constraint"
    
    obj_name: bpy.props.StringProperty(name="Base Point Name")

    def execute(self, context):
        obj = bpy.data.objects[self.obj_name]
        obj.constraints.clear()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(KITCHEN_OT_place_cabinet)        
    bpy.utils.register_class(KITCHEN_OT_update_scene_materials)     
    bpy.utils.register_class(KITCHEN_OT_update_material_pointer)   
    bpy.utils.register_class(KITCHEN_OT_update_scene_pulls) 
    bpy.utils.register_class(KITCHEN_OT_update_pull_pointer)   
    bpy.utils.register_class(KITCHEN_OT_disconnect_cabinet_constraint)   

def unregister():    
    bpy.utils.unregister_class(KITCHEN_OT_place_cabinet)        
    bpy.utils.unregister_class(KITCHEN_OT_update_scene_materials)     
    bpy.utils.unregister_class(KITCHEN_OT_update_material_pointer)      
    bpy.utils.unregister_class(KITCHEN_OT_update_scene_pulls)  
    bpy.utils.unregister_class(KITCHEN_OT_update_pull_pointer)     
    bpy.utils.unregister_class(KITCHEN_OT_disconnect_cabinet_constraint)     