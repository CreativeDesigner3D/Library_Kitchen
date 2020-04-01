import bpy

def get_kitchen_scene_props():
    return bpy.context.scene.kitchen

def get_cabinet_bp(obj):
    if "IS_CABINET_BP" in obj:
        return obj
    elif obj.parent:
        return get_cabinet_bp(obj.parent)