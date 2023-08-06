#!/usr/bin python
# -*- coding: utf-8 -*-
"""Generate Python GCS Error defines from PIErrorCodes definitions."""

from io import open  # Redefining built-in 'open' pylint: disable=W0622
import os
import json

from pipython.pitools import piwrite
import pipython.pidevice.gcs30.gcs30error as gcs30erors
from signtools import signfile

__version__ = '1.1.0.9'
__signature__ = 0xb2d818eb32ae35a9b36dd4f23c3f8af7

INFILE = r'.\pipython\pidevice\gcs30\CustomError.json'
OUTFILE = r'.\pipython\pidevice\gcs30\gcs30error.py'


def readerrordefs():
    """Parse 'INFILE' and return list of errors defines.
    @return : Error definitions as list of tuples [(value, name)].
    """
    errors = []
    print('read error defines from %s' % INFILE)
    with open(INFILE, 'r') as error_file:
        possible_errors = json.load(error_file)

        for error_key in possible_errors[gcs30erors.PI_GCS30_ERRORS_ERRORS_DICT_KEY]:
            error_class_key = possible_errors[gcs30erors.PI_GCS30_ERRORS_ERRORS_DICT_KEY][error_key][
                gcs30erors.PI_GCS30_ERRORS_CLASS_KEY]

            if gcs30erors.PI_GCS30_ERRORS_ID_KEY in possible_errors[gcs30erors.PI_GCS30_ERRORS_ERRORS_DICT_KEY][error_key]:
                error_id = possible_errors[gcs30erors.PI_GCS30_ERRORS_ERRORS_DICT_KEY][error_key][
                    gcs30erors.PI_GCS30_ERRORS_ID_KEY]
                error_name = error_key
            else:
                if ':' in error_key:
                    error_id = int(error_key.split(':')[0])
                    error_name = error_key.split(':')[1]

            error_module_key = possible_errors[gcs30erors.PI_GCS30_ERRORS_ERRORS_DICT_KEY][error_key][
                gcs30erors.PI_GCS30_ERRORS_MODULE_KEY]

            module_alias = possible_errors[gcs30erors.PI_GCS30_ERRORS_MODULES_DICT_KEY][error_module_key][
                gcs30erors.PI_GCS30_ERRORS_ALIAS_KEY]

            for class_key in error_class_key:
                error_class = possible_errors[gcs30erors.PI_GCS30_ERRORS_CLASSES_DICT_KEY][class_key][
                    gcs30erors.PI_GCS30_ERRORS_ID_KEY]

                error_class_alias = possible_errors[gcs30erors.PI_GCS30_ERRORS_CLASSES_DICT_KEY][class_key][
                    gcs30erors.PI_GCS30_ERRORS_ALIAS_KEY]

                errval = gcs30erors.GCS30Error.parse_to_errorcode(error_class, error_id)
                errname = error_name.replace('$MODULE', module_alias).replace('$CLASS', error_class_alias)

                errors.append((errval, errname))

    return errors


def createsource(errordefs):
    """Create source code from 'errordefs'.
    @errordefs : Error definitions as list of tuples [(value, name, message)].
    @return: Source code as list of strings with trailing linefeeds.
    """
    valdefs = []  # e.g. E_1024_PI_MOTION_ERROR = -1024
    for curval, curname in errordefs:
        valstr = '%s%d' % ('_' if curval < 0 else '', abs(curval))
        valdefs.append('E%s_%s = %d\n' % (valstr, curname, curval))
    return valdefs + ['\n']


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
