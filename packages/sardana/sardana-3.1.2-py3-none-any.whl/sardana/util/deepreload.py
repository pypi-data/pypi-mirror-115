# -*- coding: utf-8 -*-

##############################################################################
##
# This file is part of Sardana
##
# http://www.sardana-controls.org/
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Sardana is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Sardana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""
A module to change reload() so that it acts recursively.
To enable it type::

    import __builtin__, deepreload
    __builtin__.reload = deepreload.reload

You can then disable it with::

    __builtin__.reload = deepreload.original_reload

Alternatively, you can add a dreload builtin alongside normal reload with::

    __builtin__.dreload = deepreload.reload

This code is almost entirely based on knee.py, which is a Python
re-implementation of hierarchical module import.
"""

import builtins
from contextlib import contextmanager
import imp
import sys

from types import ModuleType
from warnings import warn

original_import = builtins.__import__


class DeepReload(object):

    def __enter__(self):
        builtins.reload = reload

    def __exit__(self, etype, evalue, etraceback):
        builtins.reload = original_reload


@contextmanager
def replace_import_hook(new_import):
    saved_import = builtins.__import__
    builtins.__import__ = new_import
    try:
        yield
    finally:
        builtins.__import__ = saved_import


def get_parent(globals, level):
    """
    parent, name = get_parent(globals, level)

    Return the package that an import is being performed in.  If globals comes
    from the module foo.bar.bat (not itself a package), this returns the
    sys.modules entry for foo.bar.  If globals is from a package's __init__.py,
    the package's entry in sys.modules is returned.

    If globals doesn't come from a package or a module in a package, or a
    corresponding entry is not found in sys.modules, None is returned.
    """
    orig_level = level

    if not level or not isinstance(globals, dict):
        return None, ''

    pkgname = globals.get('__package__', None)

    if pkgname is not None:
        # __package__ is set, so use it
        if not hasattr(pkgname, 'rindex'):
            raise ValueError('__package__ set to non-string')
        if len(pkgname) == 0:
            if level > 0:
                raise ValueError('Attempted relative import in non-package')
            return None, ''
        name = pkgname
    else:
        # __package__ not set, so figure it out and set it
        if '__name__' not in globals:
            return None, ''
        modname = globals['__name__']

        if '__path__' in globals:
            # __path__ is set, so modname is already the package name
            globals['__package__'] = name = modname
        else:
            # Normal module, so work out the package name if any
            lastdot = modname.rfind('.')
            if lastdot < 0 and level > 0:
                raise ValueError("Attempted relative import in non-package")
            if lastdot < 0:
                globals['__package__'] = None
                return None, ''
            globals['__package__'] = name = modname[:lastdot]

    dot = len(name)
    for x in range(level, 1, -1):
        try:
            dot = name.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                             "package")
    name = name[:dot]

    try:
        parent = sys.modules[name]
    except:
        if orig_level < 1:
            warn("Parent module '%.200s' not found while handling absolute "
                 "import" % name)
            parent = None
        else:
            raise SystemError("Parent module '%.200s' not loaded, cannot "
                              "perform relative import" % name)

    # We expect, but can't guarantee, if parent != None, that:
    # - parent.__name__ == name
    # - parent.__dict__ is globals
    # If this is violated...  Who cares?
    return parent, name


def load_next(mod, altmod, name, buf):
    """
    mod, name, buf = load_next(mod, altmod, name, buf)

    altmod is either None or same as mod
    """

    if len(name) == 0:
        # completely empty module name should only happen in
        # 'from . import' (or '__import__("")')
        return mod, None, buf

    dot = name.find('.')
    if dot == 0:
        raise ValueError('Empty module name')

    if dot < 0:
        subname = name
        next = None
    else:
        subname = name[:dot]
        next = name[dot + 1:]

    if buf != '':
        buf += '.'
    buf += subname

    result = import_submodule(mod, subname, buf)
    if result is None and mod != altmod:
        result = import_submodule(altmod, subname, subname)
        if result is not None:
            buf = subname

    if result is None:
        raise ImportError("No module named %.200s" % name)

    return result, next, buf

# Need to keep track of what we've already reloaded to prevent cyclic evil
found_now = {}


def import_submodule(mod, subname, fullname):
    """m = import_submodule(mod, subname, fullname)"""
    # Require:
    # if mod == None: subname == fullname
    # else: mod.__name__ + "." + subname == fullname

    global found_now
    if fullname in found_now and fullname in sys.modules:
        m = sys.modules[fullname]
    else:
        print('Reloading', fullname)
        found_now[fullname] = 1
        oldm = sys.modules.get(fullname, None)

        if mod is None:
            path = None
        elif hasattr(mod, '__path__'):
            path = mod.__path__
        else:
            return None

        try:
            # This appears to be necessary on Python 3, because imp.find_module()
            # tries to import standard libraries (like io) itself, and we don't
            # want them to be processed by our deep_import_hook.
            with replace_import_hook(original_import):
                fp, filename, stuff = imp.find_module(subname, path)
        except ImportError:
            return None

        try:
            m = imp.load_module(fullname, fp, filename, stuff)
        except:
            # load_module probably removed name from modules because of
            # the error.  Put back the original module object.
            if oldm:
                sys.modules[fullname] = oldm
            raise
        finally:
            if fp:
                fp.close()

        add_submodule(mod, m, fullname, subname)

    return m


def add_submodule(mod, submod, fullname, subname):
    """mod.{subname} = submod"""
    if mod is None:
        return  # Nothing to do here.

    if submod is None:
        submod = sys.modules[fullname]

    setattr(mod, subname, submod)

    return


def ensure_fromlist(mod, fromlist, buf, recursive):
    """Handle 'from module import a, b, c' imports."""
    if not hasattr(mod, '__path__'):
        return
    for item in fromlist:
        if not hasattr(item, 'rindex'):
            raise TypeError("Item in ``from list'' not a string")
        if item == '*':
            if recursive:
                continue  # avoid endless recursion
            try:
                all = mod.__all__
            except AttributeError:
                pass
            else:
                ret = ensure_fromlist(mod, all, buf, 1)
                if not ret:
                    return 0
        elif not hasattr(mod, item):
            import_submodule(mod, item, buf + '.' + item)


def deep_import_hook(name, globals=None, locals=None, fromlist=None, level=-1):
    """Replacement for __import__()"""
    parent, buf = get_parent(globals, level)

    head, name, buf = load_next(
        parent, None if level < 0 else parent, name, buf)

    tail = head
    while name:
        tail, name, buf = load_next(tail, tail, name, buf)

    # If tail is None, both get_parent and load_next found
    # an empty module name: someone called __import__("") or
    # doctored faulty bytecode
    if tail is None:
        raise ValueError('Empty module name')

    if not fromlist:
        return head

    ensure_fromlist(tail, fromlist, buf, 0)
    return tail

modules_reloading = {}


def deep_reload_hook(m):
    """Replacement for reload()."""
    if not isinstance(m, ModuleType):
        raise TypeError("reload() argument must be module")

    name = m.__name__

    if name not in sys.modules:
        raise ImportError("reload(): module %.200s not in sys.modules" % name)

    global modules_reloading
    try:
        return modules_reloading[name]
    except:
        modules_reloading[name] = m

    dot = name.rfind('.')
    if dot < 0:
        subname = name
        path = None
    else:
        try:
            parent = sys.modules[name[:dot]]
        except KeyError:
            modules_reloading.clear()
            raise ImportError(
                "reload(): parent %.200s not in sys.modules" % name[:dot])
        subname = name[dot + 1:]
        path = getattr(parent, "__path__", None)

    try:
        # This appears to be necessary on Python 3, because imp.find_module()
        # tries to import standard libraries (like io) itself, and we don't
        # want them to be processed by our deep_import_hook.
        with replace_import_hook(original_import):
            fp, filename, stuff = imp.find_module(subname, path)
    finally:
        modules_reloading.clear()

    try:
        newm = imp.load_module(name, fp, filename, stuff)
    except:
        # load_module probably removed name from modules because of
        # the error.  Put back the original module object.
        sys.modules[name] = m
        raise
    finally:
        if fp:
            fp.close()

    modules_reloading.clear()
    return newm

# Save the original hooks
try:
    original_reload = builtins.reload
except AttributeError:
    original_reload = imp.reload    # Python 3

# Replacement for reload()


def reload(module, exclude=['sys', 'os.path', '__builtin__', '__main__']):
    """Recursively reload all modules used in the given module.  Optionally
    takes a list of modules to exclude from reloading.  The default exclude
    list contains sys, __main__, and __builtin__, to prevent, e.g., resetting
    display, exception, and io hooks.
    """
    global found_now
    for i in exclude:
        found_now[i] = 1
    try:
        with replace_import_hook(deep_import_hook):
            ret = deep_reload_hook(module)
    finally:
        found_now = {}
    return ret

# Uncomment the following to automatically activate deep reloading whenever
# this module is imported
#__builtin__.reload = reload
