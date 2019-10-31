# -*- coding: utf-8 -*-
import os
import sys

try:
    import pkg_resources

    get_module_res = lambda *res: pkg_resources.resource_stream(__name__,
                                                                os.path.join(*res))
except ImportError:
    get_module_res = lambda *res: open(os.path.normpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__), *res)), 'rb')


def resolve_filename(f):
    try:
        return f.name
    except AttributeError:
        return repr(f)
