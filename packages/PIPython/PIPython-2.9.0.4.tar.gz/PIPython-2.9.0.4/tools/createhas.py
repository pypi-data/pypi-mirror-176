#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Create Has functions for GCSCommands."""

from io import open
import re

from signtools import signfile
from pipython.pitools import piwrite

__version__ = '1.0.1.10'
__signature__ = 0xc97aaf271545480a51e939d7999e1241

SOURCEFILE_GCSBASE = r'pipython/pidevice/common/gcsbasecommands.py'
SOURCEFILE_GCS2 = r'pipython/pidevice/gcs2/gcs2commands.py'
SOURCEFILE_GCS30 = r'pipython/pidevice/gcs30/gcs30commands.py'

FUNCDEF = re.compile(r'^    def ([a-zA-Z_]*)\(.*')

TEMPLATE = '''    def Has{0}(self):
        """Return True if {0}() is available."""
        return self._has('{0}')

'''

def read(sourcefile, funcdef):
    """Read SOURCEFILE and return its function names.
    @return : Tuple of source code as string and function names as list of strings.
    """
    sourcecode = ''
    items = []
    scanenabled = False
    with open(sourcefile, 'r', encoding='utf-8', newline='\n') as fobj:
        for line in fobj:
            sourcecode += line
            if scanenabled:
                match = re.match(funcdef, line)
                if match:
                    items.append(match.groups()[0])
            if line.find('# GCS FUNCTIONS') >= 0:
                scanenabled = True
            if line.find('# CODEGEN BEGIN') >= 0:
                sourcecode += '\n'
                return sourcecode, items


def save(sourcecode, items, sourcefile, template):
    """Save 'sourcecode' and generated code from 'items'.
    @param sourcecode : Exisiting source code as string.
    @param items : List of function names as strings.
    """
    generatedcode = ''
    for item in items:
        generatedcode += template.format(item).encode('utf-8').decode('utf-8')
    generatedcode = generatedcode.rstrip() + '\n'
    piwrite(sourcefile, sourcecode + generatedcode)


if __name__ == '__main__':
    ALLITHEMS = set()

    SOURCE_BASE, ITEMS = read(SOURCEFILE_GCSBASE, FUNCDEF)
    ALLITHEMS.update(set(ITEMS))

    SOURCE_GCS2, ITEMS = read(SOURCEFILE_GCS2, FUNCDEF)
    ALLITHEMS.update(set(ITEMS))

    SOURCE_GCS30, ITEMS = read(SOURCEFILE_GCS30, FUNCDEF)
    ALLITHEMS.update(set(ITEMS))

    print('create %d has-functions in %s' % (len(ITEMS), SOURCEFILE_GCSBASE))
    save(SOURCE_BASE, list(ALLITHEMS), SOURCEFILE_GCSBASE, TEMPLATE)
    signfile(SOURCEFILE_GCSBASE)
