# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

from typing import Any, Iterable

import bpy
from bpy.types import ID, Object, Collection, LayerCollection
from bpy.props import IntProperty

from .constants import (ADDON_NAME,
                        OP_IDNAME_PREFIX,
                       )

def get_sel_ids() -> tuple[ID]:
    # Docs used
    # https://blender.stackexchange.com/questions/203729/python-get-selected-objects-in-outliner Check bl_rna.identifier
    # https://blender.stackexchange.com/questions/325004/how-can-i-get-the-currently-selected-objects-in-the-outliner-if-they-are-hidden Override the context
    # https://blender.stackexchange.com/questions/326453/cant-get-proper-context-selected-ids-from-3d-view DO NOT copy the entire context

    sel_ids = []

    # Get context_outliners
    context_outliners: list[dict[str, Any]] | None = []
    outliner_areas = [area for area in bpy.context.screen.areas if area.type == "OUTLINER"]
    if outliner_areas != []:
        for area in outliner_areas:
            context_outliners.append(
                {
                    'parms': {
                        'area' : area,
                        'region' : area.regions[-1],
                    },
                }
            )
    else:
        context_outliners: list[dict[str, Any]] | None = None
        print('No Outliner found')
    
    # Get context_viewports
    context_viewports: list[dict[str, Any]] | None = []
    viewport_areas = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"]
    if viewport_areas != []:
        for area in viewport_areas:
            context_viewports.append(
                {
                    'parms': {
                        'area' : area,
                        'region' : area.regions[-1],
                    },
                }
            )
    else:
        context_viewports: list[dict[str, Any]] | None = None
        print('No Viewport found')

    # Debug
    if context_outliners == None and context_viewports == None:
        print('Neither Outliner nor Viewport was found')
        return tuple(sel_ids)

    # Get sync states
    if context_outliners != None:
        if bpy.context.area.type == 'OUTLINER':
            current_sync: bool | None = bpy.context.area.spaces[0].use_sync_select
        else:
            current_sync: bool | None = None
        for context_outliner in context_outliners:
            with bpy.context.temp_override(**context_outliner['parms']):
                sync: bool = bpy.context.area.spaces[0].use_sync_select
            context_outliner['sync'] = sync

    # Get selected ids
    sel_outliners: Iterable[ID] = []
    sel_viewports: Iterable[ID] = []
    if bpy.context.area.type == 'OUTLINER':
        if current_sync == True:
            for context_outliner in context_outliners:
                if context_outliner['sync'] == True:
                    with bpy.context.temp_override(**context_outliner['parms']):
                        sel_outliners.extend(bpy.context.selected_ids)
            if context_viewports != None:
                for context_viewport in context_viewports:
                    with bpy.context.temp_override(**context_viewport['parms']):
                        sel_viewports.extend(bpy.context.selected_ids)
        else:
            sel_outliners.extend(bpy.context.selected_ids)
    elif bpy.context.area.type == 'VIEW_3D':
        if context_outliners != None:
            for context_outliner in context_outliners:
                if context_outliner['sync'] == True:
                    with bpy.context.temp_override(**context_outliner['parms']):
                        sel_outliners.extend(bpy.context.selected_ids)
        for context_viewport in context_viewports:
            with bpy.context.temp_override(**context_viewport['parms']):
                sel_viewports.extend(bpy.context.selected_ids)
    
    # Remove any duplicate
    sel_ids = set(sel_outliners + sel_viewports)

    # Debug
    if sel_ids == []:
        print('WARNING : Selection is empty')

    return tuple(sel_ids)

def sort_ids_per_type(ids : Iterable[ID]):
    # Sort ids per types
    sorted_ids = {}
    for id in ids:
        sorted_ids.setdefault(id.bl_rna.identifier, []).append(id)
    return sorted_ids

def get_sorted_sel() -> dict[str, ID]:    
    return sort_ids_per_type(get_sel_ids())

def get_sel_collections(sel : Iterable[ID] | None = None) -> tuple[Collection] | None:
    ids = []

    if sel == None:
        sorted_sel = get_sorted_sel()
    else:
        sel = set(sel)
        sorted_sel = sort_ids_per_type(sel)

    try:
        ids = sorted_sel['Collection']
    except:
        pass

    return tuple(ids)

def get_sel_layer_collections(sel : Iterable[ID] | None = None) -> tuple[LayerCollection]:
    layer_collections = []
    for layer_collection in bpy.context.view_layer.layer_collection.children:
        if layer_collection.collection in get_sel_collections(sel):
            layer_collections.append(layer_collection)

    return tuple(layer_collections)

def get_sel_objects(sel : Iterable[ID] | None = None) -> tuple[Object]:
    ids = []

    if sel == None:
        sorted_sel = get_sorted_sel()
    else:
        sel = set(sel)
        sorted_sel = sort_ids_per_type(sel)

    try:
        ids = sorted_sel['Object']
    except:
        pass

    return tuple(ids)

def get_sel_global_state_hide_viewport(sel : Iterable[ID] | None = None) -> bool | None:
    # https://blender.stackexchange.com/questions/155563/how-to-hide-a-collection-in-viewport-but-not-disable-in-viewport-via-script
    global_state = None

    sel_layer_collections: tuple[LayerCollection] = get_sel_layer_collections(sel)
    if len(sel_layer_collections) > 0:
        layer_collections_global_state = sel_layer_collections[0].hide_viewport
        for layer_collection in sel_layer_collections[1:]:
            if layer_collections_global_state != layer_collection.hide_viewport:
                layer_collections_global_state = None
    
    sel_objects: list[Object] = get_sel_objects(sel)
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

def get_sel_global_state_disable_viewport(sel : Iterable[ID] | None = None) -> bool | None:
    ids: list[Object, Collection] = get_sel_collections(sel) + get_sel_objects(sel)
    global_state = ids[0].hide_viewport
    for id in ids[1:]:
        if global_state != id.hide_viewport:
            global_state = None

    return global_state

def get_sel_global_state_disable_render(sel : Iterable[ID] | None = None) -> bool | None:
    ids: list[Object, Collection] = get_sel_collections(sel) + get_sel_objects(sel)
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

    internal_id : IntProperty(
        name = 'internal_id',
        options = {"HIDDEN"}
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - HideInViewport - execute')

        ids: list[Object, Collection] = get_sel_collections() + get_sel_objects()
        if len(ids) == 0:
            ids = [item.id for item in bpy.context.scene.hide.previous_sel]

        global_state = get_sel_global_state_hide_viewport(ids)

        sel_layer_collections: tuple[LayerCollection] = get_sel_layer_collections(ids)
        if len(sel_layer_collections) > 0:
            if global_state == None or global_state == False:
                for layer_collection in sel_layer_collections:
                    layer_collection.hide_viewport = True
            else:
                for layer_collection in sel_layer_collections:
                    layer_collection.hide_viewport = False

        sel_objects = get_sel_objects(ids)
        if len(sel_objects) > 0:
            if global_state == None or global_state == False:
                for obj in sel_objects:
                    obj.hide_set(True)
            else:
                for obj in sel_objects:
                    obj.hide_set(False)
                    obj.select_set(True)

        try:
            bpy.context.scene.hide.previous_sel.clear()
        except:
            pass
        for id in ids:
            previous_sel_new_item = bpy.context.scene.hide.previous_sel.add()
            previous_sel_new_item.id = id

        return {"FINISHED"}

class DisableInViewports(bpy.types.Operator):
    bl_idname = OP_IDNAME_PREFIX + "." + "disableinviewports"
    bl_label = "Hide - Disable in viewport"
    bl_description = "Disable in viewport."
    bl_options = {"UNDO", "INTERNAL"}

    internal_id : IntProperty(
        name = 'internal_id',
        options = {"HIDDEN"}
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - DisableInViewports - execute')

        ids: list[Object, Collection] = get_sel_collections() + get_sel_objects()
        if len(ids) == 0:
            ids = [item.id for item in bpy.context.scene.hide.previous_sel]

        if len(ids) > 0:
            global_state = get_sel_global_state_disable_viewport(ids)
            if global_state == None or global_state == False:
                for id in ids:
                    id.hide_viewport = True
            else:
                for id in ids:
                    id.hide_viewport = False
                    if id.bl_rna.identifier == 'Object':
                        id.select_set(True)

            try:
                bpy.context.scene.hide.previous_sel.clear()
            except:
                pass
            for id in ids:
                previous_sel_new_item = bpy.context.scene.hide.previous_sel.add()
                previous_sel_new_item.id = id

        return {"FINISHED"}

class DisableInRenders(bpy.types.Operator):
    bl_idname = OP_IDNAME_PREFIX + "." + "disableinrenders"
    bl_label = "Hide - Disable in render"
    bl_description = "Disable in render."
    bl_options = {"UNDO", "INTERNAL"}

    internal_id : IntProperty(
        name = 'internal_id',
        options = {"HIDDEN"}
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('Hide - DisableInRenders - execute')

        ids: list[Object, Collection] = get_sel_collections() + get_sel_objects()
        if len(ids) == 0:
            ids = [item.id for item in bpy.context.scene.hide.previous_sel]

        if len(ids) > 0:
            global_state = get_sel_global_state_disable_render(ids)
            if global_state == None or global_state == False:
                for id in ids:
                    id.hide_render = True
            else:
                for id in ids:
                    id.hide_render = False
                    if id.bl_rna.identifier == 'Object':
                        id.select_set(True)
            
            try:
                bpy.context.scene.hide.previous_sel.clear()
            except:
                pass
            for id in ids:
                previous_sel_new_item = bpy.context.scene.hide.previous_sel.add()
                previous_sel_new_item.id = id

        return {"FINISHED"}

class Hide(bpy.types.Operator):
    bl_idname = OP_IDNAME_PREFIX + "." + "hide"
    bl_label = "Hide - Hide"
    bl_description = "Hide the selection"
    bl_options = {"UNDO", "INTERNAL"}

    internal_id : IntProperty(
        name = 'internal_id',
        options = {"HIDDEN"}
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