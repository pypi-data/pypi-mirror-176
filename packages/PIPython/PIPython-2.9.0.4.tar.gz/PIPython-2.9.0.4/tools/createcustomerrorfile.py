#!/usr/bin python
# -*- coding: utf-8 -*-
"""Generate Python GCS Error defines from PIErrorCodes definitions."""
import os
from io import open  # Redefining built-in 'open' pylint: disable=W0622
import numpy
import json

from pipython.pitools import piwrite
import pipython.pidevice.gcs30.gcs30error as gcs30erors
from signtools import signfile

__version__ = '1.1.0.9'
__signature__ = 0xb2d818eb32ae35a9b36dd4f23c3f8af7

INFILE = r'.\Error.json'
OUTFILE = r'.\pipython\pidevice\gcs30\CustomError.json'


# Custom json generator that keeps lists inline:
def to_json(o, level=0, INDENT = 4):
    SPACE = " "
    NEWLINE = "\n"
    ret = ""
    if isinstance(o, dict):
        ret += "{" + NEWLINE
        comma = ""
        for k, v in o.items():
            ret += comma
            comma = ",\n"
            ret += SPACE * INDENT * (level + 1)
            ret += '"' + str(k) + '":' + SPACE
            ret += to_json(v, level + 1,INDENT)
        ret += NEWLINE + SPACE * INDENT * level + "}"
    elif isinstance(o, str):
        ret += '"' + o + '"'
    elif isinstance(o, list):
        ret += "[" + ",".join([to_json(e, level + 1,INDENT) for e in o]) + "]"
    # Tuples are interpreted as lists
    elif isinstance(o, tuple):
        ret += "[" + ",".join(to_json(e, level + 1,INDENT) for e in o) + "]"
    elif isinstance(o, bool):
        ret += "true" if o else "false"
    elif isinstance(o, int):
        ret += str(o)
    elif isinstance(o, float):
        ret += '%.7g' % o
    elif isinstance(o, numpy.ndarray) and numpy.issubdtype(o.dtype, numpy.integer):
        ret += "[" + ','.join(map(str, o.flatten().tolist())) + "]"
    elif isinstance(o, numpy.ndarray) and numpy.issubdtype(o.dtype, numpy.inexact):
        ret += "[" + ','.join(map(lambda x: '%.7g' % x, o.flatten().tolist())) + "]"
    elif o is None:
        ret += 'null'
    else:
        raise TypeError("Unknown type '%s' for json serialization" % str(type(o)))
    return ret

# Create an error json without the PI internal usage elements
def makeReducedErrorJson(errJsonInFile: str, errJsonOutFile: str):
    print('Generating Reduced Error Json')
    with open(errJsonInFile, 'r+') as err_json_file:
        errorJson = json.load(err_json_file)
        keysToKeep = ('id','module','class', 'description')
        errDefs = [str(err) for err in errorJson['errors']]
        for errDef in errDefs:
            keys = list(errorJson['errors'][errDef].keys())
            for key in keys:
                if key not in keysToKeep:
                    del errorJson['errors'][errDef][key]
            #Remove errors that are only for debug and deprecated  errors (id= -1)

            user_error = True
            if gcs30erors.PI_GCS30_ERRORS_ID_KEY in errorJson['errors'][errDef]:
                    if errorJson['errors'][errDef]['id'] == -1:
                        user_error = False
            else:
                if (':' in errorJson['errors'][errDef]) and (int(errorJson['errors'][errDef].split(':')[0]) == -1):
                        user_error = False

            classes = list(errorJson['errors'][errDef]['class'])
            if not user_error:
                del errorJson['errors'][errDef]
                continue
            #Replace $MODULE with actual module alias
            module = errorJson['errors'][errDef]['module']
            moduleAlias = errorJson['modules'][module]['alias']
            newErrDef = str(errDef).replace('$MODULE', moduleAlias)
            errorJson['errors'][newErrDef] = errorJson['errors'].pop(errDef)

        # json.dump(json_file,open("Error_gen.json","w"),indent=4)
        output = to_json(errorJson) # custom formatter to inline lists
        os.remove(errJsonOutFile)
        with open(errJsonOutFile, 'w+') as file:
            file.write(output)

def create():
    """Update error definitions and sign OUTILE."""
    makeReducedErrorJson(INFILE, OUTFILE)


if __name__ == '__main__':
    create()