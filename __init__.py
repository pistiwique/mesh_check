'''
Copyright (C) 2016 Pistiwique

Created by Pistiwique

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {"name": "Mesh Check BGL edition",
        "description": "Display the triangles and ngons of the mesh",
        "author": "Pistiwique",
        "version": (1, 0, 0),
        "blender": (2, 75, 0),
        "location": "3D View(s) -> Properties -> Shading",
        "category": "3D View"
        }



import bpy
from . mesh_check import *


# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())



# register
##################################

import traceback

def register():
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))
    
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.mesh_check = bpy.props.PointerProperty(
        type=MeshCheckCollectionGroup)
    bpy.types.VIEW3D_PT_view3d_shading.append(displayMeshCheckPanel)
    if mesh_check_handle:
        bpy.types.SpaceView3D.draw_handler_remove(mesh_check_handle[0], 'WINDOW')
    mesh_check_handle[:] = [bpy.types.SpaceView3D.draw_handler_add(mesh_check_draw_callback, (), 'WINDOW', 'POST_VIEW')]
    

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))
    
    bpy.types.VIEW3D_PT_view3d_shading.remove(displayMeshCheckPanel)
    del bpy.types.WindowManager.mesh_check
    if mesh_check_handle:
        bpy.types.SpaceView3D.draw_handler_remove(mesh_check_handle[0], 'WINDOW')
        mesh_check_handle[:] = []
    
