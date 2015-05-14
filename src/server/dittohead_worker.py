#!/usr/bin/env python

import os
import datetime
import logging
import sys

def configure_logging():
    # From the logging cookbook: https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
    log = logging.getLogger('dittohead-worker')
    log.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    # TODO: This should probably be stored somewhere smarter
    fh = logging.FileHandler("dittohead-worker-{0}-{1}.log".format(os.getpid(), datetime.now()))
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

input_directory = sys.argv[1]
log.info("Working on directory {0}".format(input_directory))
