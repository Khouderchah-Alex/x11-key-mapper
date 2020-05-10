#!/usr/bin/env python3

import attr
import importlib
import os
import pkgutil
import re
import signal
import subprocess
import sys
from time import sleep
from typing import Dict, List


@attr.s
class MappingConfig:
    current_mapping = attr.ib(type=List[str])
    process = attr.ib()
    config = attr.ib()


class KeyMapper:
    EXIT_SIGNALS = [
        signal.SIGINT,
        signal.SIGQUIT,
        signal.SIGILL,
        signal.SIGTRAP,
        signal.SIGABRT,
        signal.SIGTERM,
    ]
    CONFIG_BASE_PATH = '/etc/actkbd_'
    PIDFILE_PATH = '/var/run/key_mapper.pid'


    def __init__(self):
        self.configs = {}


    def run(self):
        signal.signal(signal.SIGHUP, self._receive_signal)
        for signum in self.EXIT_SIGNALS:
            signal.signal(signum, self._receive_signal)

        # Set up pidfile.
        pid = os.getpid()
        if os.path.exists(self.PIDFILE_PATH):
            print('An instance already appears to be running.')
            print('If this is not the case, remove the file: %s' % self.PIDFILE_PATH)
            exit(1)

        try:
            with open(self.PIDFILE_PATH, 'w') as f:
                f.write('%d' % pid)

            self._load_configurations()
            with os.popen('xtitle -s') as xtitle:
                for title in xtitle:
                    self._handle_title_change(title)
        finally:
            self._cleanup()


    def _load_configurations(self):
        package = importlib.import_module("config")
        self.configs.clear()
        for _, name, _ in pkgutil.walk_packages(package.__path__):
            module = importlib.import_module(package.__name__ + '.' + name)
            if any(c.config.DEVICE_PATH == module.DEVICE_PATH
                   for c in self.configs.values()):
                print('Cannot have multiple config files configuring the same device: ')
                print('  %s' % module.DEVICE_PATH)
                exit(2)
            self.configs[name] = MappingConfig([], None, module)
        if len(self.configs) == 0:
            print('No mapping configuration found.')
            print('Have you tried running setup.sh?')
            exit(2)


    def _receive_signal(self, signum, frame):
        if signum == signal.SIGHUP:
            print('Reloading configuration')
            self._load_configurations()
        elif signum in self.EXIT_SIGNALS:
            self._cleanup()


    def _cleanup(self):
        if os.path.exists(self.PIDFILE_PATH):
            os.remove(self.PIDFILE_PATH)


    def _handle_title_change(self, title):
        if not title:
            return

        print(title)
        for k,v in self.configs.items():
            if not os.path.exists(v.config.DEVICE_PATH):
                continue

            found = False
            for i in range(len(v.config.TITLE_MAP)):
                if v.config.TITLE_MAP[i][0].match(title):
                    self._remap_keys(k, v.config.TITLE_MAP[i][1])
                    found = True
                    break
            if not found and v.current_mapping != v.config.DEFAULT_MAP:
                self._remap_keys(k, v.config.DEFAULT_MAP)


    def _remap_keys(self, name, new_mapping):
        print(new_mapping)

        config = self.configs[name]
        contents = ''
        for i in range(len(new_mapping)):
            if new_mapping[i] is None:
                continue
            contents += '%s:%s::%s\n' % (config.config.ORIGINAL_KEYS[i], 'key,rep', new_mapping[i])
        path = self.CONFIG_BASE_PATH + name + '.conf'
        with open(path, 'w') as f:
            f.write(contents)

        if config.process is not None:
            config.process.terminate()
        if contents:
            config.process = subprocess.Popen(
                ['actkbd -g -c %s -d %s' % (path, config.config.DEVICE_PATH)],
                stdout=sys.stdout, shell=True)
        config.current_mapping = new_mapping


if __name__ == '__main__':
    key_mapper = KeyMapper()
    # In certain cases, running actkbd right after an input event on a remapped
    # device can cause the key release event to be missed by the system. Sleep
    # briefly so that hitting enter to run this command will not 'lock' the
    # enter key. Note that this isn't a foolproof solution, but makes this more
    # usable. A better long-term solution is to have actkbd release all keys on
    # startup.
    sleep(0.1)
    key_mapper.run()
