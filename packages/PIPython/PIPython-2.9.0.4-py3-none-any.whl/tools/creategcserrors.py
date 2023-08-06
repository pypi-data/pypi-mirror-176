#!/usr/bin python
# -*- coding: utf-8 -*-
"""Generate Python GCS Error defines from PIErrorCodes definitions."""

from io import open  # Redefining built-in 'open' pylint: disable=W0622
import os

from pipython.pitools import piwrite
from signtools import signfile

__version__ = '1.1.0.9'
__signature__ = 0x5d27c1debd3311f6a56b1b726fe52983

INFILE = r'T:\Entwicklung\HostSoftware\libs\PIDefinitions\generate_code\data\PIErrorCodes.err.txt'
OUTFILE = r'.\pipython\pidevice\gcserror.py'


def readerrordefs():
    """Parse 'INFILE' and return list of errors defines.
    @return : Error definitions as list of tuples [(value, name, message)].
    """
    errors = []
    print('read error defines from %s' % INFILE)
    with open(INFILE, 'r', encoding='utf-8', newline='\n') as fobj:
        for line in fobj:
            sect = line.split()
            try:
                errval = int(sect[0])
                errname = sect[1]
                if errname == 'COM_NO_ERROR':  # is duplicate of value "0"
                    continue
                errmsg = ' '.join(sect[2:])
                errmsg = errmsg.replace('\\"', "'")
            except (ValueError, IndexError):
                continue
            errors.append((errval, errname, errmsg))
    return errors


def createsource(errordefs):
    """Create source code from 'errordefs'.
    @errordefs : Error definitions as list of tuples [(value, name, message)].
    @return: Source code as list of strings with trailing linefeeds.
    """
    valdefs = []  # e.g. E_1024_PI_MOTION_ERROR = -1024
    defvals = []  # e.g. PI_MOTION_ERROR__1024 = -1024
    errmsgs = []  # e.g. -1024: "Motion error: position error too large, servo is switched off automatically",
    for curval, curname, curmsg in errordefs:
        valstr = '%s%d' % ('_' if curval < 0 else '', abs(curval))
        valdefs.append('E%s_%s = %d\n' % (valstr, curname, curval))
        defvals.append('%s_%s = %d\n' % (curname, valstr, curval))
        errmsgs.append('    %d: "%s",\n' % (curval, curmsg))
    return valdefs + ['\n'] + defvals + ['\n', '_ERRMSG = {\n'] + errmsgs + ['}\n']


def updateerrordefs(errordefs):
    """Update error definitions in OUTFILE and save OUTFILE.
    @errordefs : Error definitions as list of tuples [(value, name, message)].
    """
    print('write: %s' % os.path.abspath(OUTFILE))
    newlines = []
    inparamdef = False
    with open(OUTFILE, 'r', encoding='utf-8', newline='\n') as fobj:
        for line in fobj:
            if line.strip().startswith('# error definition end'):
                inparamdef = False
            if inparamdef:
                continue
            newlines.append(line)
            if line.strip().startswith('# error definition begin'):
                inparamdef = True
                newlines += createsource(errordefs)
    piwrite(OUTFILE, newlines)


def create():
    """Update error definitions and sign OUTILE."""
    paramdefs = readerrordefs()
    updateerrordefs(paramdefs)
    signfile(OUTFILE)


if __name__ == '__main__':
    create()
