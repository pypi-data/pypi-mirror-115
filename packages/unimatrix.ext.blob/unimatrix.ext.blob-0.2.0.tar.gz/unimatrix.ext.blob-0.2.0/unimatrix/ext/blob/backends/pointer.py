"""Declares :class:`Pointer`."""


class Pointer:
    """Represents a pointer to file."""
    __module__ = 'unimatrix.ext.backends'

    def __init__(self, provider):
        self.provider = provider
