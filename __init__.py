import bpy
from baeacs_meshes import meshes

bl_info = { # add-on info
    "name": "baeacs meshes",
    "author": "baeac",
    "version" : (1, 1),
    "blender" : (3, 4, 0),
    "location" : "View3D > baeac",
    "category" : "Create mesh",
    "description" : "Create iterated mesh,, more like irritated mesh!!! (i hate myself)",
}

def register():
    meshes.register()

def unregister():
    meshes.unregister()
 
if __name__ == "__main__":
    register()