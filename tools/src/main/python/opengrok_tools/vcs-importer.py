import argparse
import os
import logging
import svn.utility, svn.local, svn.remote
import yaml
import json
import sys

from opengrok_tools.utils.log import fatal, get_class_basename, get_console_logger
from opengrok_tools.utils.readconfig import read_config


def checkout(base_config, sys_config):
    pass


"""
entrypoint 
"""

def main():
    parser = argparse.ArgumentParser(description='sync between svn and source directory')
    parser.add_argument('-c', '--config', default=f"{os.getcwd()}/config/repository.yml", help='config file path')
    parser.add_argument('src_root', help='The root path of source code to be checkout to')

    # parser.print_help()

    try:
        args = parser.parse_args()
    except ValueError as e:
        return fatal(e, exit=False)

    logger = get_console_logger(get_class_basename(), logging.DEBUG)
    # logger = get_console_logger(get_class_basename(), args.loglevel)

    logger.info(f"Config: {args.config}, Src-Path: {args.src_root}")

    config_file = args.config
    src_path = args.src_root

    config = read_config(logger, config_file)

    logger.info(json.dumps(config, indent=4))

    svn_username = 'richard'
    svn_password = 'oftd6370'
    svn_host = 'http://svn.wanhai.com/svn'

    # client = svn.utility.get_client(svn_host, username=svn_username, password=svn_password)
    # entries = client.list(rel_path='/whl/web/dgs')
    # for entry in entries:
    #     print(entry)
    #

    # client = svn.remote.RemoteClient(f"{svn_host}/whl/web/dgs", username=svn_username, password=svn_password)
    #
    # client.checkout(f"{os.getcwd()}/DGS")


if __name__ == '__main__':
    sys.exit(main())
