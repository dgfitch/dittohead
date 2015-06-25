#!/usr/bin/env python

import os
import sys
import pwd
import datetime
import yaml
import logging

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
    log = logging.getLogger('dittohead-worker')
    log.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    # TODO: This should probably be stored somewhere smarter
    fh = logging.FileHandler("dittohead-worker-{0}-{1}.log".format(os.getpid(), datetime.datetime.now()))
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


log = configure_logging()
input_directory = sys.argv[1]
log.info("Initializing for directory {0}".format(input_directory))

config = load_yaml("config.yaml")
# Do we need to run as a different user? MAYBE NOT!
#p = pwd.getpwnam(config['subprocess_user_name'])
#os.setgid(p.pw_uid)
#os.setuid(p.pw_gid)

log.info("Working on directory {0} using uid {1} and gid {2}".format(input_directory, p.pw_uid, p.pw_gid))


#### NOW STUFF HAPPENS

os.rename()

