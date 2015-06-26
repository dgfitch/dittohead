#!/usr/bin/env python

"""
Dittohead worker process.

Given an input directory and settings from `config.yaml`, does:

- Copy to `processing_directory`
- Process by copying files into `study_directory`
  (using the study name in the uploaded folder and putting them
   inside a folder there named for `study_dittohead_raw_folder_name`)
- TODO: Notification
- Move folder from `processing_directory` to `done_directory`
"""

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

def configure_logging(log_directory):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # From the logging cookbook: https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
    log = logging.getLogger('dittohead-worker')
    log.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    fh = logging.FileHandler("{0}/dittohead-worker-{1}-{2}.log".format(log_directory, os.getpid(), datetime.datetime.now().replace(" ", "_")))
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


config = load_yaml("config.yaml")
log = configure_logging(config["log_directory"])
input_directory = sys.argv[1]

log.info("Initializing worker for directory {0}".format(input_directory))


# NOW STUFF HAPPENS

folder_name = os.path.basename(input_directory)
study_name = folder_name.split("-")[0]

study_location = os.path.join(config["study_directory"], study_name, config["study_dittohead_raw_folder_name"])
processing_location = os.path.join(config["processing_directory"], folder_name)
done_location = os.path.join(config["done_directory"], folder_name)

log.info("Working on directory {0}, using processing location {1} and study location {2}".format(input_directory, processing_location, study_location))


# We move it into processing
os.rename(input_directory, processing_location)


# From there we copy the files to the study directory
# TODO: figure out some way to use rsync to ensure no filename collisions and no changing existing files?
# TODO: Should we track these collisions and include them in a notification email?
rsync_command = "rsync -avzBupOMGLOLZ {0} {1}".format(processing_location, study_location)
log.info("Running rsync: " + rsync_command)
#os.system(rsync_command)


log.info("Done processing location {0} to study location {1}, leaving in {2}".format(processing_location, study_location, done_location))


# Success! We move it into done
os.rename(processing_location, done_location)

# TODO: Email notification of the original user somehow

