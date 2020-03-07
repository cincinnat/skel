#! /bin/env python3

import sys
import argparse
import signal


def main(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='create a cpp/python project skeleton',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)
