#!/usr/bin/env python3.7

import argparse
import logging
import pyperclip
import getpass


from storage import MODELS, NAME_TO_MODEL, init_storage
from config import ConfigurationManager


def configure_logger(logger_name=None, level='INFO'):

    # get logger
    logger = logging.getLogger(logger_name)

    # configure level
    logger.setLevel(level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='[%(asctime)s %(filename)s:%(lineno)s %(funcName)s()] - %(message)s',
        datefmt='%I:%M:%S')
    ch.setFormatter(formatter)
    ch.setLevel(level)
    logger.addHandler(ch)


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def crd_print(*args, **kwargs):
    print(Colors.OKBLUE + "crd >" + Colors.ENDC, *args, **kwargs)


def parse_arguments(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', default='ERROR', choices=logging._nameToLevel.keys(), help="output internal logs for debugging")
    commands = parser.add_subparsers(title="command", dest="command", help="available commands", required=True)

    cmnd_config = commands.add_parser("config", help="configure storage")
    cmnd_config.add_argument('--show', action='store_true', default=False, help="show current configuration")
    config_options = cmnd_config.add_subparsers(title="storage", dest="storage", help="available storage")
    for name, desc, model in MODELS:
        parser_create = config_options.add_parser(name, help=desc)
        for arg in model.get_arguments():
            parser_create.add_argument(arg[0], arg[1], **arg[2])

    cmnd_get = commands.add_parser("get", help="get secrets to clipboard")
    cmnd_get.add_argument('-k', '--key', type=str, default="", help="search keys by this substring")

    cmnd_set = commands.add_parser("set", help="set secrets to storage")
    cmnd_set.add_argument('-k', '--key', type=str, help="unique secret name")

    args = parser.parse_args(argv)
    return args


def run_config(args):
    """
    Save configuration to local cache and/or present them to stdout
    """
    with ConfigurationManager() as cfg:

        if args.show:
            crd_print(cfg.cache)

        if args.storage is not None:
            cfg.cache = args.__dict__


def input_choice(options: dict):

    crd_print("Found %d options:" % len(options))
    [print("\t%d | %s" % (k, v)) for k, v in options.items()]

    choice = -1
    while not (isinstance(choice, int) and 0 <= choice <= len(options) - 1):
        raw_choice = input("Choose {%d..%d} " % (0, len(options) - 1))
        if raw_choice in ('q', 'Q'):
            exit(0)

        try:
            choice = int(raw_choice)
        except (ValueError, TypeError):
            choice = -1

    return choice


def run_get(args):
    """
    Get secrets from storage
    """
    with ConfigurationManager() as cfg:
        strg = init_storage(NAME_TO_MODEL[cfg.cache['storage']], **cfg.cache)

        key_options = dict(enumerate(sorted([k for k in strg.keys() if args.key in k])))
        if len(key_options) > 0:

            if len(key_options) > 1:
                key = key_options[input_choice(key_options)]
            else:
                key = key_options[0]

            raw_secret = strg[key]

            if isinstance(raw_secret, dict):
                secret_options = dict(enumerate(raw_secret.keys()))
                secret = secret_options[input_choice(secret_options)]
            else:
                secret = raw_secret

            pyperclip.copy(secret)
            crd_print(Colors.OKGREEN + "Secret %s was copied to clipboard." % key + Colors.ENDC)
        else:
            crd_print("Found no relevant secrets, please try another query.")


def run_set(args):
    """
    Set secrets to storage
    """
    with ConfigurationManager() as cfg:
        strg = init_storage(NAME_TO_MODEL[cfg.cache['storage']], **cfg.cache)

        strg[args.key] = getpass.getpass()
        crd_print(Colors.OKGREEN + "Secret %s stored safely." % args.key + Colors.ENDC)


def main(argv=None):
    args = parse_arguments(argv)
    configure_logger("crd", args.log)

    if args.command == "config":
        run_config(args)
    if args.command == "get":
        run_get(args)
    if args.command == "set":
        run_set(args)


if __name__ == "__main__":
    main()
