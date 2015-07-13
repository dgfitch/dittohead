import wx
import paramiko
import os
import posixpath
import platform
import logging
import datetime



# We mirror the paramiko exception up to the UI so it doesn't have to know anything about paramiko
class AuthenticationException(Exception):
    pass



def mkdir(ftp, path, mode=511, ignore_existing=False):
    ''' Augments mkdir by adding an option to not fail if the folder exists  '''
    try:
        ftp.mkdir(path, mode)
    except IOError:
        if ignore_existing:
            pass
        else:
            raise


def copy_files(thread, user, password, files, study, remotehost="guero"):
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

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remotehost, username=user, password=password)

        ftp = ssh.open_sftp()
        final_folder_name = "{0}-{1}".format(study['name'], str(datetime.datetime.now()).replace(" ", "_"))
        final_folder_path = "{0}/{1}".format(study['remote_directory'], final_folder_name)
        upload_folder_name = "." + final_folder_name
        upload_folder_path = "{0}/{1}".format(study['remote_directory'], upload_folder_name)

        log.debug("Creating folder " + upload_folder_path)
        mkdir(ftp, upload_folder_path)

        index = 1
        for f in files:
            log.debug("Operating on file {0}".format(f))
            remote_path = f['remote_path']
            local_path  = f['local_path']
            full_remote_path = posixpath.join(upload_folder_path, remote_path)

            # make directory for remote path if necessary
            full_remote_folder = posixpath.dirname(full_remote_path)
            mkdir(ftp, full_remote_folder, ignore_existing=True)

            thread.progress(index, local_path)
            destination_path = upload_folder_path + "/" + remote_path

            # TODO: This supports a callback that sends bytes/total bytes, surface to UI as well someday?
            ftp.put(local_path, destination_path)

            mtime = os.path.getmtime(local_path)
            # Here we update the atime and mtime on the server
            ftp.utime(destination_path, (mtime, mtime))

            index += 1
            if thread.should_abort():
                break

        ftp.close()

        if not thread.should_abort():
            mv = "mv '{0}' '{1}'".format(upload_folder_path, final_folder_path)
            log.debug("Running " + mv)
            ssh.exec_command(mv)

        ssh.close()

        log.info("Completed copy of %s files for %s to %s in study %s", len(files), user, remotehost, study['name'])
        
    except paramiko.ssh_exception.AuthenticationException:
        log.info("Authentication exception by %s", user)
        raise AuthenticationException()

