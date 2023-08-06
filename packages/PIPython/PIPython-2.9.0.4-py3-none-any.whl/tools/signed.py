#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Read source code and verify its MD5 hash."""

from argparse import ArgumentParser
import os

from signtools import verifyfile

__version__ = '1.0.1.1'
__signature__ = 0xcfb2ea169f524851e474b08450811db2


def signed(filepath):
    """Verify  signature in file 'filepath' or recursively in all "*.py" files in directory 'filepath'.
    @param filepath : Full path to source file or directory to scan recursively.
    """
    if os.path.isdir(filepath):
        for root, _dirs, files in os.walk(filepath):
            for filename in files:
                if not filename.lower().endswith('.py'):
                    continue
                curfilepath = os.path.join(root, filename)
                verifyfile(curfilepath)
    else:
        verifyfile(filepath)


def main():
    """Read source code and add/update a signature."""
    parser = ArgumentParser()
    parser.add_argument(dest='filepath', metavar='FILEPATH',
                        help='full path to file or directory to add/update signature')
    args = parser.parse_args()
    signed(args.filepath)


if __name__ == '__main__':
    main()
