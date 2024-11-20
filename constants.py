# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

import os

import bpy

ADDON_NAME = __package__
OP_IDNAME_PREFIX = ADDON_NAME.lower().split('.')[-1]

PREFS_DIR = bpy.utils.extension_path_user(ADDON_NAME, path="prefs", create=True)
PREFS_FILEPATH = os.path.join(PREFS_DIR, 'hide_prefs.json')

KEYMAPITEM_TEMPLATE = {
    'km_name' : '',
    'kmi_op_idname' : '',
    'kmi_type' : '',
    'kmi_value' : '',
    'kmi_any' : False,
    'kmi_shift' : 0,
    'kmi_ctrl' : 0,
    'kmi_alt' : 0,
    'kmi_oskey' : 0,
    'kmi_key_modifier' : 'NONE',
    'kmi_direction' : 'ANY',
    'kmi_repeat' : False,
    'kmi_head' : False,
    'km_space_type' : 'EMPTY',
    'km_region_type' : 'WINDOW',
    'km_modal' : False,
    'km_tool' : False,
}

KEYMAPITEM_HIDE_OBJECTMODE = {
    'km_name' : 'Object Mode',
    'kmi_op_idname' : 'hide.hide',
    'kmi_type' : 'H',
    'kmi_value' : 'PRESS',
    'km_space_type' : 'EMPTY',
}

KEYMAPITEM_HIDE_OUTLINER = {
    'km_name' : 'Outliner',
    'kmi_op_idname' : 'hide.hide',
    'kmi_type' : 'H',
    'kmi_value' : 'PRESS',
    'km_space_type' : 'OUTLINER',
}

DEFAULT_KMI_LIST = (KEYMAPITEM_HIDE_OBJECTMODE,
                    KEYMAPITEM_HIDE_OUTLINER,
)