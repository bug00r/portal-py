class BaseNode(object):
    """
        Every Node have to inherit from this in reason of an easier access to performance critical methods
    """
    def __init__(self):
        self._lib = None

    def set_lib(self, lib):
        self._lib = lib