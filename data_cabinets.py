from .bp_lib import bp_types, bp_unit, bp_utils
from . import data_cabinet_carcass
from . import kitchen_utils

class Base_Cabinet(bp_types.Assembly):
    show_in_library = True
    category_name = "Cabinets"
    prompt_id = "kitchen.cabinet_prompts"
    placement_id = "kitchen.place_cabinet"

    def draw(self):
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



