import argparse
import json
import logging
import os
import shutil
import sys

import svn.local
import svn.remote
import svn.utility

from opengrok_tools.utils.log import fatal, get_class_basename, get_console_logger
from opengrok_tools.utils.readconfig import read_config

SRC_ROOT = '.'
CONFIG_PATH = ''


# update working copy
def update_repository(repository, sys_name):
    sys_dir = os.path.join(SRC_ROOT, sys_name.upper())

    # do update process
    def update(local_dir, username, password):
        client = svn.local.LocalClient(local_dir, username, password)
        client.update()
        info = client.info()

        print(json.dumps(info, indent=2, default=str))

    if os.path.exists(sys_dir):
        local_dir = f"{sys_dir}/web"
        print("Update VCS Path:  {}".format(local_dir))
        update(local_dir, repository['username'], repository['password'])

        local_dir = f"{sys_dir}/web"
        print("Update VCS Path:  {}".format(local_dir))
        update(local_dir, repository['username'], repository['password'])

    pass


# 由vcs checkout
def checkout_repository(repository, sys_name, web_path, sisapp_path):
    sys_dir = os.path.join(SRC_ROOT, sys_name.upper())
    vcs_host = repository['host']
    print("VCS Host: {}, System Directory: {}".format(vcs_host, sys_dir))
    if os.path.exists(sys_dir):
        shutil.rmtree(sys_dir)
    os.makedirs(sys_dir)

    if vcs_host.endswith('/'):
        vcs_host = vcs_host[:-1] + ''

    # do checkout process
    def checkout(remote_dir, local_dir, username, password):
        print("Checkout from {} to {}".format(remote_dir, local_dir))
        client = svn.remote.RemoteClient(remote_dir, username, password)
        client.checkout(local_dir)

    # checkout web
    remote_dir = f"{vcs_host}{web_path}"
    local_dir = f"{sys_dir}/web"
    checkout(remote_dir, local_dir, repository['username'], repository['password'])

    # checkout sisapp
    remote_dir = f"{vcs_host}{sisapp_path}"
    local_dir = f"{sys_dir}/sisapp"
    checkout(remote_dir, local_dir, repository['username'], repository['password'])


"""
entrypoint 
"""


def main():
    # parse command-line arguments
    parser = argparse.ArgumentParser(description='sync between svn and source directory')
    parser.add_argument('-c', '--config', default=f"{os.getcwd()}/config/repository.yml", help='config file path')
    parser.add_argument('-a', '--action', default='update', help='action which to be performed, checkout / update ')
    parser.add_argument('src_root', help='The root path of source code to be checkout to')

    # parser.print_help()

    global SRC_ROOT
    global CONFIG_PATH
    global ACTION

    try:
        args = parser.parse_args()
    except ValueError as e:
        return fatal(e, exit=False)

    logger = get_console_logger(get_class_basename(), logging.DEBUG)
    # logger = get_console_logger(get_class_basename(), args.loglevel)

    logger.info(f"Config: {args.config}, Src-Path: {args.src_root}")

    CONFIG_PATH = args.config
    SRC_ROOT = args.src_root
    ACTION = args.action.lower()

    configs = read_config(logger, CONFIG_PATH)

    logger.info(json.dumps(configs, indent=4))

    for sys_name, config in configs['systems'].items():
        try:
            repository = configs['repositories'][config['repository']]
            if ACTION == 'checkout':
                checkout_repository(repository, sys_name, config['web-path'], config['sisapp-path'])
            elif ACTION == 'update':
                update_repository(repository, sys_name)

        except Exception as ex:
            fatal(ex, exit=False)


if __name__ == '__main__':
    sys.exit(main())
