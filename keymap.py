import bpy

addon_keymaps = []

def register():

    # handle the keymap
    wm = bpy.context.window_manager
    
    km_objectmode = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km_objectmode.keymap_items.new('hide.toggleviewportdisplay', 'H', 'PRESS')
    addon_keymaps.append((km_objectmode, kmi))

    km_outliner = wm.keyconfigs.addon.keymaps.new(name='Outliner', space_type='OUTLINER')
    kmi = km_outliner.keymap_items.new('hide.toggleviewportdisplay', 'H', 'PRESS')
    addon_keymaps.append((km_outliner, kmi))


def unregister():

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()