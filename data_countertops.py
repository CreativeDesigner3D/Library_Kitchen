import math
from .bp_lib import bp_types, bp_unit, bp_utils
from . import data_cabinet_parts
from . import kitchen_utils

from os import path

class Countertop(bp_types.Assembly):
    category_name = "Countertop"
    prompt_id = ""
    placement_id = ""

    def draw(self):
        self.create_assembly("Carcass")

        self.obj_bp["IS_COUNTERTOP_BP"] = True

        self.obj_x.location.x = bp_unit.inch(18) 
        self.obj_y.location.y = -bp_unit.inch(22) 
        self.obj_z.location.z = bp_unit.inch(1.5) 

        add_backsplash = self.add_prompt("Add Backsplash",'CHECKBOX',True)
        add_left_backsplash = self.add_prompt("Add Left Backsplash",'CHECKBOX',False)
        add_right_backsplash = self.add_prompt("Add Right Backsplash",'CHECKBOX',False)
        side_splash_setback = self.add_prompt("Side Splash Setback",'DISTANCE',bp_unit.inch(2.75))
        deck_thickness = self.add_prompt("Deck Thickness",'DISTANCE',bp_unit.inch(1.5))
        splash_thickness = self.add_prompt("Splash Thickness",'DISTANCE',bp_unit.inch(.75))

        width = self.obj_x.drivers.get_var('location.x','width')
        depth = self.obj_y.drivers.get_var('location.y','depth')
        height = self.obj_z.drivers.get_var('location.z','height')        
        deck_thickness = deck_thickness.get_var('deck_thickness')
        splash_thickness = splash_thickness.get_var('splash_thickness')

        deck = data_cabinet_parts.add_countertop_part(self)
        deck.set_name('Top')
        deck.loc_x(value=0)
        deck.loc_y(value=0)
        deck.loc_z(value=0)
        deck.dim_x('width',[width])
        deck.dim_y('depth',[depth])
        deck.dim_z('deck_thickness',[deck_thickness])
        kitchen_utils.assign_countertop_pointers
        kitchen_utils.flip_normals(deck)
