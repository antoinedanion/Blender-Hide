# "Hide" Blender Add-on which simplifies the hide and unhide process.
# Copyright (C) 2024  Antoine Danion

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/antoinedanion/Blender-Hide/blob/main/NOTICE>.

import os

ADDON_NAME = __package__
OP_IDNAME_PREFIX = ADDON_NAME.lower().split('.')[-1]

PREFS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'prefs')
PREFS_FILEPATH = os.path.join(PREFS_DIR, 'hide_prefs.json')