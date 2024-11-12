import os

ADDON_NAME = __package__
OP_IDNAME_PREFIX = ADDON_NAME.lower()

PREFS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'prefs')
PREFS_FILEPATH = os.path.join(PREFS_DIR, 'hide_prefs.json')