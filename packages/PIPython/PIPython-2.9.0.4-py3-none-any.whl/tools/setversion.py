#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Insert current pipython version into a text file given by command line argument."""

from io import open
from sys import argv

from pipython import __version__ as version
from pipython.pitools import piwrite

__version__ = '1.0.0.12'
__signature__ = 0xe0a5f857aa99759f07c4afb16da5c3f1


def setversion(filepath):
    """Update file 'filepath' with __version__.
    @param filepath : Python or Doxygen file.
    """
    print('set version of %r to %s...' % (filepath, version))
    versioninfo = tuple([int(num) for num in version.split('.')])
    newlines = []
    with open(filepath, 'r', encoding='utf-8', newline='\n') as fobj:
        for line in fobj:
            if line.startswith('__version_info__'):
                line = "__version_info__ = " + repr(versioninfo) + "\n"
            elif line.startswith('__version__'):
                line = "__version__ = '" + version + "'\n"
            elif line.startswith('Version:'):
                line = 'Version: ' + version + '\n'
            elif line.startswith('PROJECT_NUMBER'):
                line = 'PROJECT_NUMBER = ' + version + '\n'
            newlines.append(line)
    piwrite(filepath, newlines)


if __name__ == '__main__':
    setversion(argv[1])
