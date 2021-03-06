import os
import subprocess
#import logging
from application import app

BIN_FFPROBE = app.config['BIN_FFPROBE']
BIN_FFMPEG = app.config['BIN_FFMPEG']
BIN_SSH = app.config['BIN_SSH']
BIN_RSYNC = app.config['BIN_RSYNC']


def get_sizedata(filepath):
    outdata = dict(
        size = int(os.stat(filepath).st_size)
        )
    return outdata


def rsync(path, remote_dir=''):
    DRY_RUN = False
    arguments=['--verbose', '--ignore-existing', '--recursive', '--human-readable']
    logs_path = app.config['CDN_SYNC_LOGS']
    storage_address = app.config['CDN_STORAGE_ADDRESS']
    user = app.config['CDN_STORAGE_USER']
    rsa_key_path = app.config['CDN_RSA_KEY']
    known_hosts_path = app.config['CDN_KNOWN_HOSTS']

    if DRY_RUN:
        arguments.append('--dry-run')
    folder_arguments = list(arguments)
    if rsa_key_path:
        folder_arguments.append(
            '-e ' + BIN_SSH + ' -i ' + rsa_key_path + ' -o "StrictHostKeyChecking=no"')
    # if known_hosts_path:
    #     folder_arguments.append("-o UserKnownHostsFile " + known_hosts_path)
    folder_arguments.append("--log-file=" + logs_path  + "/rsync.log")
    folder_arguments.append(path)
    folder_arguments.append(user + "@" + storage_address + ":/public/" + remote_dir)
    # print (folder_arguments)
    devnull = open(os.devnull, 'wb')
    # DEBUG CONFIG
    # print folder_arguments
    # proc = subprocess.Popen(['rsync'] + folder_arguments)
    # stdout, stderr = proc.communicate()
    subprocess.Popen(['nohup', BIN_RSYNC] + folder_arguments, stdout=devnull, stderr=devnull)


def remote_storage_sync(path): #can be both folder and file
    if os.path.isfile(path):
        filename = os.path.split(path)[1]
        rsync(path, filename[:2] + '/')
    else:
        if os.path.exists(path):
            rsync(path)
