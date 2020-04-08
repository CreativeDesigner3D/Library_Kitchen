import bpy
import os
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

preview_collections = {}
preview_collections["material_categories"] = bp_utils.create_image_preview_collection()
preview_collections["material_items"] = bp_utils.create_image_preview_collection()

def get_material_library_path():
    return os.path.join(os.path.dirname(__file__),"assets","Materials")

def enum_material_categories(self,context):
    if context is None:
        return []
    
    icon_dir = get_material_library_path()
    pcoll = preview_collections["material_categories"]
    return bp_utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_material_names(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(get_material_library_path(),self.material_category)
    pcoll = preview_collections["material_items"]
    return bp_utils.get_image_enum_previews(icon_dir,pcoll)

def update_material_category(self,context):
    if preview_collections["material_items"]:
        bpy.utils.previews.remove(preview_collections["material_items"])
        preview_collections["material_items"] = bp_utils.create_image_preview_collection()     
        
    enum_material_names(self,context)

def clear_material_categories(self,context):
    if preview_collections["material_categories"]:
        bpy.utils.previews.remove(preview_collections["material_categories"])
        preview_collections["material_categories"] = bp_utils.create_image_preview_collection()

    enum_material_categories(self,context)

class Kitchen_Material_Pointer(PropertyGroup):
    category: bpy.props.StringProperty(name="Category")
    material_name: bpy.props.StringProperty(name="Material Name")
    material: bpy.props.PointerProperty(name="Material",type=bpy.types.Material)

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

    material_pointers: bpy.props.CollectionProperty(name="Material Pointers",type=Kitchen_Material_Pointer)

    exposed_cabinet_surfaces: bpy.props.PointerProperty(name="Exposed Cabinet Surfaces",type=bpy.types.Material)
    interior_cabinet_surfaces: bpy.props.PointerProperty(name="Interior Cabinet Surfaces",type=bpy.types.Material)

    material_category: bpy.props.EnumProperty(name="Material Category",items=enum_material_categories,update=update_material_category)

    material_name: bpy.props.EnumProperty(name="Material Name",items=enum_material_names)

    def draw_materials(self,layout):
        split = layout.split(factor=.25)
        left_col = split.column()
        right_col = split.column()

        material_box = left_col.box()
        row = material_box.row()
        row.label(text="Material Selections:")

        material_box.prop(self,'material_category',text="",icon='FILE_FOLDER')  
        if len(self.material_name) > 0:
            material_box.template_icon_view(self,"material_name",show_labels=True)  

        right_row = right_col.row()
        right_row.scale_y = 1.3
        right_row.operator('kitchen.update_scene_materials',text="Update Materials",icon='FILE_REFRESH')

        box = right_col.box()
        col = box.column(align=True)
        for mat in self.material_pointers:
            row = col.row()
            row.operator('kitchen.update_material_pointer',text=mat.name,icon='FORWARD').pointer_name = mat.name
            row.label(text=mat.category + " - " + mat.material_name,icon='MATERIAL')

    def draw_cabinet_sizes(self,layout):
        col = layout.column(align=True)
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

    def draw(self,layout):
        col = layout.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(self, "kitchen_tabs", 'SIZES', icon='CON_SAMEVOL', text="Sizes") 
        row.prop_enum(self, "kitchen_tabs", 'CONSTRUCTION', icon='MOD_BUILD', text="Construction") 
        row.prop_enum(self, "kitchen_tabs", 'MATERIALS', icon='COLOR', text="Materials") 
        row.prop_enum(self, "kitchen_tabs", 'MOLDINGS', icon='MOD_SMOOTH', text="Moldings") 
        row.prop_enum(self, "kitchen_tabs", 'FRONTS', icon='FACESEL', text="Fronts") 
        row.prop_enum(self, "kitchen_tabs", 'HARDWARE', icon='MODIFIER_ON', text="Hardware") 
        row.prop_enum(self, "kitchen_tabs", 'TOOLS', icon='TOOL_SETTINGS', text="Tools") 

        box = col.box()

        if self.kitchen_tabs == 'SIZES':
            
            self.draw_cabinet_sizes(box)

        if self.kitchen_tabs == 'CONSTRUCTION':
            pass

        if self.kitchen_tabs == 'MATERIALS':

            self.draw_materials(box)

        if self.kitchen_tabs == 'MOLDINGS':
            pass

        if self.kitchen_tabs == 'FRONTS':
            pass

        if self.kitchen_tabs == 'HARDWARE':
            pass

        if self.kitchen_tabs == 'TOOLS':
            pass        


    @classmethod
    def register(cls):
        bpy.types.Scene.kitchen = PointerProperty(
            name="Kitchen Props",
            description="Kitchen Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.kitchen

def register():
    bpy.utils.register_class(Kitchen_Material_Pointer)  
    bpy.utils.register_class(Kitchen_Scene_Props)  

def unregister():
    bpy.utils.unregister_class(Kitchen_Material_Pointer)   
    bpy.utils.unregister_class(Kitchen_Scene_Props)        