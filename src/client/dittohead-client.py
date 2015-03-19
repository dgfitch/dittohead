import os
import subprocess
import wx
from sys import stdin

PSCP = r"c:\Program Files (x86)\PuTTY\pscp.exe"
PLINK = r"c:\Program Files (x86)\PuTTY\plink.exe"
REMOTE_HOST = "guero"


# TODO: Take a UI base from a wx sample


def copy():
    localfile = r"c:\DanTemp\git\pySketch"
    remotefile = "dittohead_copy"

    try:
        # Making a directory
        subprocess.check_call([PLINK, REMOTE_HOST, "-batch", "mkdir .%s" % remotefile])

        # Copying a local directory recursively
        subprocess.check_call([PSCP, "-r", "-C", localfile, "%s:.%s" % (REMOTE_HOST, remotefile)])

        # Move the directory to its final location
        subprocess.check_call([PLINK, REMOTE_HOST, "-batch", "mv .{0} {0}".format(remotefile)])

    except Exception as e:
        # Show some kind of helpful error here.
        # TODO: We should also log it to a local log of some kind
        print "Got an exception", e

        """
        Now here's a weird thing: input hangs here on a failure,
        possibly because the subprocess calls above cause some kind
        of input redirection
        """
        #input("Hit ENTER to exit")

