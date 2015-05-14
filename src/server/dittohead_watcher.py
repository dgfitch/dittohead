#!/usr/bin/env python

import os
import logging
import yaml
import pwd
import subprocess
import sys


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


def main():

    log = configure_logging()
    config = load_yaml("config.yaml")

    if config['should-demote']:
        pw_record = pwd.getpwnam(config['subprocess-user-name'])
        user_name      = pw_record.pw_name
        user_home_dir  = pw_record.pw_dir
        user_uid       = pw_record.pw_uid
        user_gid       = pw_record.pw_gid
        env = os.environ.copy()
        env[ 'HOME'     ]  = user_home_dir
        env[ 'LOGNAME'  ]  = user_name
        env[ 'USER'     ]  = user_name
        report_ids(log, 'starting ' + str(args))
        process = subprocess.Popen(
            args, preexec_fn=demote(user_uid, user_gid), env=env
        )
        report_ids(log, 'finished ' + str(args))


def demote(log, user_uid, user_gid):
    def result():
        report_ids(log, 'starting demotion')
        os.setgid(user_gid)
        os.setuid(user_uid)
        report_ids(log, 'finished demotion')
    return result


def report_ids(log, msg):
    log.info( 'uid, gid = %d, %d; %s' % (os.getuid(), os.getgid(), msg) )


if __name__ == '__main__':
    main()

