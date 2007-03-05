'''
FictionBook2 -> TeX converter exceptions

Author: Vadim Zaliva <lord@crocodile.org>
'''


class Error(Exception):
    """ Base class for all FB2PDF exceptions """
    def __str__(self):
        return self.message

class TemporaryError(Error):
    """ Temporary error, document could be retried later."""

    def __init__(self, msg, nested=None):
        self.message = msg
        self.nested = nested
        
class PersistentError(Error):
    """ Persistent error, document could not be converted."""

    def __init__(self, msg, nested=None):
        self.message = msg
        self.nested = nested
