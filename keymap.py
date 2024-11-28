# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

from typing import Any, Iterable

import bpy
from bpy.types import (KeyMap,
                       KeyMapItem
                      )
from bpy.props import IntProperty

from .constants import (OP_IDNAME_PREFIX,
                        DEFAULT_KMI_LIST,
                       )

addon_keymaps: list[tuple[KeyMap,KeyMapItem]] = []

def get_user_keymapitems(internal_only = False, internal_id: int | None = None):
    def _append_kmi(list: list[Any], km: KeyMap, kmi: KeyMapItem):
        try:
            if kmi in list[km.name]:
                found = True
            else :
                found = False
        except:
            found = False
        if found == False:
            list.setdefault(km.name, []).append(kmi)
    
    user_keymaps: dict[str, list[KeyMapItem]] = {}

    wm = bpy.context.window_manager
    user_kc = wm.keyconfigs.user

    if user_kc is None:
        print("No user keyconfig found.")
        return user_keymaps
    
    km: KeyMap
    for km in user_kc.keymaps:
        kmi: KeyMapItem
        for kmi in km.keymap_items:
            if kmi.idname.startswith( OP_IDNAME_PREFIX + '.'):
                if internal_id != None and internal_only == False:
                    try:
                        if kmi.properties.internal_id == internal_id:
                            _append_kmi(user_keymaps, km, kmi)
                    except:
                        pass

                elif internal_id != None and internal_only == True:
                    try:
                        if kmi.properties.internal_id == internal_id and kmi.properties.internal_id != 0:
                            _append_kmi(user_keymaps, km, kmi)
                    except:
                        pass

                elif internal_id == None and internal_only == False:
                    _append_kmi(user_keymaps, km, kmi)

                elif internal_id == None and internal_only == True:
                    try:
                        if kmi.properties.internal_id != 0:
                            _append_kmi(user_keymaps, km, kmi)
                    except:
                        pass

    return user_keymaps

def get_user_keymapitem_parms(km: KeyMap, kmi: KeyMapItem):
    parms = {
        'km_name' : km.name,
        'kmi_op_idname' : kmi.idname,
        'kmi_type' : kmi.type,
        'kmi_value' : kmi.value,
        'kmi_any' : kmi.any,
        'kmi_shift' : kmi.shift,
        'kmi_ctrl' : kmi.ctrl,
        'kmi_alt' : kmi.alt,
        'kmi_oskey' : kmi.oskey,
        'kmi_key_modifier' : kmi.key_modifier,
        'kmi_direction' : kmi.direction,
        'kmi_repeat' : kmi.repeat,
        'kmi_head' : False,
        'km_space_type' : km.space_type,
        'km_region_type' : km.region_type,
        'km_modal' : km.is_modal,
        'km_tool' : False,
        'kmi_active' : kmi.active,
    }

    return parms

def get_default_keymapitems():
    result: dict[str, list[int]] = {}
    for kmi_def in DEFAULT_KMI_LIST:
        result.setdefault(kmi_def['parms']['km_name'], []).append(kmi_def['id'])
    return result

def get_default_kmi_def_from_id(id: int):
    result = None

    for kmi_def in DEFAULT_KMI_LIST:
        if kmi_def['id'] == id:
            result = kmi_def
            break

    return result

def create_kmi(km_name, kmi_op_idname, kmi_type, kmi_value, kmi_any, kmi_shift, kmi_ctrl, kmi_alt, kmi_oskey, kmi_key_modifier, kmi_direction, kmi_repeat, kmi_head, km_space_type, km_region_type, km_modal, km_tool) -> tuple[KeyMap, KeyMapItem]:
    if bpy.context.window_manager:
        wm = bpy.context.window_manager
        if wm.keyconfigs.addon:
            addon_kc = wm.keyconfigs.addon
            km = addon_kc.keymaps.new(name=km_name, space_type=km_space_type, region_type=km_region_type, modal=km_modal, tool=km_tool)
            kmi = km.keymap_items.new(idname=kmi_op_idname, type=kmi_type, value=kmi_value, any=kmi_any, shift=kmi_shift, ctrl=kmi_ctrl, alt=kmi_alt, oskey=kmi_oskey, key_modifier=kmi_key_modifier, direction=kmi_direction, repeat=kmi_repeat, head=kmi_head)
            return (km, kmi)
        
def add_kmi(internal_id: int, km_name: str, kmi_op_idname: str, kmi_type, kmi_value, kmi_any=False, kmi_shift=0, kmi_ctrl=0, kmi_alt=0, kmi_oskey=0, kmi_key_modifier='NONE', kmi_direction='ANY', kmi_repeat=False, kmi_head=False, km_space_type='EMPTY', km_region_type:str='WINDOW', km_modal=False, km_tool=False, kmi_active: bool = True):
    kmi_tuple = create_kmi(km_name, kmi_op_idname, kmi_type, kmi_value, kmi_any, kmi_shift, kmi_ctrl, kmi_alt, kmi_oskey, kmi_key_modifier, kmi_direction, kmi_repeat, kmi_head, km_space_type, km_region_type, km_modal, km_tool)
    kmi_tuple[1].properties.internal_id = internal_id
    kmi_tuple[1].active = kmi_active
    
    addon_keymaps.append(kmi_tuple)

    print(f'KeyMapItem added : "Addon" - "{km_name}" - [{kmi_op_idname}] - "{kmi_type}"')

def add_default_keymaps(id_list: Iterable[int] | None = None):
    if id_list:
        for kmi_def in DEFAULT_KMI_LIST:
            if kmi_def['id'] in id_list:
                add_kmi(kmi_def['id'], **kmi_def['parms'])
    else:
        for kmi_def in DEFAULT_KMI_LIST:
            add_kmi(kmi_def['id'], **kmi_def['parms'])

def remove_addon_keymapitems():
    for km, kmi in addon_keymaps:
        km_name = km.name
        kmi_idname = kmi.idname
        kmi_type = kmi.type

        km.keymap_items.remove(kmi)

        print(f'KeyMapItem removed : "Addon" - "{km_name}" - [{kmi_idname}] - "{kmi_type}"')
        
    addon_keymaps.clear()

def remove_user_keymapitems(internal_only=False):
    user_keymapitems = get_user_keymapitems(internal_only=internal_only)

    for km_name in user_keymapitems:
        wm = bpy.context.window_manager
        user_kc = wm.keyconfigs.user
        km = user_kc.keymaps[km_name]
        for kmi in user_keymapitems[km_name]:
            kmi_idname = kmi.idname
            kmi_type = kmi.type

            km.keymap_items.remove(kmi)

            print(f'KeyMapItem removed : "User" - "{km_name}" - [{kmi_idname}] - "{kmi_type}"')

class AddDefaultKeymapitem(bpy.types.Operator):
    bl_idname = OP_IDNAME_PREFIX + "." + "adddefaultkeymapitem"
    bl_label = "Hide - Add Default KeyMapItem"
    bl_description = ""
    bl_options = {"UNDO", "INTERNAL"}

    internal_id : IntProperty(
        name='internal_id',
        options = {"HIDDEN"}
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - Add Default KeyMapItem - execute')

        add_default_keymaps(id_list=[self.internal_id,])

        return {"FINISHED"}

classes = (
    AddDefaultKeymapitem,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    remove_addon_keymapitems()

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)