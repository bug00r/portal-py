import unittest
from portal_src.bin.math.algorithm.noise import MidpointDisplacement, DiamondSquare
from PIL import Image
import numpy as np

class TestAlgorithm(unittest.TestCase):

    def test_midpoint_displacement(self):
        size = 513
        md = MidpointDisplacement(size, size)
        md.create()
        noiseinter = md.interpolate(0, 255)
        col_array = np.array(noiseinter, dtype=np.uint8).reshape((size, size), order='F')
        im = Image.fromarray(col_array, 'L')
        im.save("test_md.png")

    def test_diamond_square(self):
        size = 513
        ds = DiamondSquare(size, size)
        ds.create()
        noiseinter = ds.interpolate(0, 255)
        col_array = np.array(noiseinter, dtype=np.uint8).reshape((size, size), order='F')
        im = Image.fromarray(col_array, 'L')
        im.save("test_ds.png")