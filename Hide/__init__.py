from . import (operators,
               keymap,
              )
from .ui import (preferences,
              )

bl_info = {
    "name": "Hide",
    "description": "Hide/Unhide using H.",
    "author": "Antoine Danion",
    "version": (1, 1, 1),
    "blender": (4, 2, 1),
    "location": "",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "",
    "tracker_url": "https://github.com/antoinedanion/Blender-Hide/issues",
    "support": "COMMUNITY",
    "category": "3D View",
}

classes = ()

modules = (
    operators,
    preferences,
    keymap,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    for mod in modules:
        mod.register()

    preferences.load_preferences_from_file()

def unregister():
    preferences.export_preferences_to_file()

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    for mod in reversed(modules):
        mod.unregister()

if __name__ == "__main__":
    register()