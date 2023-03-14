import bpy # import all the shit i need (i think there's some things i didn't use
import addon_utils
import math
import numpy as np
import mathutils
from bpy.props import EnumProperty, PointerProperty, IntProperty
from bpy.types import Operator, Panel, PropertyGroup, Scene

bl_info = { # add-on info
    "name": "baeacs meshes",
    "author": "baeac",
    "version" : (1, 1),
    "blender" : (3, 4, 0),
    "location" : "View3D > baeac",
    "category" : "Create mesh",
    "description" : "Create iterated mesh,, more like irritated mesh!!! (i hate myself)",
}

precision = 200 # used later for displacing mesh

def enable_addon(addon_module_name):
    loaded_default, loaded_state = addon_utils.check(addon_module_name)
    if not loaded_state:
        addon_utils.enable(addon_module_name)

def enable_extra_meshes():
    enable_addon(addon_module_name="add_mesh_extra_objects")

class BaeacsMeshes_PT_Panel(Panel): # draw panel
    bl_idname = 'BAEACSMESHES_PT_panel'
    bl_label = 'baeacs meshes'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'baeacs meshes'
    
    def draw(self, context): # do the thingies for the buttons and sliders
        layout = self.layout
        temporary = context.scene.temporary
        
        row = layout.row()
        row.prop(temporary, "int_slider", text="Resolution", slider=True) # find out rows make vertical splits, cols horizontal
        layout.operator('baeac.op', text='Add instance')
        col = layout.column()
        col.prop(temporary, "dropdownbox", text="Presets")
        col = layout.column()
        col.prop(temporary, "step_slider", text="Step size", slider=True)
        layout.operator('iterations.op', text='Iterate')
        
class FractalProperties(PropertyGroup): #dropdown box and presets
    dropdownbox: EnumProperty(
        items=(
            ("Preset1", "Mandelblub", "Doesn't even look like a mandelbulb lol"), # intentional spelling error
            ("Preset2", "Spikey Llama", "Fortnite Spikey Llama"),
            ("Preset3", "Ant Emperor", "Generate the last great Ant Emperor"),
            ("Preset4", "Folder", "Generate folded geometry"),
            ("Preset5", "Reefback Whale", "Generate a mesh that looks like the reefbacks from Subnautica"),
        ),
        name="Presets",
        default="Preset1",
        description="Amazing presets with the worst performance!",
    )
    int_slider: IntProperty(name='int value', default=50, soft_min=0, soft_max=200) # resolution slider
    step_slider: IntProperty(name='step value', default=10, soft_min=1, soft_max=10) # iteration step size slider
        
class baeac_OT_op(Operator):
    bl_idname = 'baeac.op'
    bl_label = 'baeacs meshes'
    bl_description = 'baeacs meshes'
    bl_options = {'REGISTER', 'UNDO'}
    
    action: EnumProperty(
        items=[
            ('INSTANCE', 'add instance', 'add instance'),
        ]
    )
    
    def execute(self, context):
        if self.action == 'INSTANCE':
            self.instance(context=context)
            
        return {'FINISHED'}
    
    @staticmethod
    def instance(context):
        slider_value = bpy.context.scene.temporary.int_slider

        bpy.ops.mesh.primitive_round_cube_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), change=False, arc_div=slider_value, lin_div=0, radius=1)
    
class Iterations_OT_op(Operator):
    bl_idname = 'iterations.op'
    bl_label = 'Iterate'
    bl_description = 'Iterate'
    bl_options = {'REGISTER', 'UNDO'}
    
    action: EnumProperty(
        items=[
            ('ITERATE', 'set iterations', 'set iterations'),
        ]
    )
    
    def execute(self, context):
        if self.action == 'ITERATE':
            self.iteration(context=context)
            
        return {'FINISHED'}
    
    @staticmethod
    def iteration(context):
        get_step_size = bpy.context.scene.temporary.step_slider    
            
        vert_coord = bpy.context.active_object.data
        
        if bpy.context.scene.temporary.dropdownbox == 'Preset1': # this has to be the WORST way of doing things...
            for i in range(get_step_size): # if loop, for loop, for loop, while loop...
                for vert in vert_coord.vertices: # maybe using switches? how do they work in python???
                    count = 1
                    
                    x_loc = vert.co[0]
                    y_loc = vert.co[1]
                    z_loc = vert.co[2]
                    
                    mandel_val = (complex(x_loc, y_loc,) ** 2) - z_loc
                    
                    while 0 < abs(mandel_val) < 2 and count < precision:
                        count += 1
                        
                        mandel_val = (mandel_val ** 2) - z_loc
                        
                    vert.co = vert.co * (count ** (1/10) - 0.12)
                    
            bpy.ops.object.shade_smooth()
        elif bpy.context.scene.temporary.dropdownbox == 'Preset2':
            for i in range(get_step_size):
                for vert in vert_coord.vertices:
                    count = 1
                    
                    x_loc = vert.co[0]
                    y_loc = vert.co[1]
                    z_loc = vert.co[2]
                    
                    mandel_val = (complex(x_loc, y_loc) ** 2) - (complex(z_loc, y_loc))
                    
                    while 0 < abs(mandel_val) < 2 and count < precision:
                        count += 1
                        
                        mandel_val = (mandel_val ** 4) - z_loc
                        
                    vert.co = vert.co * (count ** (1/10) - 0.12)
                    
            bpy.ops.object.shade_smooth()
        elif bpy.context.scene.temporary.dropdownbox == 'Preset3':
            for i in range(get_step_size):
                for vert in vert_coord.vertices:
                    count = 2
                    
                    x_loc = vert.co[0]
                    y_loc = vert.co[1]
                    z_loc = vert.co[2]
                    
                    mandel_val = -complex(x_loc, y_loc) ** 2 + z_loc
                    
                    while 0 < abs(mandel_val) < 2 and count < precision:
                        count += 1
                        
                        mandel_val = ((mandel_val ** 2) - z_loc) ** mandel_val
                        
                    vert.co = vert.co * (count ** (1/20) - 0.08)
                
            bpy.ops.object.shade_smooth()
        elif bpy.context.scene.temporary.dropdownbox == 'Preset4':
            for i in range(get_step_size):
                for vert in vert_coord.vertices:
                    count = 2
                    
                    x_loc = vert.co[0]
                    y_loc = vert.co[1]
                    z_loc = vert.co[2]
                    
                    mandel_val = complex(x_loc, y_loc) * math.atan2(x_loc, y_loc) - z_loc
                    
                    while 0 < abs(mandel_val) < 2 and count < precision:
                        count += 1
                        
                        mandel_val = (mandel_val ** 2)
                        
                    vert.co = vert.co * (count ** (1/10) - 0.3)
                
            bpy.ops.object.shade_smooth()
        elif bpy.context.scene.temporary.dropdownbox == 'Preset5':
            for i in range(get_step_size):
                for vert in vert_coord.vertices:
                    count = 2
                    
                    x_loc = vert.co[0]
                    y_loc = vert.co[1]
                    z_loc = vert.co[2]
                    
                    mandel_val = 4 * z_loc + x_loc - y_loc ** 2 # math :sunglasses:
                    
                    while 0 < abs(mandel_val) < 2 and count < precision:
                        count += 1
                        
                        mandel_val = math.sin(x_loc) - z_loc
                        
                    vert.co = vert.co * (count ** (1/20) - 0.12)
                
            bpy.ops.object.shade_smooth()
    
def register(): # register
    bpy.utils.register_class(BaeacsMeshes_PT_Panel)
    bpy.utils.register_class(FractalProperties)
    bpy.utils.register_class(baeac_OT_op)
    bpy.utils.register_class(Iterations_OT_op)

    Scene.temporary = PointerProperty(type=FractalProperties)
    enable_extra_meshes()
 
def unregister(): # unregister
    bpy.utils.unregister_class(Iterations_OT_op)
    bpy.utils.unregister_class(baeac_OT_op)
    bpy.utils.unregister_class(FractalProperties)
    bpy.utils.unregister_class(BaeacsMeshes_PT_Panel)
    
    del Scene.temporary

if __name__ == '__main__':
    register()