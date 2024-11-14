# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

import os, json

import bpy
from bpy.types import AddonPreferences, KeyMap, KeyMapItem
from bpy.props import EnumProperty
import rna_keymap_ui

from .constants import (PREFS_FILEPATH,
                         PREFS_DIR,
                         ADDON_NAME
                        )

from .keymap import get_user_keymaps

def get_addon_prefs():
    preferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    prefs_values = {}
    for key in preferences.__annotations__.keys():
        k = getattr(preferences, key)
        if str(type(k)) == "<class 'bpy_prop_array'>":
            prefs_values[key] = k[:]
        else:
            prefs_values[key] = k
    return prefs_values

def set_addon_prefs(prefs_values):
    preferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    for key in preferences.__annotations__.keys():
        value = prefs_values[key]
        setattr(preferences, key, value)

def export_preferences_to_file():
    prefs_values = get_addon_prefs()
    
    if prefs_values:
        json_data = json.dumps(prefs_values, indent=4)
        
        # Write the JSON data to a file
        if os.path.exists(PREFS_DIR) == False:
            os.makedirs(PREFS_DIR)
        with open(PREFS_FILEPATH, 'w') as file:
            file.write(json_data)

        print(f'Preferences successfully saved to "{PREFS_FILEPATH}"')

def load_preferences_from_file():
    try:
        with open(PREFS_FILEPATH, 'r') as file:
            prefs_values = json.load(file)
            set_addon_prefs(prefs_values)

        print(f'Preferences successfully loaded from "{PREFS_FILEPATH}"')
    except:
        prefs_values = None

        print(f'Failed to loade preferences"')

class HidePreferences(AddonPreferences):
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
        default='DISABLEINVIEWPORTS',
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "hide_method")

        layout.separator()

        hotkeys_box = layout.box()
        hotkeys_col = hotkeys_box.column()
        hotkeys_col.label(text="Hotkeys:")
        hotkeys_col.separator()
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        user_keymaps = get_user_keymaps()
        for km_name in user_keymaps:
            hotkeys_col.label(text=f"•   {km_name}")
            km: KeyMap = kc.keymaps[km_name]
            for kmi in user_keymaps[km_name]:
                hotkeys_col.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, hotkeys_col, 0)
            hotkeys_col.separator()


classes = (HidePreferences,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)