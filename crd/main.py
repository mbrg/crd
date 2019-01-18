#!/usr/bin/env python3.7

import argparse

from storage import MODELS
from config import ConfigurationManager


def parse_arguments(argv):

    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(title="command", dest="command", help="available commands", required=True)

    config = commands.add_parser("config", help="configure storage")
    config_options = config.add_subparsers(title="storage", dest="storage", help="available storage")
    for name, desc, model in MODELS:
        parser_create = config_options.add_parser(name, help=desc)
        for arg in model.get_arguments():
            parser_create.add_argument(arg[0], arg[1], **arg[2])

    run = commands.add_parser("run", help="run actions")

    args = parser.parse_args(argv)
    return args


def config(args):
    """
    Save configuration to local cache
    """
    with ConfigurationManager() as cfg:
        cfg.cache = args.__dict__


def main(argv=None):
    args = parse_arguments(argv)

    if args.command == "config":
        config(args)
    if args.command == "run":
        with ConfigurationManager() as cfg:
            print(cfg.cache)


if __name__ == "__main__":
    main()
