from .bp_lib import bp_types, bp_unit, bp_utils

def add_front_prompts(assembly):
    assembly.add_prompt("Inset Front",'CHECKBOX',False)
    assembly.add_prompt("Door to Cabinet Gap",'DISTANCE',bp_unit.inch(.125))
    assembly.add_prompt("Front Thickness",'DISTANCE',bp_unit.inch(.75))

def add_door_prompts(assembly):
    assembly.add_prompt("Door Rotation",'ANGLE',0)
    assembly.add_prompt("Open Door",'PERCENTAGE',0)

def add_front_overlay_prompts(assembly):
    assembly.add_prompt("Inset Reveal",'DISTANCE',bp_unit.inch(.125))
    assembly.add_prompt("Top Overlay",'DISTANCE',bp_unit.inch(.6875))
    assembly.add_prompt("Bottom Overlay",'DISTANCE',bp_unit.inch(.6875))
    assembly.add_prompt("Left Overlay",'DISTANCE',bp_unit.inch(.6875))
    assembly.add_prompt("Right Overlay",'DISTANCE',bp_unit.inch(.6875))
    assembly.add_prompt("Vertical Gap",'DISTANCE',bp_unit.inch(.125))

def add_pull_prompts(assembly):
    assembly.add_prompt("Pull Vertical Location",'DISTANCE',bp_unit.inch(1.5))
    assembly.add_prompt("Pull Horizontal Location",'DISTANCE',bp_unit.inch(2))

def add_countertop_prompts(assembly):
    assembly.add_prompt("Add Backsplash",'CHECKBOX',True)
    assembly.add_prompt("Add Left Backsplash",'CHECKBOX',False)
    assembly.add_prompt("Add Right Backsplash",'CHECKBOX',False)
    assembly.add_prompt("Side Splash Setback",'DISTANCE',bp_unit.inch(2.75))
    assembly.add_prompt("Deck Thickness",'DISTANCE',bp_unit.inch(1.5))
    assembly.add_prompt("Splash Thickness",'DISTANCE',bp_unit.inch(.75))    

def add_carcass_prompts(assembly):
    assembly.add_prompt("Left Finished End",'CHECKBOX',False)
    assembly.add_prompt("Right Finished End",'CHECKBOX',False)
    assembly.add_prompt("Run Sides to Floor",'CHECKBOX',True)
    assembly.add_prompt("Toe Kick Height",'DISTANCE',bp_unit.inch(4))
    assembly.add_prompt("Toe Kick Setback",'DISTANCE',bp_unit.inch(3.25))
    assembly.add_prompt("Material Thickness",'DISTANCE',bp_unit.inch(.75))    
    assembly.add_prompt("Boolean Overhang",'DISTANCE',bp_unit.inch(1))  
