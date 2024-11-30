# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

import bpy
from bpy.types import ID
from bpy.props import (
    PointerProperty,
    CollectionProperty,
)

class IDItem(bpy.types.PropertyGroup):
    id : PointerProperty(
        type = ID,
        name = 'ID'
    )

class HideProperties(bpy.types.PropertyGroup):
    previous_sel : CollectionProperty(
        type = IDItem,
        name = 'Previous selection'
    )

def init_addon_props():
    try:
        props = bpy.types.Scene.hide
        print('Hide properties was found attached to the scene')
    except:
        print('No Hide properties was found attached to the scene. Creating new ones')
        bpy.types.Scene.hide = PointerProperty(
            type = HideProperties,
            name = 'Hide properties'
        )

classes = (
    IDItem,
    HideProperties,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    init_addon_props()

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)