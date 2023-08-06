#!/usr/bin python
# -*- coding: utf-8 -*-
"""Generate PI Parameter defines."""

from collections import OrderedDict
from io import open  # Redefining built-in 'open' pylint: disable=W0622
import os

from pipython.pitools import piwrite
from signtools import signfile

__version__ = '1.0.0.8'
__signature__ = 0xc625a67f12263d6e96cdfcf6545169e5

INFILE = r'T:\Entwicklung\HostSoftware\libs\PIDefinitions\source\PIParameter.h'
OUTFILE = r'.\pipython\pidevice\piparams.py'


def readparamdefs():
    """Parse INFILE and return parameter definitions.
    @return : Parameter definitions as ordered dictionary {name: id}.
    """
    params = OrderedDict()
    print('read parameter defines from %s' % INFILE)
    with open(INFILE, 'r', encoding='utf-8', newline='\n') as fobj:
        for line in fobj:
            if not line.strip().startswith('#define'):
                continue
            paramname = line.split()[1].strip().lstrip('PI_PARA_')
            paramid = line.split()[2].strip().rstrip('UL')
            paramid = int(paramid, base=16)
            params[paramid] = 'P0X%0X_%s' % (paramid, paramname)
    return params


def updateparamdefs(paramdefs):
    """Update parameter definitions in OUTFILE and save OUTFILE.
    @paramdefs : Parameter definitions as ordered dictionary {name: id}.
    """
    print('write: %s' % os.path.abspath(OUTFILE))
    newlines = []
    inparamdef = False
    with open(OUTFILE, 'r', encoding='utf-8', newline='\n') as fobj:
        for line in fobj:
            if line.strip().startswith('# parameter definition end'):
                inparamdef = False
            if inparamdef:
                continue
            newlines.append(line)
            if line.strip().startswith('# parameter definition begin'):
                inparamdef = True
                for paramid, paramname in paramdefs.items():
                    newlines.append('%s = 0x%0x\n' % (paramname, paramid))
    piwrite(OUTFILE, newlines)


def create():
    """Update parameter definitions and sign OUTILE."""
    paramdefs = readparamdefs()
    updateparamdefs(paramdefs)
    signfile(OUTFILE)


if __name__ == '__main__':
    create()
