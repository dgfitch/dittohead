import os
import subprocess
from sys import stdin

PSCP = r"c:\Program Files (x86)\PuTTY\pscp.exe"
PLINK = r"c:\Program Files (x86)\PuTTY\plink.exe"
localfile = r"c:\DanTemp\git\pySketch"
remotehost = "guero"
remotefile = "dittohead_copy"

#os.system('"%s" "%s" "%s:%s"' % (PSCP, localfile, remotehost, remotefile) )

try:
    # Making a directory
    subprocess.check_call([PLINK, remotehost, "-batch", "mkdir .%s" % remotefile])

    # Copying a local directory recursively
    subprocess.check_call([PSCP, "-r", "-C", localfile, "%s:.%s" % (remotehost, remotefile)])

    # Move the directory to its final location
    subprocess.check_call([PLINK, remotehost, "-batch", "mv .{0} {0}".format(remotefile)])

except Exception as e:
    # If this was a UI program, show some kind of helpful error here.
    # TODO: We should also log it to a local log of some kind
    print "Got an exception", e

    """
    Now here's a weird thing: input hangs here on a failure,
    possibly because the subprocess calls above cause some kind
    of input redirection
    """
    #input("Hit ENTER to exit")

