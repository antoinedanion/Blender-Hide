# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

import os, json
from typing import Any

import bpy
from bpy.types import AddonPreferences, KeyMap, KeyMapItem
from bpy.props import (
    EnumProperty,
    IntProperty,
)
import rna_keymap_ui

from .constants import (
    PREFS_FILEPATH,
    PREFS_DIR,
    ADDON_NAME,
    OP_IDNAME_PREFIX,
)
from .keymap import (
    get_user_kmis,
    get_user_kmi_parms,
    add_addon_kmi,
    add_default_keymaps,
    get_default_kmi_def_from_id,
    get_default_kmis,
)

def get_addon_prefs() -> dict[str, Any]:
    """
    Retrieves the current addon preferences and user-defined keymaps.

    Returns
    -------
    dict[str, Any]
        A dictionary containing addon preferences and keymaps.
    """

    prefs_values = {'preferences': {},
                    'keymaps': {},
    }

    # Preferences
    preferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    for key in preferences.__annotations__.keys():
        k = getattr(preferences, key)
        if str(type(k)) == "<class 'bpy_prop_array'>":
            prefs_values['preferences'][key] = k[:]
        else:
            prefs_values['preferences'][key] = k
    
    # Keymaps
    user_keymapitems = get_user_kmis(internal_only = True)
    if user_keymapitems:
        wm = bpy.context.window_manager
        user_kc = wm.keyconfigs.user
        for km_name in user_keymapitems:
            km = user_kc.keymaps[km_name]
            km_kmis = []
            for kmi in user_keymapitems[km_name]:
                kmi_def = {
                    'id' : kmi.properties.internal_id,
                    'parms' : get_user_kmi_parms(km, kmi),
                }
                km_kmis.append(kmi_def)
            prefs_values['keymaps'][km.name] = km_kmis

    return prefs_values

def set_addon_prefs(prefs_values, preferences: bool = True, keymaps: bool = True) -> None:
    """
    Sets addon preferences and user-defined keymaps from the provided values.

    Parameters
    ----------
    prefs_values : dict
        A dictionary containing preferences and keymap definitions.
    preferences : bool, optional
        If True, preferences will be set. Default is True.
    keymaps : bool, optional
        If True, keymaps will be set. Default is True.

    Returns
    -------
    None
    """

    # Preferences
    preferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    for key in preferences.__annotations__.keys():
        value = prefs_values['preferences'][key]
        setattr(preferences, key, value)

    # Keymaps
    if prefs_values['keymaps']:
        for km_name in prefs_values['keymaps']:
            for kmi_def in prefs_values['keymaps'][km_name]:
                add_addon_kmi(kmi_def['id'], **kmi_def['parms'])

def export_preferences_to_file() -> None:
    """
    Exports the current addon preferences and user-defined keymaps to a file.

    Returns
    -------
    None
    """

    prefs_values = get_addon_prefs()
    
    if prefs_values:
        json_data = json.dumps(prefs_values, indent=4)
        
        # Write the JSON data to a file
        if os.path.exists(PREFS_DIR) == False:
            os.makedirs(PREFS_DIR)
        with open(PREFS_FILEPATH, 'w') as file:
            file.write(json_data)

        print(f'Preferences successfully saved to "{PREFS_FILEPATH}"')

def load_preferences_from_file(preferences: bool = True, keymaps: bool = True) -> None:
    """
    Loads addon preferences and user-defined keymaps from a file.

    Parameters
    ----------
    preferences : bool, optional
        If True, preferences will be loaded. Default is True.
    keymaps : bool, optional
        If True, keymaps will be loaded. Default is True.

    Returns
    -------
    None
    """

    try:
        with open(PREFS_FILEPATH, 'r') as file:
            prefs_values = json.load(file)

            set_addon_prefs(prefs_values, preferences=preferences, keymaps=keymaps)

        print(f'Preferences successfully loaded from "{PREFS_FILEPATH}"')

    except FileNotFoundError:
        print(f'Failed to find preferences file, a new one will be created.')
        if keymaps == True:
            add_default_keymaps()

    except:
        print(f'Failed to load preferences')
        if keymaps == True:
            add_default_keymaps()

def reset_preferences() -> None:
    """
    Resets the addon preferences to their default values.

    Returns
    -------
    None
    """
    
    preferences: AddonPreferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    for key in preferences.__annotations__.keys():
        preferences.property_unset(key)

class ResetPreferences(bpy.types.Operator):
    """
    Operator for resetting addon preferences.
    """

    bl_idname = OP_IDNAME_PREFIX + "." + "resetpreferences"
    bl_label = "Hide - Reset preferences"
    bl_description = "Reset the preferences"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - ResetPreferences - execute')

        reset_preferences()

        return {"FINISHED"}

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

class HidePreferences(AddonPreferences):
    """
    Preferences class for the "Hide" addon.
    """

    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = ADDON_NAME

    hide_method: EnumProperty(
        name = "Hide method",
        items = [
            ('HIDEINVIEWPORT', 'Hide in Viewport', 'Temporarily hide in viewport'),
            ('DISABLEINVIEWPORTS', 'Disable in Viewports', 'Globally disable in viewports'),
            ('DISABLEINRENDERS', 'Disable in Renders', 'Globally disable in renders'),
        ],
        description = 'The method that will be used to hide objects and collections',
        default='HIDEINVIEWPORT',
    ) # type: ignore

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "hide_method")

        layout.separator()

        hotkeys_box = layout.box()
        hotkeys_col = hotkeys_box.column()

        hotkeys_title_row = hotkeys_col.row()
        hotkeys_title_row.label(text="Hotkeys:")

        hotkeys_col.separator()

        wm = bpy.context.window_manager
        user_kc = wm.keyconfigs.user
        user_keymaps = get_user_kmis()
        default_keymaps = get_default_kmis()
        keymaps = []
        for km_name in list(user_keymaps.keys()) + list(default_keymaps.keys()):
            if km_name not in keymaps:
                keymaps.append(km_name)

        for km_name in keymaps:
            hotkeys_col.label(text=f"•   {km_name}")
            km: KeyMap = user_kc.keymaps[km_name]
            if km_name in user_keymaps:
                for kmi in user_keymaps[km_name]:
                    hotkeys_col.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi([], user_kc, km, kmi, hotkeys_col, 0)
            if km_name in default_keymaps:
                for kmi_id in default_keymaps[km_name]:
                    if get_user_kmis(internal_id=kmi_id) == {}:
                        kmi_def = get_default_kmi_def_from_id(kmi_id)
                        kmi_op_idname = kmi_def['parms']['kmi_op_idname']
                        hotkeys_col.operator("hide.adddefaultkeymapitem", text=f'Restore default hotkey for {kmi_op_idname}').internal_id = kmi_id
        
        # layout.separator()
        # layout.operator("hide.resetpreferences", text=f'Reset addon preferences')

classes = (
    ResetPreferences,
    AddDefaultKeymapitem,
    HidePreferences,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)