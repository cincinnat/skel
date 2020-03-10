#! /bin/env python3

import argparse
import signal
import sys


def main(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='description',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parsed_args = parser.parse_args()

    try:
        main(parsed_args)
    except BrokenPipeError:
        sys.exit(128 + signal.SIGPIPE)
    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)
