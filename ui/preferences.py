import bpy
from bpy.types import AddonPreferences
from bpy.props import (EnumProperty,
                      )
import rna_keymap_ui

class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__.split('.')[0]

    hide_method: EnumProperty(
        name = "Hide method",
        items = [
            ('HIDEINVIEWPORT', 'Hide in Viewport', 'Temporarily hide in viewport'),
            ('DISABLEINVIEWPORTS', 'Disable in Viewports', 'Globally disable in viewports'),
            ('DISABLEINRENDERS', 'Disable in Renders', 'Globally disable in renders'),
        ],
        description = 'The method that will be used to hide objects and collections',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "hide_method")

classes = (ExampleAddonPreferences,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)