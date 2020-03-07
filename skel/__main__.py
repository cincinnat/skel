#! /bin/env python3

import argparse
import signal
import sys

import skel


def main(args):
    def get_target(target_types):
        target_type = filter(lambda t: getattr(args, t), target_types)
        target_type = next(target_type)
        lang = getattr(args, target_type)
        return lang, target_type

    lang, target_type = get_target(['project', 'module', 'script'])
    target_name = args.name

    handler_name = f'gen_{lang}_{target_type}'
    handler = getattr(skel.actions, handler_name)
    handler(target_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='create a cpp/python project skeleton')

    group = parser.add_argument_group('available targets')
    group = group.add_mutually_exclusive_group(required=True)
    group.add_argument('--project', '-p', metavar='LANG',
        choices=['cpp', 'py'],
        help='create a py/cpp project')
    group.add_argument('--module', '-m', metavar='LANG',
        choices=['cpp'],
        help='create a module')
    group.add_argument('--script', '-s', metavar='LANG',
        choices=['py'],
        help='create a script')

    parser.add_argument('name', help='a target name')

    parsed_args = parser.parse_args()

    try:
        main(parsed_args)
    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)
