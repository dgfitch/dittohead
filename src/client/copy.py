import paramiko
import os
import platform
import logging

# These extensions to paramiko are required to recursively copy a directory
# Taken from http://stackoverflow.com/questions/4409502/directory-transfers-on-paramiko
def put_dir(ftp, source, target):
    ''' Uploads the contents of the source directory to the target path. The
        target directory needs to exists. All subdirectories in source are 
        created under target.
    '''
    for item in os.listdir(source):
        if os.path.isfile(os.path.join(source, item)):
            ftp.put(os.path.join(source, item), '%s/%s' % (target, item))
        else:
            mkdir(ftp, '%s/%s' % (target, item), ignore_existing=True)
            put_dir(ftp, os.path.join(source, item), '%s/%s' % (target, item))

def mkdir(ftp, path, mode=511, ignore_existing=False):
    ''' Augments mkdir by adding an option to not fail if the folder exists  '''
    try:
        ftp.mkdir(path, mode)
    except IOError:
        if ignore_existing:
            pass
        else:
            raise


def copy_files(user, password, localfile, remotehost="guero", remotefile="dittohead_copy"):
    log = logging.getLogger('dittohead.copy')

    log.info("Starting copy of %s for %s to %s in %s", localfile, user, remotehost, remotefile)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remotehost, username=user, password=password)

        ftp = ssh.open_sftp()
        ftp.mkdir("." + remotefile)
        put_dir(ftp, localfile, "." + remotefile)
        ftp.close()

        ssh.exec_command("mv '.{0}' '{0}'".format(remotefile))

        ssh.close()
        
    except Exception as e:
        # If this was a UI program, show some kind of helpful error here.
        log.error("Got an exception: %s", e)
        raise e
