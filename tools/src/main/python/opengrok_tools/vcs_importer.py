import argparse
import json
import logging
import os
import sys

import svn.local
import svn.remote
import svn.utility

from opengrok_tools.utils.log import fatal, get_class_basename, get_console_logger
from opengrok_tools.utils.readconfig import read_config
from .utils.parsers import get_base_parser
from opengrok_tools.projadm import project_add

SRC_ROOT = '.'
CONFIG_PATH = ''

__version__ = '0.1'


def check_rep_urlL(repository, *paths):
    vcs_host = repository['host']
    id, pw = repository['username'], repository['password']
    if vcs_host.endswith('/'):
        vcs_host = vcs_host[:-1] + ''
    for path in paths:
        if path:
            print(f"Checking Remote Path: {path}")
            try:
                client = svn.remote.RemoteClient(f"{vcs_host}{path}", id, pw)
                client.info()
            except Exception as ex:
                fatal(ex, exit=False)


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
        # shutil.rmtree(sys_dir)
        # update_repository(repository, sys_name)
        return
    else:
        os.makedirs(sys_dir)

    if vcs_host.endswith('/'):
        vcs_host = vcs_host[:-1] + ''

    # do checkout process
    def checkout(remote_dir, local_dir, username, password):
        print("Checkout from {} to {}".format(remote_dir, local_dir))
        client = svn.remote.RemoteClient(remote_dir, username, password)
        client.checkout(local_dir)

    # checkout web
    if web_path:
        remote_dir = f"{vcs_host}{web_path}"
        local_dir = f"{sys_dir}/web"
        checkout(remote_dir, local_dir, repository['username'], repository['password'])

    # checkout sisapp
    if sisapp_path:
        remote_dir = f"{vcs_host}{sisapp_path}"
        local_dir = f"{sys_dir}/sisapp"
        checkout(remote_dir, local_dir, repository['username'], repository['password'])


def main():
    # parse command-line arguments
    global __version__
    parser = argparse.ArgumentParser(description='sync between svn and source directory', parents=[get_base_parser(
        tool_version=__version__)])
    parser.add_argument('-c', '--config', default=f"{os.getcwd()}/config/repository.yml", help='config file path')
    parser.add_argument('-U', '--uri', default='http://localhost:8080/',
                        help='URI of the webapp with context path')
    group = parser.add_argument_group('Actions', 'checkout/update/check/add')
    group.add_argument('-a', '--action', default='update',
                       help='action which to be performed')
    parser.add_argument('src_root', default=".", help='The root path of source code to be checkout to')

    # parser.print_help()

    global SRC_ROOT
    global CONFIG_PATH
    global ACTION

    try:
        args = parser.parse_args()
    except ValueError as e:
        return fatal(e, exit=False)

    # logger = get_console_logger(get_class_basename(), logging.DEBUG)
    logger = get_console_logger(get_class_basename(), args.loglevel)

    logger.info(f"Config: {args.config}, Src-Path: {args.src_root}")

    CONFIG_PATH = args.config
    SRC_ROOT = args.src_root
    ACTION = args.action.lower()

    configs = read_config(logger, CONFIG_PATH)

    logger.info(json.dumps(configs, indent=4))

    for sys_name, config in configs['systems'].items():
        try:
            # web_path = config['web-path'] if 'web-path' in config.keys() else None
            # sisapp_path = config['sisapp-path'] if 'sisapp-path' in config.keys() else None
            #
            # print("System: {}, Web-Path: {}, Sisapp-Path: {}".format(sys_name, web_path, sisapp_path))

            repository = configs['repositories'][config['repository']]
            web_path = config['web-path'] if 'web-path' in config.keys() else None
            sisapp_path = config['sisapp-path'] if 'sisapp-path' in config.keys() else None
            if ACTION == 'checkout':
                checkout_repository(repository, sys_name, web_path, sisapp_path)
            elif ACTION == 'update':
                update_repository(repository, sys_name)
            elif ACTION == 'check':
                check_rep_urlL(repository, web_path, sisapp_path)
            elif ACTION == 'add':
                project_add(doit=False,
                            logger=logger,
                            project=sys_name.upper,
                            uri=args.url)

        except Exception as ex:
            fatal(ex, exit=False)


if __name__ == '__main__':
    sys.exit(main())
