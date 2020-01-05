import re


def key(combination):
    return 'xdotool key %s' % combination
def keys(combination):
    return 'xdotool type %s' % combination
def mouse(click):
    return 'xdotool click %s' % click

ORIGINAL_KEYS = ['2', '57', '4']
DEFAULT_MAP = [key('a'), key('b'), key('c')]

TITLE_MAP = [
    re.compile('/home/.*[.]pdf'), [key('Control_L+u'), key('Down'), key('Control_L+d')],
    re.compile('.*- Anki'), [],
    re.compile('.* \[Emacs\]'), [key('Alt_L+v'), key('Control_L+s'), key('Control_L+v')],
    re.compile('ranger'), [key('Control_L+u'), key('space'), key('Control_L+d')],

    re.compile('.*- Gmail - Opera'),
        [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
         ' && '.join([key('Escape'), keys('i_'), key('Escape')]),
         ' && '.join([key('Escape'), keys('ij'), key('Escape')])],
    re.compile('.*- Gmail - Google Chrome'),
        [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
         ' && '.join([key('Escape'), keys('i_'), key('Escape')]),
         ' && '.join([key('Escape'), keys('ij'), key('Escape')])],
    re.compile('.*- Google.com Mail - Google Chrome'),
        [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
         ' && '.join([key('Escape'), keys('i_'), key('Escape')]),
         ' && '.join([key('Escape'), keys('ij'), key('Escape')])],

    re.compile('.*- Opera'), [keys('u'), key('Down'), keys('d')],
    re.compile('.*- Google Chrome'), [keys('u'), key('Down'), keys('d')],

    re.compile('grep .*'), [key('u'), key('n'), key('d')],
    re.compile('git grep .*'), [key('u'), key('n'), key('d')],
    re.compile('git diff'), [key('u'), key('n'), key('d')],
    re.compile('git log'), [key('u'), key('n'), key('d')],
    re.compile('git show'), [key('u'), key('n'), key('d')],
]
