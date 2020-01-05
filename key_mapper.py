#!/usr/bin/env python3

import os
import re
import signal
import subprocess
import sys
from importlib import reload

import mappings


DEVICE_PATH = '/dev/input/by-id/usb-Kinesis_Savant_Elite2_Foot_Pedal_271828182846-if01-event-kbd'
CONFIG_PATH = '/etc/actkbd.conf'

current_mapping = None
current_mapping_process = None


def receive_signal(signum, frame):
    if signum != signal.SIGHUP:
        return
    print('Reloading configuration')
    reload(mappings)


def handle_title_change(title):
    if not title:
        return

    if not os.path.exists(DEVICE_PATH):
        return

    print(title)

    for i in range(len(mappings.TITLE_MAP)):
        if i % 2:
            continue
        if mappings.TITLE_MAP[i].match(title):
            remap_keys(mappings.TITLE_MAP[i+1])
            return
    global current_mapping
    if current_mapping != mappings.DEFAULT_MAP:
        remap_keys(mappings.DEFAULT_MAP)


def remap_keys(new_mapping):
    print(new_mapping)
    contents = ''
    for i in range(len(new_mapping)):
        if new_mapping[i] is None:
            continue
        contents += '%s:%s::%s\n' % (mappings.ORIGINAL_KEYS[i], 'key,rep', new_mapping[i])
    with open(CONFIG_PATH, 'w') as f:
        f.write(contents)

    global current_mapping_process
    if current_mapping_process is not None:
        current_mapping_process.terminate()
    if contents:
        current_mapping_process = subprocess.Popen(['actkbd -g -d %s' % DEVICE_PATH], stdout=sys.stdout, shell=True)
    global current_mapping
    current_mapping = new_mapping


if __name__ == '__main__':
    signal.signal(signal.SIGHUP, receive_signal)

    with os.popen('xtitle -s') as xtitle:
        for title in xtitle:
            handle_title_change(title)
