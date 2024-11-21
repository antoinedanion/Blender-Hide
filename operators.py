# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

from typing import Any, Iterable

import bpy
from bpy.types import ID, Object, Collection, LayerCollection
from bpy.props import BoolProperty

from .constants import (ADDON_NAME,
                        OP_IDNAME_PREFIX,
                       )

def get_sel() -> dict[str, ID]:
    # Docs used
    # https://blender.stackexchange.com/questions/203729/python-get-selected-objects-in-outliner Check bl_rna.identifier
    # https://blender.stackexchange.com/questions/325004/how-can-i-get-the-currently-selected-objects-in-the-outliner-if-they-are-hidden Override the context
    # https://blender.stackexchange.com/questions/326453/cant-get-proper-context-selected-ids-from-3d-view DO NOT copy the entire context

    sel_objects = {}

    if bpy.context.area.type != 'OUTLINER':
        override_context = {}
        area = [area for area in bpy.context.screen.areas if area.type == "OUTLINER"][0]
        override_context['area'] = area
        override_context['region'] = area.regions[-1]
    
        with bpy.context.temp_override(**override_context):
            sync: bool = bpy.context.area.spaces[0].use_sync_select
        if sync == True:
            with bpy.context.temp_override(**override_context):
                sel: Iterable[ID] = bpy.context.selected_ids
        else:
            sel: Iterable[ID] = bpy.context.selected_ids
    else:
        sel: Iterable[ID] = bpy.context.selected_ids

    for id in sel:
        if id.bl_rna.identifier == 'Collection':
            sel_objects.setdefault('Collections', []).append(id)
        elif id.bl_rna.identifier == 'Object':
            sel_objects.setdefault('Objects', []).append(id)

    return sel_objects

def get_sel_collections() -> tuple[Collection]:
    ids = []
    sel = get_sel()
    try:
        ids = sel['Collections']
    except:
        pass

    return tuple(ids)

def get_sel_layer_collections() -> tuple[LayerCollection]:
    layer_collections = []
    for layer_collection in bpy.context.view_layer.layer_collection.children:
        if layer_collection.collection in get_sel_collections():
            layer_collections.append(layer_collection)

    return tuple(layer_collections)

def get_sel_objects() -> tuple[Object]:
    ids = []
    sel = get_sel()
    try:
        ids = sel['Objects']
    except:
        pass
    return tuple(ids)

def get_sel_global_state_hide_viewport() -> bool | None:
    # https://blender.stackexchange.com/questions/155563/how-to-hide-a-collection-in-viewport-but-not-disable-in-viewport-via-script
    global_state = None

    sel_layer_collections: tuple[LayerCollection] = get_sel_layer_collections()
    if len(sel_layer_collections) > 0:
        layer_collections_global_state = sel_layer_collections[0].hide_viewport
        for layer_collection in sel_layer_collections[1:]:
            if layer_collections_global_state != layer_collection.hide_viewport:
                layer_collections_global_state = None
    
    sel_objects: list[Object] = get_sel_objects()
    if len(sel_objects) > 0:
        objects_global_state = sel_objects[0].hide_get()
        for id in sel_objects[1:]:
            if objects_global_state != id.hide_get():
                objects_global_state = None

    if len(sel_layer_collections) > 0 and len(sel_objects) > 0:
        if layer_collections_global_state == objects_global_state:
            global_state = layer_collections_global_state
        else:
            global_state = None
    elif len(sel_layer_collections) > 0:
        global_state = layer_collections_global_state
    elif len(sel_objects) > 0:
        global_state = objects_global_state

    return global_state

def get_sel_global_state_disable_viewport() -> bool | None:
    ids: list[Object, Collection] = get_sel_collections() + get_sel_objects()
    global_state = ids[0].hide_viewport
    for id in ids[1:]:
        if global_state != id.hide_viewport:
            global_state = None

    return global_state

def get_sel_global_state_disable_render() -> bool | None:
    ids: list[Object, Collection] = get_sel_collections() + get_sel_objects()
    global_state = ids[0].hide_render
    for id in ids[1:]:
        if global_state != id.hide_render:
            global_state = None

    return global_state

class HideInViewport(bpy.types.Operator):
    bl_idname = OP_IDNAME_PREFIX + "." + "hideinviewport"
    bl_label = "Hide - Hide in viewport"
    bl_description = "Temporarily hide in viewport."
    bl_options = {"UNDO", "INTERNAL"}

    internal : BoolProperty(
        name = 'internal',
        default = False
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - HideViewport - execute')

        global_state = get_sel_global_state_hide_viewport()

        sel_layer_collections: tuple[LayerCollection] = get_sel_layer_collections()
        if len(sel_layer_collections) > 0:
            if global_state == None or global_state == False:
                for layer_collection in sel_layer_collections:
                    layer_collection.hide_viewport = True
            else:
                for layer_collection in sel_layer_collections:
                    layer_collection.hide_viewport = False

        sel_objects: list[Object] = get_sel_objects()
        if len(sel_objects) > 0:
            if global_state == None or global_state == False:
                for obj in sel_objects:
                    obj.hide_set(True)
            else:
                for obj in sel_objects:
                    obj.hide_set(False)
                    obj.select_set(True)

        return {"FINISHED"}

class DisableInViewports(bpy.types.Operator):
    bl_idname = OP_IDNAME_PREFIX + "." + "disableinviewports"
    bl_label = "Hide - Disable in viewport"
    bl_description = "Disable in viewport."
    bl_options = {"UNDO", "INTERNAL"}

    internal : BoolProperty(
        name = 'internal',
        default = False
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - DisableViewport - execute')

        ids: list[Object, Collection] = get_sel_collections() + get_sel_objects()
        if len(ids) > 0:
            global_state = get_sel_global_state_disable_viewport()
            if global_state == None or global_state == False:
                for id in ids:
                    id.hide_viewport = True
            else:
                for id in ids:
                    id.hide_viewport = False
                    if id.bl_rna.identifier == 'Object':
                        id.select_set(True)

        return {"FINISHED"}

class DisableInRenders(bpy.types.Operator):
    bl_idname = OP_IDNAME_PREFIX + "." + "disableinrenders"
    bl_label = "Hide - Disable in render"
    bl_description = "Disable in render."
    bl_options = {"UNDO", "INTERNAL"}

    internal : BoolProperty(
        name = 'internal',
        default = False
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - DisableRender - execute')

        ids: list[Object, Collection] = get_sel_collections() + get_sel_objects()
        if len(ids) > 0:
            global_state = get_sel_global_state_disable_render()
            if global_state == None or global_state == False:
                for id in ids:
                    id.hide_render = True
            else:
                for id in ids:
                    id.hide_render = False
                    if id.bl_rna.identifier == 'Object':
                        id.select_set(True)

        return {"FINISHED"}

class Hide(bpy.types.Operator):
    bl_idname = OP_IDNAME_PREFIX + "." + "hide"
    bl_label = "Hide - Hide"
    bl_description = "Hide the selection"
    bl_options = {"UNDO", "INTERNAL"}

    internal : BoolProperty(
        name = 'internal',
        default = False
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - Hide - execute')

        addon_prefs = bpy.context.preferences.addons[ADDON_NAME].preferences
        hide_method = addon_prefs.hide_method

        if hide_method == 'HIDEINVIEWPORT':
            bpy.ops.hide.hideinviewport()
        elif hide_method == 'DISABLEINVIEWPORTS':
            bpy.ops.hide.disableinviewports()
        elif hide_method == 'DISABLEINRENDERS':
            bpy.ops.hide.disableinrenders()

        return {"FINISHED"}


classes = (
    HideInViewport,
    DisableInViewports,
    DisableInRenders,
    Hide,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)