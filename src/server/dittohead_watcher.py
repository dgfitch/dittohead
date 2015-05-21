#!/usr/bin/env python

import os
import logging
import yaml
import pwd
import subprocess
import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def load_yaml(filename):
    if os.path.isfile(filename):
        stream = open(filename, 'r')
        x = yaml.load(stream)
        stream.close()
        return x
    else:
        return {}

def configure_logging():
    # From the logging cookbook: https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
    log = logging.getLogger('dittohead-watcher')
    log.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    # TODO: This should probably be stored somewhere smarter
    fh = logging.FileHandler('dittohead-watcher.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a less-verbose log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)

    return log



class DittoheadWatcher(FileSystemEventHandler):
    def __init__(self, config, *args, **kwargs):
        super(DittoheadWatcher, self).__init__(*args, **kwargs)
        self.log = configure_logging()
        self.config = config

    def on_created(self, event):
        self.log.info("Got created: {0}".format(event))
        # If the thing that was created was a directory and it doesn't start with ., throw a warning
        #if event.src_path
  
    def on_moved(self, event):
        self.log.info("Got moved: {0}".format(event))
        # If the thing that moved was a directory

    def operate(self, directory):
        process = subprocess.Popen(
            ["dittohead_worker.py", directory]
        )


def main():
    config = load_yaml("config.yaml")
    input = config["input_directory"]

    # First, if there are any pending things in the directory, operate on them!
    # TODO

    # Using Watchdog: https://pypi.python.org/pypi/watchdog
    observer = Observer()
    watcher = DittoheadWatcher(config)
    observer.schedule(watcher, input)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()

