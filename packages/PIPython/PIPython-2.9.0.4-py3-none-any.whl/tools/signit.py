#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Read source code and add/update an MD5 hash."""

from argparse import ArgumentParser
import os

from signtools import signfile

__version__ = '1.0.2.2'
__signature__ = 0x8ffb9f2af96d1f72bcb42f1b3aeea57f


def signit(filepath):
    """Add/update signature in file 'filepath' or recursively in all "*.py" files in directory 'filepath'.
    @param filepath : Full path to source file or directory to scan recursively.
    """
    if os.path.isdir(filepath):
        for root, _dirs, files in os.walk(filepath):
            for filename in files:
                if not filename.lower().endswith('.py'):
                    continue
                curfilepath = os.path.join(root, filename)
                signfile(curfilepath)
    else:
        signfile(filepath)


def main():
    """Read source code and add/update a signature."""
    parser = ArgumentParser()
    parser.add_argument(dest='filepath', metavar='FILEPATH',
                        help='full path to file or directory to add/update signature')
    args = parser.parse_args()
    signit(args.filepath)


if __name__ == '__main__':
    main()
