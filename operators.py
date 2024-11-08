from typing import Any, Iterable

import bpy
from bpy.types import ID, Object, Collection

def get_sel() -> dict[str, ID]:
    # Docs used
    # https://blender.stackexchange.com/questions/203729/python-get-selected-objects-in-outliner Check bl_rna.identifier
    # https://blender.stackexchange.com/questions/325004/how-can-i-get-the-currently-selected-objects-in-the-outliner-if-they-are-hidden Override the context
    # https://blender.stackexchange.com/questions/326453/cant-get-proper-context-selected-ids-from-3d-view DO NOT copy the entire context

    sel_objects = {}

    override_context = {}
    area = [area for area in bpy.context.screen.areas if area.type == "OUTLINER"][0]
    override_context['area'] = area
    override_context['region'] = area.regions[-1]
    
    if bpy.context.area.type != 'OUTLINER':
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

def get_sel_collections(sel: dict[str, ID]) -> tuple[Collection]:
    ids = []
    try:
        ids = sel['Collections']
    except:
        pass
    return tuple(ids)

def get_sel_objects(sel: dict[str, ID]) -> tuple[Object]:
    ids = []
    try:
        ids = sel['Objects']
    except:
        pass
    return tuple(ids)

def get_sel_global_state(sel: dict[str, ID]) -> bool | None:
    ids: list[ID] = get_sel_collections(sel) + get_sel_objects(sel)
    global_state = ids[0].hide_viewport
    for id in ids[1:]:
        if global_state != id.hide_viewport:
            global_state = None

    return global_state

class DisableInViewport(bpy.types.Operator):
    bl_idname = "hide.disableinviewport"
    bl_label = "Hide - Disable in viewport"
    bl_description = "Disable in viewport"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print('\nHide - DisableInViewport - execute')

        sel = get_sel()
        ids: list[Object, Collection] = get_sel_collections(sel) + get_sel_objects(sel)
        if len(ids) > 0:
            global_state = get_sel_global_state(sel)
            if global_state == None or global_state == False:
                for id in ids:
                    id.hide_viewport = True
            else:
                for id in ids:
                    id.hide_viewport = False
                    if id.bl_rna.identifier == 'Object':
                        id.select_set(True)

        return {"FINISHED"}

ops = (
    DisableInViewport,
)

def register():
    from bpy.utils import register_class
    for cls in ops:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(ops):
        unregister_class(cls)