import os, json

import bpy
from bpy.types import AddonPreferences
from bpy.props import EnumProperty

from ..constants import (PREFS_FILEPATH,
                         PREFS_DIR,
                         ADDON_NAME
                        )

def get_scene_prefs():
    preferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    prefs_values = {}
    for key in preferences.__annotations__.keys():
        k = getattr(preferences, key)
        if str(type(k)) == "<class 'bpy_prop_array'>":
            prefs_values[key] = k[:]
        else:
            prefs_values[key] = k
    return prefs_values

def set_scene_prefs(prefs_values):
    preferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    for key in preferences.__annotations__.keys():
        value = prefs_values[key]
        setattr(preferences, key, value)

def export_preferences_to_file():
    prefs_values = get_scene_prefs()
    
    if prefs_values:
        json_data = json.dumps(prefs_values, indent=4)
        
        # Write the JSON data to a file
        if os.path.exists(PREFS_DIR) == False:
            os.makedirs(PREFS_DIR)
        with open(PREFS_FILEPATH, 'w') as file:
            file.write(json_data)

def load_preferences_from_file():
    try:
        with open(PREFS_FILEPATH, 'r') as file:
            prefs_values = json.load(file)
    except:
        prefs_values = None

    set_scene_prefs(prefs_values)


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