import unittest

from portal_src.bin.app import ExtensionManager
from pathlib import Path
import os

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        path = os.path.join( os.path.dirname(os.path.realpath(__file__)), "..", "..", "ext")
        mgr = ExtensionManager(Path(path).resolve())
        mgr.get('_portal_')
        mgr.get('_portal_')
        mgr.get('_portal_')

