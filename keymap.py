# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

from typing import Any

import bpy
from bpy.types import (KeyMap,
                       KeyMapItem
                      )

addon_keymaps: list[tuple[KeyMap,KeyMapItem]] = []

def add_kmi(km_name: str, kmi_op_idname: str, kmi_type, kmi_value, kmi_any=False, kmi_shift=0, kmi_ctrl=0, kmi_alt=0, kmi_oskey=0, kmi_key_modifier='NONE', kmi_direction='ANY', kmi_repeat=False, kmi_head=False, km_space_type='EMPTY', km_region_type:str='WINDOW', km_modal=False, km_tool=False):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name=km_name, space_type=km_space_type, region_type=km_region_type, modal=km_modal, tool=km_tool)
    kmi = km.keymap_items.new(idname=kmi_op_idname, type=kmi_type, value=kmi_value, any=kmi_any, shift=kmi_shift, ctrl=kmi_ctrl, alt=kmi_alt, oskey=kmi_oskey, key_modifier=kmi_key_modifier, direction=kmi_direction, repeat=kmi_repeat, head=kmi_head)
    addon_keymaps.append((km, kmi))

def remove_keymaps():
    for km, kmi in addon_keymaps:
        bpy.context.window_manager.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

def register():
    add_kmi(
        km_name='Object Mode',
        kmi_op_idname='hide.hide',
        kmi_type='H',
        kmi_value='PRESS',
        km_space_type='EMPTY'
    )
    add_kmi(
        km_name='Outliner',
        kmi_op_idname='hide.hide',
        kmi_type='H',
        kmi_value='PRESS',
        km_space_type='OUTLINER'
    )

def unregister():
    remove_keymaps()