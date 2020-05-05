import re


# Config file version. Generally should not be manually changed.
VERSION = 1

# Path of the device whose keys will be partialy replaced by the map below.
DEVICE_PATH = '/dev/input/by-id/usb-Kinesis_Savant_Elite2_Foot_Pedal_271828182846-if01-event-kbd'


# Convenience functions for encapsulating xdotool commands.
def key(combination):
    return 'xdotool key %s' % combination
def keys(combination):
    return 'xdotool type %s' % combination
def mouse(click):
    return 'xdotool click %s' % click


# List of keys that will be rewritted by {DEFAULT,TITLE}_MAP.
#
# These keys are specified by the number of the KEY_* or BTN_* entries in:
# https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
ORIGINAL_KEYS = ['2', '57', '4']

# Replacement commands for ORIGINAL_KEYS when no TITLE_MAP entry matches the
# current title.
DEFAULT_MAP = [key('u'), key('n'), key('d')]

# List of pairs mapping regex expression of window title to list of new commands.
TITLE_MAP = [
    (re.compile('/home/.*[.]pdf'), [key('Control_L+u'), key('Down'), key('Control_L+d')]),
    (re.compile('.*- Anki'), []),
    (re.compile('.* \[Emacs\]'), [key('Alt_L+v'), key('Control_L+s'), key('Control_L+v')]),
    (re.compile('ranger'), [key('Control_L+u'), key('space'), key('Control_L+d')]),

    (re.compile('.*- Gmail - Opera'),
        [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
         ' && '.join([key('Escape'), key('Page_Down')]),
         ' && '.join([key('Escape'), keys('ij'), key('Escape')])]),
    (re.compile('.*- Gmail - Google Chrome'),
        [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
         ' && '.join([key('Escape'), key('Page_Down')]),
         ' && '.join([key('Escape'), keys('ij'), key('Escape')])]),
    (re.compile('.*- Google.com Mail - Google Chrome'),
        [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
         ' && '.join([key('Escape'), key('Page_Down')]),
         ' && '.join([key('Escape'), keys('ij'), key('Escape')])]),

    (re.compile('.*- Opera'), [keys('u'), key('Down'), keys('d')]),
    (re.compile('.*- Google Chrome'), [keys('u'), key('Down'), keys('d')]),

    (re.compile('grep .*'), [key('u'), key('n'), key('d')]),
    (re.compile('git grep .*'), [key('u'), key('n'), key('d')]),
    (re.compile('git diff'), [key('u'), key('n'), key('d')]),
    (re.compile('git log'), [key('u'), key('n'), key('d')]),
    (re.compile('git show'), [key('u'), key('n'), key('d')]),
]
