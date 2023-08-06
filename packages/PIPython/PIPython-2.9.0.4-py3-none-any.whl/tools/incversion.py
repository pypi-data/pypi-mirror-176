#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Increase __version__ formatted 'x.x.x.x' of given python module."""

from io import open
from sys import argv

from pipython.pitools import piwrite

__version__ = '1.0.0.10'
__signature__ = 0xd2ff4562ceaae0b5d754f18aa01c477b


def incversion(filepath):
    """Increase module scoped __version__ in file 'filepath'.
    @param filepath : Python file.
    """
    with open(filepath, 'r', encoding='utf-8', newline='\n') as fobj:
        lines = fobj.readlines()
    versionstr = ''
    for i in range(len(lines)):
        if lines[i].startswith('__version__'):
            version = lines[i].split('=')[1].strip().strip("'").strip('"')
            version = [int(x) for x in version.split('.')]
            version[3] += 1
            versionstr = '.'.join(str(x) for x in version)
            lines[i] = "__version__ = '%s'\n" % versionstr
            break
    print('increase version of %r to %s...' % (filepath, versionstr))
    piwrite(filepath, lines)


if __name__ == '__main__':
    incversion(argv[1])
