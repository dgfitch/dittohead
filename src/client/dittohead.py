import os
import logging
import yaml

import wx
from dittohead_interface import *


def configure_logging():
    # From the logging cookbook: https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
    log = logging.getLogger('dittohead')
    log.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    fh = logging.FileHandler('dittohead.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a less-verbose log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)

    return log


def load_yaml(filename, default={}):
    if os.path.isfile(filename):
        stream = open(filename, 'r')
        x = yaml.load(stream)
        stream.close()
        return x
    else:
        return default

def save_yaml(x, filename):
    with open(filename, 'w') as outfile:
        outfile.write( yaml.dump(x, default_flow_style=False) )


log = configure_logging()


studies = load_yaml("studies.yaml", [])
if len(studies) < 1:
    log.warn("No studies found in YAML settings file.")

last_users = load_yaml("last_users.yaml", {})

app = wx.App(0)
copy_frame = CopyFrame(None, wx.ID_ANY, "", size=wx.Size(800,600))
copy_frame.LoadStudies(log, studies, last_users)
app.SetTopWindow(copy_frame)
copy_frame.Show()

app.MainLoop()

save_yaml(last_users, "last_users.yaml")
save_yaml(studies, "studies.yaml")


