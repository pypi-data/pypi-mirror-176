#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Provide tools for verifying modules with an according signature."""

from __future__ import print_function

import hashlib
from io import open  # Redefining built-in 'open' pylint: disable=W0622
from logging import debug, info, warning
import os
import sys

from piconnector.pitools import piwrite

__signature__ = 0x10303e1de60eeb9230d2978f2fe25a0b


def split_source(filepath):
    """Read source according to 'filepath' and split at "__version__" or "__signature__".
    @param filepath : Full path to source file to read with extensions ".py" or ".pyc".
    @return : Tuple (prehash, hash, posthash) of strings.
    """
    filepath = filepath.replace('.pyc', '.py').replace('.PYC', 'PY')
    src_pre = u''
    src_hash = u''
    src_post = u''
    pre_signature = True
    with open(filepath, 'r', encoding='utf-8', newline='\n') as fobj:
        for line in fobj:
            line = line.rstrip() + '\n'
            if line.startswith('__signature__'):
                src_hash = line.split('=')[1].strip()
                pre_signature = False
                continue
            if pre_signature:
                src_pre += line
            else:
                src_post += line
            if line.startswith('__version__'):
                pre_signature = False
    if pre_signature:  # if there is no "__version__" a new "__signature__" is put on the first line
        src_post = src_pre
        src_pre = u''
    return src_pre, src_hash, src_post


def increase_version(sourcecode):
    """Increase lowest digit of "__version__" - formatted x.x.x.x - by one increment.
    @param sourcecode : Source code as string.
    @return : Source code with modified "__version__" line with trailing linefeed.
    """
    lines = sourcecode.splitlines(True)  # keepends = True
    for i, _ in enumerate(lines):
        if lines[i].startswith('__version__'):
            version = lines[i].split('=')[1].strip().strip("'").strip('"')
            version = [int(x) for x in version.split('.')]
            version[3] += 1
            lines[i] = "__version__ = '%s'\n" % '.'.join(str(x) for x in version)
    return u''.join(lines)


# The except handler raises immediately pylint: disable=W0706
def verify_module_signature(modulename):
    """Verify current vs. saved signature of 'modulename' and log result.
    @param modulename : Unique module name as string.
    @return : True if signature is valid or 'modulename' is no longer in memory.
    """
    if modulename not in sys.modules or modulename.startswith('piconnector'):
        return True
    logname = os.path.basename(sys.modules[modulename].__file__) if modulename == '__main__' else modulename
    debug('verify_module_signature(modulename=%s)', logname)
    try:
        saved_signature = sys.modules[modulename].__signature__
    except AttributeError:
        warning('unsigned module %r', logname)
        return False
    except:
        raise
    src_pre, _, src_post = split_source(sys.modules[modulename].__file__)
    src_all = src_pre + src_post
    current_signature = int(hashlib.md5(src_all.encode('utf-8')).hexdigest(), base=16)
    if saved_signature != current_signature:
        warning('invalid signature in %r', logname)
        return False
    info('*sign*\t%s', logname)
    return True


def verify_all_signatures():
    """Verify signature of all according modules currently in memory."""
    verify_module_signature('__main__')
    modulenames = list(sys.modules)  # dictionary sys.modules could change size when running through loop
    for modulename in modulenames:
        if not in_signed_package(modulename):
            continue
        verify_module_signature(modulename)


def in_signed_package(modulename):
    """Return True if 'modulename' is within a signed packages.
    @param modulename : Unique module name as string.
    @return : True if 'modulename' is within a signed package.
    """
    if modulename not in sys.modules:
        return False
    packages = ('pitest', 'pitt', 'piconnector')
    try:
        for package in packages:
            if package in sys.modules[modulename].__file__.split(os.sep):
                return True
    except AttributeError:
        return False
    except:
        raise
    return False


def save_with_signature(filepath, src_pre, src_post):
    """Save source code and "__signature__" line to 'filepath'.
    @param filepath : Full path to source file to write.
    @param src_pre : Source code prior to "__signature__" line as string.
    @param src_post : Source code after "__signature__" line as string.
    """
    src_all = src_pre + src_post
    hashval = int(hashlib.md5(src_all.encode('utf-8')).hexdigest(), base=16)
    output = src_pre + u'__signature__ = 0x%x\n' % hashval + src_post
    piwrite(filepath, output)


def signfile(filepath):
    """Add/update "__signature__" and "__version__" in file 'filepath'.
    @param filepath : Full path to source file.
    """
    filepath = os.path.abspath(filepath)
    print('sign: %s' % filepath[-30:])
    src_pre, _, src_post = split_source(filepath)
    src_pre = increase_version(src_pre)
    save_with_signature(filepath, src_pre, src_post)


def incrementfileversion(filepath):
    """Add/update "__version__" in file 'filepath'.
    @param filepath : Full path to source file.
    """
    filepath = os.path.abspath(filepath)
    print('sign: %s' % filepath[-30:])
    src_pre, _, src_post = split_source(filepath)
    src_pre = increase_version(src_pre)
    piwrite(filepath, src_pre + src_post)


def verifyfile(filepath):
    """Compare calculated hash of 'filepath' with its "__signature__" value and print result.
    @param filepath : Full path to source file.
    """
    src_pre, hashsaved, src_post = split_source(filepath)
    try:
        hashsaved = int(hashsaved, base=16)
    except ValueError:
        hashsaved = 0
    src_all = src_pre + src_post
    hashcurrent = int(hashlib.md5(src_all.encode('utf-8')).hexdigest(), base=16)
    print('%sVALID signature: %s' % ('' if hashsaved == hashcurrent else 'IN', filepath[-30:]))
