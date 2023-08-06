#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Update current year in copyright message."""

from argparse import ArgumentParser
from datetime import datetime
from io import open
import os
import re

from pipython.pitools import piwrite

__version__ = '1.0.0.11'
__signature__ = 0x3a82052c6d4d51735f9e526c6d97d101

REGEX = re.compile(r'# \(c\)20\d{2}(-\d{4}) Physik Instrumente \(PI\) GmbH & Co\. KG')


def findfiles(filepath):
    """Yield absolute path to Python files in 'filepath'.
    @param filepath : Full path to source file or directory to scan recursively.
    """
    if os.path.isdir(filepath):
        for root, _dirs, files in os.walk(filepath):
            for filename in files:
                if not filename.lower().endswith('.py'):
                    continue
                curfilepath = os.path.join(root, filename)
                yield os.path.abspath(curfilepath)
    else:
        yield os.path.abspath(filepath)


def updatecopyright(filepath):
    """Update first occurence of REGEX in 'filepath' to current year and save 'filepath' if appropriate.
    @param filepath : Full path to python source file to update.
    """
    lines = []
    tosave = False
    newcopyright = '-%d' % datetime.now().year
    with open(filepath, 'r', encoding='utf-8', newline='\n') as fobj:
        for line in fobj:
            match = REGEX.match(line)
            if match is None:
                lines.append(line)
                continue
            if match.groups()[0] == newcopyright:
                return
            lines.append(re.sub(match.groups()[0], newcopyright, line))
            tosave = True
    if tosave:
        print('update copyright in %s' % filepath)
        piwrite(filepath, lines)


def main():
    """Read source code and add/update a signature."""
    parser = ArgumentParser()
    parser.add_argument(dest='filepath', metavar='FILEPATH',
                        help='full path to file or directory to update copyright')
    args = parser.parse_args()
    for filepath in findfiles(args.filepath):
        updatecopyright(filepath)


if __name__ == '__main__':
    main()
