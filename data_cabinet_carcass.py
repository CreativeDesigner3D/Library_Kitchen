import math
from .bp_lib import bp_types, bp_unit, bp_utils
from . import data_cabinet_parts
from . import kitchen_utils

from os import path

class Standard(bp_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

    def draw(self):
        props = kitchen_utils.get_kitchen_scene_props()

        self.create_assembly("Carcass")

        self.obj_x.location.x = bp_unit.inch(18) 
        self.obj_y.location.y = -props.base_cabinet_depth
        self.obj_z.location.z = props.base_cabinet_height

        width = self.obj_x.drivers.get_var('location.x','width')
        depth = self.obj_y.drivers.get_var('location.y','depth')
        height = self.obj_z.drivers.get_var('location.z','height')

        toe_kick_height = self.obj_prompts.prompt_page.add_prompt('DISTANCE',"Toe Kick Height")
        toe_kick_height.set_value(bp_unit.inch(4))
        toe_kick_setback = self.obj_prompts.prompt_page.add_prompt('DISTANCE',"Toe Kick Setback")
        toe_kick_setback.set_value(bp_unit.inch(3.25))
        material_thickness = self.obj_prompts.prompt_page.add_prompt('DISTANCE',"Material Thickness")
        material_thickness.set_value(bp_unit.inch(.75))
        run_sides_to_floor = self.obj_prompts.prompt_page.add_prompt('CHECKBOX',"Run Sides to Floor")
        run_sides_to_floor.set_value(bp_unit.inch(.75))

        toe_kick_height = toe_kick_height.get_var("toe_kick_height")
        toe_kick_setback = toe_kick_setback.get_var("toe_kick_setback")
        material_thickness = material_thickness.get_var("material_thickness")

        bottom = self.add_assembly(data_cabinet_parts.Cutpart())
        bottom.set_name('Bottom')
        bottom.loc_x('material_thickness',[material_thickness])
        bottom.loc_y(value=0)
        bottom.loc_z('toe_kick_height',[toe_kick_height])
        bottom.dim_x('width-(material_thickness*2)',[width,material_thickness])
        bottom.dim_y('depth',[depth])
        bottom.dim_z('material_thickness',[material_thickness])
        kitchen_utils.flip_normals(bottom)

        top = self.add_assembly(data_cabinet_parts.Cutpart())
        top.set_name('Top')
        top.loc_x('material_thickness',[material_thickness])
        top.loc_y(value=0)
        top.loc_z('height',[height])
        top.dim_x('width-(material_thickness*2)',[width,material_thickness])
        top.dim_y('depth',[depth])
        top.dim_z('-material_thickness',[material_thickness])

        left_side = self.add_assembly(data_cabinet_parts.Cutpart())
        left_side.set_name('Left Side')
        left_side.loc_x(value=0)
        left_side.loc_y(value=0)
        left_side.loc_z(value=0)
        left_side.rot_y(value=math.radians(-90))
        left_side.dim_x('height',[height])
        left_side.dim_y('depth',[depth])
        left_side.dim_z('-material_thickness',[material_thickness])

        right_side = self.add_assembly(data_cabinet_parts.Cutpart())
        right_side.set_name('Left Side')
        right_side.loc_x('width',[width])
        right_side.loc_y(value=0)
        right_side.loc_z(value=0)
        right_side.rot_y(value=math.radians(-90))
        right_side.dim_x('height',[height])
        right_side.dim_y('depth',[depth])
        right_side.dim_z('material_thickness',[material_thickness])
        kitchen_utils.flip_normals(right_side)

        back = self.add_assembly(data_cabinet_parts.Cutpart())
        back.set_name('Back')
        back.loc_x('width-material_thickness',[width,material_thickness])
        back.loc_y(value=0)
        back.loc_z('toe_kick_height+material_thickness',[toe_kick_height,material_thickness])
        back.rot_y(value=math.radians(-90))
        back.rot_z(value=math.radians(90))
        back.dim_x('height-toe_kick_height-(material_thickness*2)',[height,toe_kick_height,material_thickness])
        back.dim_y('width-(material_thickness*2)',[width,material_thickness])
        back.dim_z('material_thickness',[material_thickness])

        toe_kick = self.add_assembly(data_cabinet_parts.Cutpart())
        toe_kick.set_name('Toe Kick')
        toe_kick.loc_x('material_thickness',[material_thickness])
        toe_kick.loc_y('depth+toe_kick_setback',[depth,toe_kick_setback])
        toe_kick.loc_z(value=0)
        toe_kick.rot_x(value=math.radians(90))
        toe_kick.dim_x('width-(material_thickness*2)',[width,material_thickness])
        toe_kick.dim_y('toe_kick_height',[toe_kick_height])
        toe_kick.dim_z('material_thickness',[material_thickness])

class Standard2(bp_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

    def draw(self):
        props = kitchen_utils.get_kitchen_scene_props()

        self.create_assembly("Carcass")

        self.obj_bp["IS_CARCASS_BP"] = True

        self.obj_x.location.x = bp_unit.inch(18) 
        self.obj_y.location.y = -props.base_cabinet_depth
        self.obj_z.location.z = props.base_cabinet_height

        width = self.obj_x.drivers.get_var('location.x','width')
        depth = self.obj_y.drivers.get_var('location.y','depth')
        height = self.obj_z.drivers.get_var('location.z','height')

        left_finished_end = self.add_prompt("Left Finished End",'CHECKBOX',False)
        right_finished_end = self.add_prompt("Right Finished End",'CHECKBOX',False)
        run_sides_to_floor = self.add_prompt("Run Sides to Floor",'CHECKBOX',True)
        toe_kick_height = self.add_prompt("Toe Kick Height",'DISTANCE',bp_unit.inch(4))
        toe_kick_setback = self.add_prompt("Toe Kick Setback",'DISTANCE',bp_unit.inch(3.25))
        material_thickness = self.add_prompt("Material Thickness",'DISTANCE',bp_unit.inch(.75))

        toe_kick_height = toe_kick_height.get_var("toe_kick_height")
        toe_kick_setback = toe_kick_setback.get_var("toe_kick_setback")
        material_thickness = material_thickness.get_var("material_thickness")

        bottom = data_cabinet_parts.add_carcass_part(self)
        bottom.set_name('Bottom')
        bottom.loc_x('material_thickness',[material_thickness])
        bottom.loc_y(value=0)
        bottom.loc_z('toe_kick_height',[toe_kick_height])
        bottom.dim_x('width-(material_thickness*2)',[width,material_thickness])
        bottom.dim_y('depth',[depth])
        bottom.dim_z('material_thickness',[material_thickness])
        kitchen_utils.flip_normals(bottom)

        top = data_cabinet_parts.add_carcass_part(self)
        top.set_name('Top')
        top.loc_x('material_thickness',[material_thickness])
        top.loc_y(value=0)
        top.loc_z('height',[height])
        top.dim_x('width-(material_thickness*2)',[width,material_thickness])
        top.dim_y('depth',[depth])
        top.dim_z('-material_thickness',[material_thickness])

        left_side = data_cabinet_parts.add_carcass_part(self)
        left_side.obj_bp["IS_LEFT_SIDE_BP"] = True
        left_side.set_name('Left Side')
        left_side.loc_x(value=0)
        left_side.loc_y(value=0)
        left_side.loc_z(value=0)
        left_side.rot_y(value=math.radians(-90))
        left_side.dim_x('height',[height])
        left_side.dim_y('depth',[depth])
        left_side.dim_z('-material_thickness',[material_thickness])

        right_side = data_cabinet_parts.add_carcass_part(self)
        right_side.obj_bp["IS_RIGHT_SIDE_BP"] = True
        right_side.set_name('Right Side')
        right_side.loc_x('width',[width])
        right_side.loc_y(value=0)
        right_side.loc_z(value=0)
        right_side.rot_y(value=math.radians(-90))
        right_side.dim_x('height',[height])
        right_side.dim_y('depth',[depth])
        right_side.dim_z('material_thickness',[material_thickness])
        kitchen_utils.flip_normals(right_side)

        back = data_cabinet_parts.add_carcass_part(self)
        back.set_name('Back')
        back.loc_x('width-material_thickness',[width,material_thickness])
        back.loc_y(value=0)
        back.loc_z('toe_kick_height+material_thickness',[toe_kick_height,material_thickness])
        back.rot_y(value=math.radians(-90))
        back.rot_z(value=math.radians(90))
        back.dim_x('height-toe_kick_height-(material_thickness*2)',[height,toe_kick_height,material_thickness])
        back.dim_y('width-(material_thickness*2)',[width,material_thickness])
        back.dim_z('material_thickness',[material_thickness])

        toe_kick = data_cabinet_parts.add_carcass_part(self)
        toe_kick.set_name('Toe Kick')
        toe_kick.loc_x('material_thickness',[material_thickness])
        toe_kick.loc_y('depth+toe_kick_setback',[depth,toe_kick_setback])
        toe_kick.loc_z(value=0)
        toe_kick.rot_x(value=math.radians(90))
        toe_kick.dim_x('width-(material_thickness*2)',[width,material_thickness])
        toe_kick.dim_y('toe_kick_height',[toe_kick_height])
        toe_kick.dim_z('material_thickness',[material_thickness])

class Refrigerator(bp_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

class Transition(bp_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

class Blind_Corner(bp_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

class Inside_Corner(bp_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

class Outside_Corner(bp_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"