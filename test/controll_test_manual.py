import unittest

from portal_src.bin.control import MainController

class TestController(unittest.TestCase):

    def test_com(self):
        ctrl = MainController(None, None, None)
        for suffix in range(0,200):
            ctrl.submit("req{0}".format(suffix))
