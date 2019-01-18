#!/usr/bin/env python3

import argparse

from storage import models


def parse_arguments(argv):

    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(title="command", dest="command", help="available commands", required=True)

    config = commands.add_parser("config", help="configure storage")
    config_options = config.add_subparsers(title="storage", dest="storage", help="available storage")
    for name, desc, model in models:
        parser_create = config_options.add_parser(name, help=desc)
        for arg in model.get_arguments():
            parser_create.add_argument(arg[0], arg[1], **arg[2])

    args = parser.parse_args(argv)
    return args


def main(argv=None):
    args = parse_arguments(argv)


if __name__ == "__main__":
    main()
