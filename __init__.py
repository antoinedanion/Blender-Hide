from . import operators, keymap

bl_info = {
    "name": "Hide",
    "description": "Disable/Enable any selection in viewport with H.",
    "author": "Antoine Danion",
    "version": (1, 0, 0),
    "blender": (4, 2, 1),
    "location": "",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "3D View",
}

classes = ()

modules = (
    keymap,
    operators,
)

addon_keymaps = []

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    for mod in modules:
        mod.register()

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    for mod in reversed(modules):
        mod.unregister()

if __name__ == "__main__":
    register()