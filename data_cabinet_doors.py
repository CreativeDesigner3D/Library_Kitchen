import math
from .bp_lib import bp_types, bp_unit, bp_utils
from . import data_cabinet_parts
from . import kitchen_utils
from . import common_prompts

from os import path

class Door(bp_types.Assembly):
    category_name = "Doors"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

    def draw(self):
        props = kitchen_utils.get_kitchen_scene_props()

        self.create_assembly("Door")
        self.obj_bp["IS_DOOR_BP"] = True

        common_prompts.add_door_prompts(self)
        common_prompts.add_front_prompts(self)
        common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)

        x = self.obj_x.drivers.get_var('location.x','x')
        y = self.obj_y.drivers.get_var('location.y','y')
        z = self.obj_z.drivers.get_var('location.z','z')
        top_overlay = self.get_prompt("Top Overlay").get_var('top_overlay')
        bottom_overlay = self.get_prompt("Bottom Overlay").get_var('bottom_overlay')
        left_overlay = self.get_prompt("Left Overlay").get_var('left_overlay')
        right_overlay = self.get_prompt("Right Overlay").get_var('right_overlay')
        door_to_cabinet_gap = self.get_prompt("Door to Cabinet Gap").get_var('door_to_cabinet_gap')
        front_thickness = self.get_prompt("Front Thickness").get_var('front_thickness')
        pull_vertical_location = self.get_prompt("Pull Vertical Location").get_var('pull_vertical_location')
        pull_horizontal_location = self.get_prompt("Pull Horizontal Location").get_var('pull_horizontal_location')

        door = data_cabinet_parts.add_door_part(self)
        door.set_name('Door')
        door.loc_x('-left_overlay',[left_overlay])
        door.loc_y('-door_to_cabinet_gap',[door_to_cabinet_gap])
        door.loc_z('-bottom_overlay',[bottom_overlay])
        door.rot_x(value = math.radians(90))
        door.rot_y(value = math.radians(-90))
        door.dim_x('z+top_overlay+bottom_overlay',[z,top_overlay,bottom_overlay])
        door.dim_y('(x+left_overlay+right_overlay)*-1',[x,left_overlay,right_overlay])
        door.dim_z('front_thickness',[front_thickness])      
        kitchen_utils.flip_normals(door)  

        pull_obj = kitchen_utils.get_pull(props.pull_category,props.pull_name)
        self.add_object(pull_obj)
        pull_obj.drivers.loc_y('-front_thickness',[front_thickness])
        pull_obj.drivers.loc_z('z-pull_vertical_location-'+str(pull_obj.dimensions.x)+'/2',[z,pull_vertical_location])
        pull_obj.drivers.loc_x('x-pull_horizontal_location',[x,pull_horizontal_location])
        pull_obj.rotation_euler.y = math.radians(90)
        kitchen_utils.assign_materials_to_object(pull_obj)
