# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

from . import (
    properties,
    operators,
    preferences,
    keymap,
)

classes = ()

modules = (
    properties,
    operators,
    preferences,
    keymap,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    for mod in modules:
        try:
            mod.register()
            print(f'{mod.__name__} registered successfully.')
        except:
            print(f'Failed to register module : {mod.__name__}')

    preferences.load_preferences_from_file()

def unregister():
    preferences.export_preferences_to_file()

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    for mod in reversed(modules):
        try:
            mod.unregister()
            print(f'{mod.__name__} unregistered successfully.')
        except:
            print(f'Failed to unregister module : {mod.__name__}')

if __name__ == "__main__":
    register()