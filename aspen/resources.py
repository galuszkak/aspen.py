from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import stat


__cache__ = dict()  # cache, keyed to filesystem path


class Entry(object):
    """An entry in the global resource cache.
    """
    __slots__ = ('fspath', 'mtime', 'resource')

    def __init__(self, fspath, mtime, resource):
        #: The filesystem path [string]
        self.fspath = fspath
        #: The timestamp of the last change [int]
        self.mtime = mtime
        #: The loaded resource [Static or Dynamic]
        self.resource = resource


def get(request_processor, fspath):
    """Given a RequestProcessor and a filesystem path, return a Resource object (with caching).
    """

    # Get a cache Entry object.
    entry = __cache__.get(fspath)

    # Process the resource.
    if not entry or request_processor.changes_reload:
        mtime = os.stat(fspath)[stat.ST_MTIME]
        if getattr(entry, 'mtime', None) != mtime:  # cache miss
            resource = load(request_processor, fspath)
            entry = __cache__[fspath] = Entry(fspath, mtime, resource)

    # Return
    # ======
    # The caller must take care to avoid mutating any context dictionary at
    # entry.resource.pages[0].

    return entry.resource


def load(request_processor, fspath):
    """Given a RequestProcessor and a filesystem path, return a Resource object (w/o caching).
    """

    Class = request_processor.get_resource_class(fspath)

    # Compute and instantiate a class.
    # ================================
    # An instantiated resource is compiled as far as we can take it.

    return Class(request_processor, fspath)
