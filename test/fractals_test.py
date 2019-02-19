import unittest
from bin.math.algorithm.fractal.mandelbrot import *
from bin.math.algorithm.fractal.julia import *
from PIL import Image

class TestAlgorithm(unittest.TestCase):

    def __test_mandelbrot(self):
        size = 512
        ms = MandelbrotSet(size,size, complex(-2.0, -1.0), complex(0.5, 1.0))
        ms.create()
        rgb_array = MandelbrotSetConverter(ms).to_rgb_array(mandelbrot_color_line_int_rgb)
        im = Image.new('RGB', (size, size), 'black')
        pixels = im.load()
        for y in range(size):
            y_ = y * size * 3
            for x in range(size):
                idx = y_ + (x*3)
                pixels[x,y] = (int(rgb_array[idx]), int(rgb_array[idx+1]), int(rgb_array[idx+2]))

        im.save("test_mandelbrot.png")

    def test_julia(self):
        size = 512
        c = complex(0., 1.)
        ms = JuliaSet(size,size, complex(-1.1, -1.1), complex(1.1, 1.1), c, julia_pfunc_quad_plus_c)
        ms.set_cntiterations(200)
        ms.create()
        rgb_array = JuliaSetConverter(ms).to_rgb_array(julia_color_line_int_8_bit_2)
        im = Image.new('RGB', (size, size), 'black')
        pixels = im.load()
        for y in range(size):
            y_ = y * size * 3
            for x in range(size):
                idx = y_ + (x*3)
                pixels[x,y] = (int(rgb_array[idx]), int(rgb_array[idx+1]), int(rgb_array[idx+2]))

        im.save("test_julia.png")