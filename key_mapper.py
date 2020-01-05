#!/usr/bin/env python3

import os
import re
import subprocess
import sys

DEVICE_PATH = '/dev/input/by-id/usb-Kinesis_Savant_Elite2_Foot_Pedal_271828182846-if01-event-kbd'
CONFIG_PATH = '/etc/actkbd.conf'

def key(combination):
    return 'xdotool key %s' % combination
def keys(combination):
    return 'xdotool type %s' % combination
def mouse(click):
    return 'xdotool click %s' % click

TITLE_MAP = [re.compile('/home/.*[.]pdf'), [key('Control_L+u'), key('Down'), key('Control_L+d')],
             re.compile('.*- Anki'), [],
             re.compile('.* \[Emacs\]'), [key('Alt_L+v'), key('Control_L+s'), key('Control_L+v')],
             re.compile('.*- Gmail - Opera'), [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
                                               ' && '.join([key('Escape'), keys('i_'), key('Escape')]),
                                               ' && '.join([key('Escape'), keys('ij'), key('Escape')])],
             re.compile('.*- Gmail - Google Chrome'), [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
                                                       ' && '.join([key('Escape'), keys('i_'), key('Escape')]),
                                                       ' && '.join([key('Escape'), keys('ij'), key('Escape')])],
             re.compile('.*- Google.com Mail - Google Chrome'),
                 [' && '.join([key('Escape'), keys('ik'), key('Escape')]),
                  ' && '.join([key('Escape'), keys('i_'), key('Escape')]),
                  ' && '.join([key('Escape'), keys('ij'), key('Escape')])],
             re.compile('.*- Opera'), [keys('gT'), key('Down'), keys('gt')],
             re.compile('.*- Google Chrome'), [keys('u'), key('Down'), keys('d')],
             re.compile('grep .*'), [key('u'), key('n'), key('d')],
             re.compile('git grep .*'), [key('u'), key('n'), key('d')],
             re.compile('git diff'), [key('u'), key('n'), key('d')],
             re.compile('git log'), [key('u'), key('n'), key('d')],
             re.compile('git show'), [key('u'), key('n'), key('d')],
             re.compile('ranger'), [key('Control_L+u'), key('space'), key('Control_L+d')],
]

ORIGINAL_KEYS = ['2', '57', '4']
DEFAULT_MAPPING = [key('a'), key('b'), key('c')]

current_mapping = None
current_mapping_process = None


def handle_title_change(title):
    if not title:
        return

    if not os.path.exists(DEVICE_PATH):
        return

    print(title)

    for i in range(len(TITLE_MAP)):
        if i % 2:
            continue
        if TITLE_MAP[i].match(title):
            remap_keys(TITLE_MAP[i+1])
            return
    global current_mapping
    if current_mapping != DEFAULT_MAPPING:
        remap_keys(DEFAULT_MAPPING)


def remap_keys(new_mapping):
    print(new_mapping)
    contents = ''
    for i in range(len(new_mapping)):
        if new_mapping[i] is None:
            continue
        contents += '%s:%s::%s\n' % (ORIGINAL_KEYS[i], 'key,rep', new_mapping[i])
    with open(CONFIG_PATH, 'w') as f:
        f.write(contents)

    global current_mapping_process
    if current_mapping_process is not None:
        current_mapping_process.terminate()
    #current_mapping_process = os.popen('actkbd -d %s -D' % DEVICE_PATH)
    if contents:
        current_mapping_process = subprocess.Popen(['actkbd -g -d %s' % DEVICE_PATH], stdout=sys.stdout, shell=True)
    global current_mapping
    current_mapping = new_mapping


if __name__ == '__main__':
    with os.popen('xtitle -s') as xtitle:
        for title in xtitle:
            handle_title_change(title)
