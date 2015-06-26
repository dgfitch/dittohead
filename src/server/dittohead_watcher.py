#!/usr/bin/env python

import os
import logging
import yaml
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


def operate(directory):
    subprocess.Popen(
        ["python", "dittohead_worker.py", directory]
    )


class DittoheadWatcher(FileSystemEventHandler):
    def __init__(self, config, *args, **kwargs):
        super(DittoheadWatcher, self).__init__(*args, **kwargs)
        self.log = configure_logging()
        self.config = config

    def path_is_period(self, path):
        return os.path.basename(path).startswith(".")

    def on_created(self, event):
        self.log.info("Got created: {0}".format(event))
        if event.is_directory:
            # If the thing that was created was a directory and it doesn't start with ., throw a warning
            if not self.path_is_period(event.src_path):
                self.log.warn("Directory was created without a period: {0}".format(event.src_path))
            else:
                self.log.info("New directory was created: {0}".format(event.src_path))
  
    def on_moved(self, event):
        if event.is_directory:
            # If the thing that moved was a directory,
            # and its new name does not start with a period,
            # we should operate on it
            if self.path_is_period(event.src_path) and not self.path_is_period(event.dest_path):
                self.log.info("Got moved directory, firing watcher: {0}".format(event))
                operate(event.dest_path)



def main():
    config = load_yaml("config.yaml")
    input_dir = config["input_directory"]

    # First, if there are any pending things in the directory already, operate on them!
    for f in os.listdir(input_dir):
        path = os.path.join(input_dir, f)
        if os.path.isdir(path):
            operate(path)

    # Now, watch the input directory using Watchdog
    observer = Observer()
    watcher = DittoheadWatcher(config)
    observer.schedule(watcher, input_dir)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()

