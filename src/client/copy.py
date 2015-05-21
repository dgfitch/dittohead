import paramiko
import os
import posixpath
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


def copy_files(window_owner, user, password, files, study, remotehost="guero"):
    """
    User and password are unencrypted in memory.
    Probably not great.

    `files` is a list of hashes which contains
        - local_path    (absolute, for easier fun)
        - remote_path   (relative)
        - mtime         (in case we want to force mtimes to match?)

    `study` is the hash with name, remote_directory, extra_contacts, and so on

    """
    log = logging.getLogger('dittohead.copy')

    log.info("Starting copy of %s files for %s to %s in study %s", len(files), user, remotehost, study['name'])

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remotehost, username=user, password=password)

    ftp = ssh.open_sftp()
    final_folder_name = "dittohead-{0}-tmp".format(study['name'])
    upload_folder_name = "." + final_folder_name

    log.debug("Creating folder " + upload_folder_name)
    # TODO: After testing, turn off ignore_existing here, we should explode if we collide with something that already exists
    mkdir(ftp, upload_folder_name, ignore_existing=True)

    index = 1
    for f in files:
        log.debug("Operating on file {0}".format(f))
        remote_path = f['remote_path']
        local_path  = f['local_path']
        full_remote_path = posixpath.join(upload_folder_name, remote_path)

        # make directory for remote path if necessary
        full_remote_folder = posixpath.dirname(full_remote_path)
        mkdir(ftp, full_remote_folder, ignore_existing=True)

        window_owner.CopyingFile(index, len(files), local_path)
        # TODO: This supports a callback that sends bytes/total bytes, surface to UI?
        ftp.put(local_path, upload_folder_name + "/" + remote_path)
        index += 1

    ftp.close()

    ssh.exec_command("mv '{0}' '{1}'".format(upload_folder_name, final_folder_name))

    ssh.close()
    