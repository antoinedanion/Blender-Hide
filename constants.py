import os

ADDON_NAME = __name__.split('.')[0]

PREFS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'prefs')
PREFS_FILEPATH = os.path.join(PREFS_DIR, 'hide_prefs.json')