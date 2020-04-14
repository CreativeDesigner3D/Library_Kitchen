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

    assembly = None
    obj = None
    exclude_objects = []

    class_name = ""

    def execute(self, context):
        # self.starting_point = ()
        
        self.create_drawing_plane(context)
        self.get_cabinet(context)
        # self.create_wall()
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
            print('MOUSE',mouse_location)
            print('BP,X',sel_cabinet_world_loc,sel_cabinet_x_world_loc)

            dist_to_bp = bp_utils.calc_distance(mouse_location,sel_cabinet_world_loc)
            dist_to_x = bp_utils.calc_distance(mouse_location,sel_cabinet_x_world_loc)
            rot = self.selected_cabinet.obj_bp.rotation_euler.z
            x_loc = 0
            y_loc = 0

            if wall_bp:
                rot += wall.obj_bp.rotation_euler.z      
            print('DIST',dist_to_bp,dist_to_x)
            if dist_to_bp < dist_to_x:
                print('LEFT')
                #LEFT
                add_x_loc = 0
                add_y_loc = 0
                # if sel_product.obj_bp.mv.placement_type == 'Corner':
                #     rot += math.radians(90)
                #     add_x_loc = math.cos(rot) * sel_product.obj_y.location.y
                #     add_y_loc = math.sin(rot) * sel_product.obj_y.location.y
                x_loc = self.selected_cabinet.obj_bp.matrix_world[0][3] - math.cos(rot) * self.cabinet.obj_x.location.x + add_x_loc
                y_loc = self.selected_cabinet.obj_bp.matrix_world[1][3] - math.sin(rot) * self.cabinet.obj_x.location.x + add_y_loc

            else:
                print('RIGHT')
                #RIGHT
                x_loc = self.selected_cabinet.obj_bp.matrix_world[0][3] + math.cos(rot) * self.selected_cabinet.obj_x.location.x
                y_loc = self.selected_cabinet.obj_bp.matrix_world[1][3] + math.sin(rot) * self.selected_cabinet.obj_x.location.x

            self.cabinet.obj_bp.rotation_euler.z = rot
            self.cabinet.obj_bp.location.x = x_loc
            self.cabinet.obj_bp.location.y = y_loc

        elif wall_bp:
            pass
        else:
            self.cabinet.obj_bp.location = mouse_location

    def get_cabinet(self,context):
        self.exclude_objects = []
        obj = bpy.data.objects[self.obj_bp_name]
        cabinet_bp = kitchen_utils.get_cabinet_bp(obj)
        self.cabinet = bp_types.Assembly(cabinet_bp)
        self.set_child_properties(self.cabinet.obj_bp)

    # def set_child_properties(self,obj):
    #     obj["PROMPT_ID"] = "kitchen.cabinet_prompts"   
    #     if obj.type == 'EMPTY':
    #         obj.hide_viewport = True    
    #     if obj.name != self.drawing_plane.name:
    #         self.exclude_objects.append(obj)    
    #     if obj.mesh == 'MESH':
    #         obj.display_type = 'WIRE'            
    #     for child in obj.children:
    #         self.set_child_properties(child)

    # def set_placed_properties(self,obj):
    #     if obj.mesh == 'MESH':
    #         obj.display_type = 'TEXTURED'
    #     for child in obj.children:
    #         self.set_placed_properties(child)

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

    def modal(self, context, event):
        context.area.tag_redraw()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y

        selected_point, selected_obj = bp_utils.get_selection_point(context,event,exclude_objects=self.exclude_objects)

        self.position_cabinet(selected_point,selected_obj)
        # self.position_object(selected_point,selected_obj)
        # self.set_end_angles()            

        if self.event_is_place_first_point(event):
            return self.finish(context)
            
        # if self.event_is_place_next_point(event):
        #     self.set_placed_properties(self.current_wall.obj_bp)
        #     self.create_wall()
        #     self.connect_walls()
        #     self.starting_point = (selected_point[0],selected_point[1],selected_point[2])
        #     return {'RUNNING_MODAL'}

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

    # def set_end_angles(self):
    #     if self.previous_wall and self.current_wall:
    #         left_angle = self.current_wall.get_prompt("Left Angle")
    #         # right_angle = self.current_wall.get_prompt("Right Angle")    

    #         # prev_left_angle = self.previous_wall.get_prompt("Left Angle")
    #         prev_right_angle = self.previous_wall.get_prompt("Right Angle") 

    #         prev_rot = self.previous_wall.obj_bp.rotation_euler.z  
    #         rot = self.current_wall.obj_bp.rotation_euler.z

    #         left_angle.set_value((rot-prev_rot)/2)
    #         prev_right_angle.set_value((prev_rot-rot)/2)

    #         self.current_wall.obj_prompts.location = self.current_wall.obj_prompts.location
    #         self.previous_wall.obj_prompts.location = self.previous_wall.obj_prompts.location            
        
    def position_object(self,selected_point,selected_obj):
        self.cabinet.obj_bp.location = selected_point

    def cancel_drop(self,context):
        bp_utils.delete_object_and_children(self.cabinet.obj_bp)
        bp_utils.delete_object_and_children(self.drawing_plane)
        return {'CANCELLED'}

    def finish(self,context):
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

def register():
    bpy.utils.register_class(KITCHEN_OT_place_cabinet)        
    bpy.utils.register_class(KITCHEN_OT_update_scene_materials)     
    bpy.utils.register_class(KITCHEN_OT_update_material_pointer)   
    bpy.utils.register_class(KITCHEN_OT_update_scene_pulls) 
    bpy.utils.register_class(KITCHEN_OT_update_pull_pointer)   

def unregister():    
    bpy.utils.unregister_class(KITCHEN_OT_place_cabinet)        
    bpy.utils.unregister_class(KITCHEN_OT_update_scene_materials)     
    bpy.utils.unregister_class(KITCHEN_OT_update_material_pointer)      
    bpy.utils.unregister_class(KITCHEN_OT_update_scene_pulls)  
    bpy.utils.unregister_class(KITCHEN_OT_update_pull_pointer)     