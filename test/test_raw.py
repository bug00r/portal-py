from portal_src.bin.math.algorithm.noise import MidpointDisplacement, DiamondSquare
from PIL import Image
import numpy as np

size = 513
md = MidpointDisplacement(size, size)
md.create()
noiseinter = md.interpolate(0, 255, int)
col_array = np.array(noiseinter, dtype=np.uint8).reshape((size, size), order='F')
im = Image.fromarray(col_array, 'L')
im.save("test.bmp")