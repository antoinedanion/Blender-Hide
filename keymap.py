import bpy
from bpy.types import (KeyMap,
                       KeyMapItem
                      )

addon_keymaps: list[tuple[KeyMap,KeyMapItem]] = []

def add_kmi(km_name: str, kmi_op_idname: str, kmi_type, kmi_value, any=False, shift=0, ctrl=0, alt=0, oskey=0, key_modifier='NONE', direction='ANY', repeat=False, head=False, km_space_type='EMPTY', km_region_type:str='WINDOW', modal=False, tool=False):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name=km_name, space_type=km_space_type, region_type=km_region_type, modal=modal, tool=tool)
    kmi = km.keymap_items.new(idname=kmi_op_idname, type=kmi_type, value=kmi_value, any=any, shift=shift, ctrl=ctrl, alt=alt, oskey=oskey, key_modifier=key_modifier, direction=direction, repeat=repeat, head=head)
    addon_keymaps.append((km, kmi))

def register():    
    add_kmi(
        km_name='Object Mode',
        kmi_op_idname='hide.hide',
        kmi_type='H',
        kmi_value='PRESS',
        km_space_type='EMPTY'
    )
    add_kmi(
        km_name='Outliner',
        kmi_op_idname='hide.hide',
        kmi_type='H',
        kmi_value='PRESS',
        km_space_type='OUTLINER'
    )

def unregister():
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()