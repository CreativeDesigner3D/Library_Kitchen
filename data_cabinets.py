from .bp_lib import bp_types, bp_unit, bp_utils
from . import data_cabinet_parts
from . import data_cabinet_carcass
from . import data_countertops
from . import data_cabinet_doors
from . import kitchen_utils
import time
import math

class Base_Cabinet(bp_types.Assembly):
    show_in_library = True
    category_name = "Cabinets"
    prompt_id = "kitchen.cabinet_prompts"
    placement_id = "kitchen.place_cabinet"

    def draw(self):
        start_time = time.time()
        props = kitchen_utils.get_kitchen_scene_props()

        self.create_assembly()
        self.obj_bp["IS_CABINET_BP"] = True

        self.obj_x.location.x = bp_unit.inch(18) 
        self.obj_y.location.y = -props.base_cabinet_depth
        self.obj_z.location.z = props.base_cabinet_height

        width = self.obj_x.drivers.get_var('location.x','width')
        depth = self.obj_y.drivers.get_var('location.y','depth')
        height = self.obj_z.drivers.get_var('location.z','height')

        carcass = self.add_assembly(data_cabinet_carcass.Standard())
        carcass.set_name('Carcass')
        carcass.loc_x(value=0)
        carcass.loc_y(value=0)
        carcass.loc_z(value=0)
        carcass.dim_x('width',[width])
        carcass.dim_y('depth',[depth])
        carcass.dim_z('height',[height])

        print("Base_Cabinet: Draw Time --- %s seconds ---" % (time.time() - start_time))

class Test_Cabinet(bp_types.Assembly):
    show_in_library = True
    category_name = "Cabinets"
    prompt_id = "kitchen.cabinet_prompts"
    placement_id = "kitchen.place_cabinet"

    def draw(self):
        start_time = time.time()
        props = kitchen_utils.get_kitchen_scene_props()

        self.create_assembly()
        self.obj_bp["IS_CABINET_BP"] = True
        self.obj_y['IS_MIRROR'] = True
        self.obj_x.location.x = bp_unit.inch(18) 
        self.obj_y.location.y = -props.base_cabinet_depth
        self.obj_z.location.z = props.base_cabinet_height

        ctop_front = self.add_prompt("Countertop Overhang Front",'DISTANCE',bp_unit.inch(1))
        ctop_back = self.add_prompt("Countertop Overhang Back",'DISTANCE',bp_unit.inch(0))
        ctop_left = self.add_prompt("Countertop Overhang Left",'DISTANCE',bp_unit.inch(0))
        ctop_right = self.add_prompt("Countertop Overhang Right",'DISTANCE',bp_unit.inch(0))        

        width = self.obj_x.drivers.get_var('location.x','width')
        depth = self.obj_y.drivers.get_var('location.y','depth')
        height = self.obj_z.drivers.get_var('location.z','height')
        ctop_overhang_front = ctop_front.get_var('ctop_overhang_front')
        ctop_overhang_back = ctop_back.get_var('ctop_overhang_back')
        ctop_overhang_left = ctop_left.get_var('ctop_overhang_left')
        ctop_overhang_right = ctop_right.get_var('ctop_overhang_right')

        carcass = self.add_assembly(data_cabinet_carcass.Standard2())
        carcass.set_name('Carcass')
        carcass.loc_x(value=0)
        carcass.loc_y(value=0)
        carcass.loc_z(value=0)
        carcass.dim_x('width',[width])
        carcass.dim_y('depth',[depth])
        carcass.dim_z('height',[height])       

        material_thickness = carcass.get_prompt('Material Thickness').get_var('material_thickness')
        toe_kick_height = carcass.get_prompt('Toe Kick Height').get_var('toe_kick_height')

        countertop = self.add_assembly(data_countertops.Countertop())
        countertop.set_name('Countertop')
        countertop.loc_x('-ctop_overhang_left',[ctop_overhang_left])
        countertop.loc_y('ctop_overhang_back',[ctop_overhang_back])
        countertop.loc_z('height',[height])
        countertop.dim_x('width+ctop_overhang_left+ctop_overhang_right',[width,ctop_overhang_left,ctop_overhang_right])
        countertop.dim_y('depth-(ctop_overhang_front+ctop_overhang_back)',[depth,ctop_overhang_front,ctop_overhang_back])
        countertop.dim_z(value=.1)

        door = self.add_assembly(data_cabinet_doors.Door())
        door.set_name('Door')
        door.loc_x('material_thickness',[material_thickness])
        door.loc_y('depth',[depth])
        door.loc_z('toe_kick_height+material_thickness',[toe_kick_height,material_thickness])
        door.dim_x('width-(material_thickness*2)',[width,material_thickness])
        door.dim_y('depth',[depth])
        door.dim_z('height-toe_kick_height-(material_thickness*2)',[height,toe_kick_height,material_thickness])
        kitchen_utils.flip_normals(door)

        print("Test_Cabinet: Draw Time --- %s seconds ---" % (time.time() - start_time))

