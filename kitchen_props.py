import bpy
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        UIList,
        )
from bpy.props import (
        BoolProperty,
        FloatProperty,
        IntProperty,
        PointerProperty,
        StringProperty,
        CollectionProperty,
        EnumProperty,
        )
from .bp_lib import bp_types, bp_unit, bp_utils

class Kitchen_Scene_Props(PropertyGroup):
    kitchen_tabs: EnumProperty(name="Kitchen Tabs",
                            items=[('SIZES',"Sizes","Default Cabinet Sizes"),
                                   ('CONSTRUCTION',"Construction","Show the Cabinet Construction Options"),
                                   ('MATERIALS',"Materials","Show the Material Options"),
                                   ('MOLDINGS',"Moldings","Show the Molding Options"),
                                   ('FRONTS',"Fronts","Show the Door and Drawer Front Options"),
                                   ('HARDWARE',"Hardware","Show the Hardware Options"),
                                   ('TOOLS',"Tools","Show the Tools")],
                            default='SIZES')

    base_cabinet_depth: bpy.props.FloatProperty(name="Base Cabinet Depth",
                                                 description="Default depth for base cabinets",
                                                 default=bp_unit.inch(23.0),
                                                 unit='LENGTH')
    
    base_cabinet_height: bpy.props.FloatProperty(name="Base Cabinet Height",
                                                  description="Default height for base cabinets",
                                                  default=bp_unit.inch(34.0),
                                                  unit='LENGTH')
    
    base_inside_corner_size: bpy.props.FloatProperty(name="Base Inside Corner Size",
                                                     description="Default width and depth for the inside base corner cabinets",
                                                     default=bp_unit.inch(36.0),
                                                     unit='LENGTH')
    
    tall_cabinet_depth: bpy.props.FloatProperty(name="Tall Cabinet Depth",
                                                 description="Default depth for tall cabinets",
                                                 default=bp_unit.inch(25.0),
                                                 unit='LENGTH')
    
    tall_cabinet_height: bpy.props.FloatProperty(name="Tall Cabinet Height",
                                                  description="Default height for tall cabinets",
                                                  default=bp_unit.inch(84.0),
                                                  unit='LENGTH')
    
    upper_cabinet_depth: bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                  description="Default depth for upper cabinets",
                                                  default=bp_unit.inch(12.0),
                                                  unit='LENGTH')
    
    upper_cabinet_height: bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                   description="Default height for upper cabinets",
                                                   default=bp_unit.inch(34.0),
                                                   unit='LENGTH')
    
    upper_inside_corner_size: bpy.props.FloatProperty(name="Upper Inside Corner Size",
                                                      description="Default width and depth for the inside upper corner cabinets",
                                                      default=bp_unit.inch(24.0),
                                                      unit='LENGTH')
    
    sink_cabinet_depth: bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                 description="Default depth for sink cabinets",
                                                 default=bp_unit.inch(23.0),
                                                 unit='LENGTH')
    
    sink_cabinet_height: bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                  description="Default height for sink cabinets",
                                                  default=bp_unit.inch(34.0),
                                                  unit='LENGTH')

    suspended_cabinet_depth: bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                      description="Default depth for suspended cabinets",
                                                      default=bp_unit.inch(23.0),
                                                      unit='LENGTH')
    
    suspended_cabinet_height: bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                       description="Default height for suspended cabinets",
                                                       default=bp_unit.inch(6.0),
                                                       unit='LENGTH')

    column_width: bpy.props.FloatProperty(name="Column Width",
                                           description="Default width for cabinet columns",
                                           default=bp_unit.inch(2),
                                           unit='LENGTH')

    width_1_door: bpy.props.FloatProperty(name="Width 1 Door",
                                           description="Default width for one door wide cabinets",
                                           default=bp_unit.inch(18.0),
                                           unit='LENGTH')
    
    width_2_door: bpy.props.FloatProperty(name="Width 2 Door",
                                           description="Default width for two door wide and open cabinets",
                                           default=bp_unit.inch(36.0),
                                           unit='LENGTH')
    
    width_drawer: bpy.props.FloatProperty(name="Width Drawer",
                                           description="Default width for drawer cabinets",
                                           default=bp_unit.inch(18.0),
                                           unit='LENGTH')
    
    base_width_blind: bpy.props.FloatProperty(name="Base Width Blind",
                                               description="Default width for base blind corner cabinets",
                                               default=bp_unit.inch(48.0),
                                               unit='LENGTH')
    
    tall_width_blind: bpy.props.FloatProperty(name="Tall Width Blind",
                                               description="Default width for tall blind corner cabinets",
                                               default=bp_unit.inch(48.0),
                                               unit='LENGTH')
    
    blind_panel_reveal: bpy.props.FloatProperty(name="Blind Panel Reveal",
                                                 description="Default reveal for blind panels",
                                                 default=bp_unit.inch(3.0),
                                                 unit='LENGTH')
    
    inset_blind_panel: bpy.props.BoolProperty(name="Inset Blind Panel",
                                               description="Check this to inset the blind panel into the cabinet carcass",
                                               default=True)
    
    upper_width_blind: bpy.props.FloatProperty(name="Upper Width Blind",
                                                description="Default width for upper blind corner cabinets",
                                                default=bp_unit.inch(36.0),
                                                unit='LENGTH')

    height_above_floor: bpy.props.FloatProperty(name="Height Above Floor",
                                                 description="Default height above floor for upper cabinets",
                                                 default=bp_unit.inch(84.0),
                                                 unit='LENGTH')
    
    equal_drawer_stack_heights: bpy.props.BoolProperty(name="Equal Drawer Stack Heights", 
                                                        description="Check this make all drawer stack heights equal. Otherwise the Top Drawer Height will be set.", 
                                                        default=True)
    
    top_drawer_front_height: bpy.props.FloatProperty(name="Top Drawer Front Height",
                                                      description="Default top drawer front height.",
                                                      default=bp_unit.inch(6.0),
                                                      unit='LENGTH')

    def draw(self,layout):
        col = layout.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(self, "kitchen_tabs", 'SIZES', icon='CON_SAMEVOL', text="Sizes") 
        row.prop_enum(self, "kitchen_tabs", 'CONSTRUCTION', icon='MOD_BUILD', text="Construction") 
        row.prop_enum(self, "kitchen_tabs", 'MATERIALS', icon='COLOR', text="Materials") 
        row.prop_enum(self, "kitchen_tabs", 'MOLDINGS', icon='MOD_SMOOTH', text="Moldings") 
        row.prop_enum(self, "kitchen_tabs", 'FRONTS', icon='MODIFIER_ON', text="Fronts") 
        row.prop_enum(self, "kitchen_tabs", 'HARDWARE', icon='FACESEL', text="Hardware") 
        row.prop_enum(self, "kitchen_tabs", 'TOOLS', icon='TOOL_SETTINGS', text="Tools") 

        box = col.box()

        if self.kitchen_tabs == 'SIZES':
            
            col = box.column(align=True)
            split = col.split(factor=.7,align=True)

            box = col.box()
            box.label(text="Standard Cabinet Sizes:")
            
            row = box.row(align=True)
            row.label(text="Base:")
            row.prop(self,"base_cabinet_height",text="Height")
            row.prop(self,"base_cabinet_depth",text="Depth")
            
            row = box.row(align=True)
            row.label(text="Tall:")
            row.prop(self,"tall_cabinet_height",text="Height")
            row.prop(self,"tall_cabinet_depth",text="Depth")
            
            row = box.row(align=True)
            row.label(text="Upper:")
            row.prop(self,"upper_cabinet_height",text="Height")
            row.prop(self,"upper_cabinet_depth",text="Depth")

            row = box.row(align=True)
            row.label(text="Sink:")
            row.prop(self,"sink_cabinet_height",text="Height")
            row.prop(self,"sink_cabinet_depth",text="Depth")
            
            row = box.row(align=True)
            row.label(text="Suspended:")
            row.prop(self,"suspended_cabinet_height",text="Height")
            row.prop(self,"suspended_cabinet_depth",text="Depth")
            
            row = box.row(align=True)
            row.label(text="1 Door Wide:")
            row.prop(self,"width_1_door",text="Width")
            
            row = box.row(align=True)
            row.label(text="2 Door Wide:")
            row.prop(self,"width_2_door",text="Width")
            
            row = box.row(align=True)
            row.label(text="Drawer Stack Width:")
            row.prop(self,"width_drawer",text="Width")
            
            box = col.box()
            box.label(text="Blind Cabinet Widths:")
            
            row = box.row(align=True)
            row.label(text='Base:')
            row.prop(self,"base_width_blind",text="Width")
            
            row = box.row(align=True)
            row.label(text='Tall:')
            row.prop(self,"tall_width_blind",text="Width")
            
            row = box.row(align=True)
            row.label(text='Upper:')
            row.prop(self,"upper_width_blind",text="Width")
            
            box = col.box()
            box.label(text="Inside Corner Cabinet Sizes:")
            row = box.row(align=True)
            row.label(text="Base:")
            row.prop(self,"base_inside_corner_size",text="")
            
            row = box.row(align=True)
            row.label(text="Upper:")
            row.prop(self,"upper_inside_corner_size",text="")
            
            box = col.box()
            box.label(text="Placement:")
            row = box.row(align=True)
            row.label(text="Height Above Floor:")
            row.prop(self,"height_above_floor",text="")
            
            box = col.box()
            box.label(text="Drawer Heights:")
            row = box.row(align=True)
            row.prop(self,"equal_drawer_stack_heights")
            if not self.equal_drawer_stack_heights:
                row.prop(self,"top_drawer_front_height")

    @classmethod
    def register(cls):
        bpy.types.Scene.kitchen = PointerProperty(
            name="Room Props",
            description="Room Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.kitchen

bpy.utils.register_class(Kitchen_Scene_Props)        