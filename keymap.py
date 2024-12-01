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

def get_user_keymapitems(internal_only = False, internal_id: int | None = None) -> dict[str, list[KeyMapItem]]:
    """
    Retrieve user keymap items based on internal ID and filtering criteria.

    Parameters
    ----------
    internal_only : bool, optional
        If True, only include internal keymap items. Default is False.
    internal_id : int, optional
        Internal ID to filter keymap items by. Default is None.

    Returns
    -------
    dict
        A dictionary where keys are keymap names, and values are lists of KeyMapItems.
    """

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

def get_user_keymapitem_parms(km: KeyMap, kmi: KeyMapItem) -> dict[str, Any]:
    """
    Retrieve parameters of a keymap item.

    Parameters
    ----------
    km : KeyMap
        The KeyMap object containing the KeyMapItem.
    kmi : KeyMapItem
        The KeyMapItem whose parameters need to be extracted.

    Returns
    -------
    dict
        Dictionary of KeyMapItem parameters.
    """

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

def get_default_keymapitems() -> dict[str, list[int]]:
    """
    Retrieve default keymap items internal IDs defined in the addon.

    Returns
    -------
    dict
        A dictionary where keys are keymap names and values are lists of IDs for default KeyMapItems.
    """

    result: dict[str, list[int]] = {}
    for kmi_def in DEFAULT_KMI_LIST:
        result.setdefault(kmi_def['parms']['km_name'], []).append(kmi_def['id'])
    return result

def get_default_kmi_def_from_id(id: int) -> dict[str, Any] | None:
    """
    Retrieve a default keymap item definition by its ID.

    Parameters
    ----------
    id : int
        The internal ID of the keymap item to retrieve.

    Returns
    -------
    dict or None
        The keymap item definition if found, otherwise None.
    """

    result: dict[str, Any] | None = None

    for kmi_def in DEFAULT_KMI_LIST:
        if kmi_def['id'] == id:
            result = kmi_def
            break

    return result

def create_kmi(km_name, kmi_op_idname, kmi_type, kmi_value, kmi_any, kmi_shift, kmi_ctrl, kmi_alt, kmi_oskey, kmi_key_modifier, kmi_direction, kmi_repeat, kmi_head, km_space_type, km_region_type, km_modal, km_tool) -> tuple[KeyMap, KeyMapItem] | None:
    """
    Create a new KeyMapItem in the addon key configuration.

    Parameters
    ----------
    km_name : str
        Name of the KeyMap.
    kmi_op_idname : str
        IDName of the operator.
    kmi_type : str
        Type of key input (e.g., 'A').
    kmi_value : str
        Value of the key event (e.g., 'PRESS').
    kmi_any : bool
        If True, any key modifier is allowed.
    kmi_shift : bool
        If True, Shift must be held.
    kmi_ctrl : bool
        If True, Ctrl must be held.
    kmi_alt : bool
        If True, Alt must be held.
    kmi_oskey : bool
        If True, the OS key must be held.
    kmi_key_modifier : str
        Modifier key type (e.g., 'NONE').
    kmi_direction : str
        Direction of input (e.g., 'ANY').
    kmi_repeat : bool
        If True, key repeat is allowed.
    kmi_head : bool
        If True, the item is a head item.
    km_space_type : str
        Space type for the KeyMap.
    km_region_type : str
        Region type for the KeyMap.
    km_modal : bool
        Whether the KeyMap is modal.
    km_tool : bool
        Whether the KeyMap is for a specific tool.

    Returns
    -------
    tuple or None
        The created KeyMap and KeyMapItem if addon keyconfig is found, otherwise None.
    """
    
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        addon_kc = wm.keyconfigs.addon
        km = addon_kc.keymaps.new(name=km_name, space_type=km_space_type, region_type=km_region_type, modal=km_modal, tool=km_tool)
        kmi = km.keymap_items.new(idname=kmi_op_idname, type=kmi_type, value=kmi_value, any=kmi_any, shift=kmi_shift, ctrl=kmi_ctrl, alt=kmi_alt, oskey=kmi_oskey, key_modifier=kmi_key_modifier, direction=kmi_direction, repeat=kmi_repeat, head=kmi_head)
        return (km, kmi)
    else:
        print('WARNING : Blender Addon keyconfig was not found')
        return None
        
def add_kmi(internal_id: int, km_name: str, kmi_op_idname: str, kmi_type, kmi_value, kmi_any=False, kmi_shift=0, kmi_ctrl=0, kmi_alt=0, kmi_oskey=0, kmi_key_modifier='NONE', kmi_direction='ANY', kmi_repeat=False, kmi_head=False, km_space_type='EMPTY', km_region_type:str='WINDOW', km_modal=False, km_tool=False, kmi_active: bool = True) -> None:
    """
    Add a new KeyMapItem to the addon keymaps list.

    Parameters
    ----------
    internal_id : int
        The internal ID associated with the KeyMapItem.
    km_name : str
        Name of the KeyMap to which the KeyMapItem belongs.
    kmi_op_idname : str
        IDName of the operator for the KeyMapItem.
    kmi_type : str
        Key type (e.g., 'A').
    kmi_value : str
        Key event value (e.g., 'PRESS').
    kmi_any : bool, optional
        If True, any modifier key is allowed. Default is False.
    kmi_shift : bool, optional
        If True, Shift must be held. Default is 0.
    kmi_ctrl : bool, optional
        If True, Ctrl must be held. Default is 0.
    kmi_alt : bool, optional
        If True, Alt must be held. Default is 0.
    kmi_oskey : bool, optional
        If True, the OS key must be held. Default is 0.
    kmi_key_modifier : str, optional
        Modifier key type (e.g., 'NONE'). Default is 'NONE'.
    kmi_direction : str, optional
        Direction of the key input (e.g., 'ANY'). Default is 'ANY'.
    kmi_repeat : bool, optional
        If True, key repeat is allowed. Default is False.
    kmi_head : bool, optional
        If True, the item is a head item. Default is False.
    km_space_type : str, optional
        Space type for the KeyMap. Default is 'EMPTY'.
    km_region_type : str, optional
        Region type for the KeyMap. Default is 'WINDOW'.
    km_modal : bool, optional
        Whether the KeyMap is modal. Default is False.
    km_tool : bool, optional
        Whether the KeyMap is for a specific tool. Default is False.
    kmi_active : bool, optional
        Whether the KeyMapItem is active. Default is True.

    Returns
    -------
    None
    """

    kmi_tuple = create_kmi(km_name, kmi_op_idname, kmi_type, kmi_value, kmi_any, kmi_shift, kmi_ctrl, kmi_alt, kmi_oskey, kmi_key_modifier, kmi_direction, kmi_repeat, kmi_head, km_space_type, km_region_type, km_modal, km_tool)
    if kmi_tuple != None:
        kmi_tuple[1].properties.internal_id = internal_id
        kmi_tuple[1].active = kmi_active
        
        addon_keymaps.append(kmi_tuple)

        print(f'KeyMapItem added : "Addon" - "{km_name}" - [{kmi_op_idname}] - "{kmi_type}"')
    else:
        print(f'WARNING : Failed to add KeyMapItem : "Addon" - "{km_name}" - [{kmi_op_idname}] - "{kmi_type}"')

def add_default_keymaps(id_list: Iterable[int] | None = None) -> None:
    """
    Adds default KeyMapItems to the addon keymaps.

    Parameters
    ----------
    id_list : Iterable[int] | None, optional
        A list of internal IDs for the KeyMapItems to add. If None, all default KeyMapItems are added.

    Returns
    -------
    None
    """

    if id_list:
        for kmi_def in DEFAULT_KMI_LIST:
            if kmi_def['id'] in id_list:
                add_kmi(kmi_def['id'], **kmi_def['parms'])
    else:
        for kmi_def in DEFAULT_KMI_LIST:
            add_kmi(kmi_def['id'], **kmi_def['parms'])

def remove_addon_keymapitems() -> None:
    """
    Remove all KeyMapItems added by the addon from the keymaps.

    Returns
    -------
    None
    """

    for km, kmi in addon_keymaps:
        km_name = km.name
        kmi_idname = kmi.idname
        kmi_type = kmi.type

        km.keymap_items.remove(kmi)

        print(f'KeyMapItem removed : "Addon" - "{km_name}" - [{kmi_idname}] - "{kmi_type}"')
        
    addon_keymaps.clear()

def remove_user_keymapitems(internal_only=False) -> None:
    """
    Removes user-defined KeyMapItems from the user keymaps.

    Parameters
    ----------
    internal_only : bool, optional
        If True, only removes KeyMapItems marked as internal. Default is False.

    Returns
    -------
    None
    """

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
    """
    Operator for adding specific Keymapitem.
    """

    bl_idname = OP_IDNAME_PREFIX + "." + "adddefaultkeymapitem"
    bl_label = "Hide - Add Default KeyMapItem"
    bl_description = ""
    bl_options = {"UNDO", "INTERNAL"}

    internal_id : IntProperty(
        name='internal_id',
        options = {"HIDDEN"}
    ) # type: ignore

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