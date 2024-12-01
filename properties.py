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
        name = 'id'
    ) # type: ignore

class HideSceneProperties(bpy.types.PropertyGroup):
    previous_sel : CollectionProperty(
        type = IDItem,
        name = 'previous_sel'
    ) # type: ignore

def init_addon_props():
    bpy.types.Scene.hide = PointerProperty(
        type = HideSceneProperties,
        name = 'hide'
    )

def del_addon_props():
    del bpy.types.Scene.hide

classes = (
    IDItem,
    HideSceneProperties,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    init_addon_props()

def unregister():
    del_addon_props()

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)