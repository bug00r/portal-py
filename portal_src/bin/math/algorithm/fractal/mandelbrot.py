from typing import Callable
import array
from portal_src.bin.math.utils import interpolate_lin
import cmath


def dummy_function_for_cython_compilation(cp: complex, c: complex) -> complex:
    """
    PLEASE DO NOT REMOVE THIS FUNCTION. WE NEED HER TO COMPILE THIS PY WITH CYTHON!!!!!!
    :param cp: unused
    :param c: unused
    :return: unused
    """
    return cmath.exp(cp**3) - c


class FractalPoint(object):
    def __init__(self, cpoint_, spoint_, abs_, iterations_, isin_):
        self.cpoint = cpoint_
        self.spoint = spoint_
        self.abs = abs_
        self.iterations = iterations_
        self.isin = isin_

class MandelbrotSet(object):
    def __init__(self, width: int, height:int, min:complex, max:complex):
        self.__map = [ FractalPoint(cpoint_=complex(),
                                    spoint_=complex(),
                                    abs_=0.0, iterations_=0, isin_=False) for i in range(width*height)]
        self.__min = min
        self.__max = max
        self.__width = width
        self.__height = height
        self.__cntiterations = 20

    def min(self):
        return self.__min

    def max(self):
        return self.__max

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def map(self):
        return self.__map

    def cntiterations(self):
        return self.__cntiterations

    def set_min(self, min: complex):
        self.__min = min

    def set_max(self, max_: complex):
        self.__max = max_

    def set_cntiterations(self, its: int):
        self.__cntiterations = its

    def __isinside_mb(self, point_real, point_imag, result: FractalPoint):
        cur_complex = complex(0.0, 0.0)
        curabs = 0.0
        inside = True
        needed_i = 0
        point = complex(point_real, point_imag)
        its = self.__cntiterations+1
        for i in range(1,its):
            needed_i = i
            cur_complex = cur_complex**2 + point
            curabs = abs(cur_complex)
            if curabs > 2.0:
                inside = False
                break
        result.cpoint = cur_complex
        result.spoint = point
        result.abs = curabs
        result.iterations = needed_i
        result.isin = inside

    def create(self):
        cur_real = self.__min.real
        cur_imag = self.__min.imag
        mwidth = self.__width
        mheight = self.__height
        step = complex( (self.__max.real - self.__min.real ) / mwidth, (self.__max.imag - self.__min.imag ) / mheight )

        for curh in range(mheight):
            for curw in range(mwidth):
                self.__isinside_mb(cur_real, cur_imag , self.__map[curh * mwidth + curw])
                cur_real += step.real
            cur_real = self.__min.real
            cur_imag += step.imag


def mandelbrot_color_normal_8_bit(mb: MandelbrotSet, mbt: FractalPoint):
   if not mbt.isin:
        colfactor = 1./mbt.abs
        return colfactor * mb.min().real*255, colfactor * 255,0
   else:
        return 0, 0, 0


def mandelbrot_color_line_int_rgb(mb: MandelbrotSet, mbt: FractalPoint):
    if not mbt.isin:
        cpabs = (mbt.cpoint.real**2 + mbt.cpoint.imag**2)**0.5
        return ( interpolate_lin(cpabs, mb.min().real, 0., mb.max().real, 255.),
                 0,
                interpolate_lin(mbt.iterations, 0., 0.,  mb.cntiterations(), 255.))
    else:
        return ( interpolate_lin(mbt.cpoint.real, mb.min().real, 0., mb.max().imag, 255.),
		         interpolate_lin(mbt.cpoint.imag, mb.min().imag, 0., mb.max().real, 255.),
		         0 )

def mandelbrot_color_line_int_8_bit(mb: MandelbrotSet, mbt: FractalPoint):
    if not mbt.isin:
        cpabs = abs(mbt.spoint)
        return ( interpolate_lin(cpabs, mb.min().real, 0., mb.max().real, 255.),
                0,
                interpolate_lin(mbt.iterations, 0., 0.,  mb.cntiterations(), 255.))
    else:
        return ( interpolate_lin(mbt.cpoint.real, mb.min().real, 0., mb.max().real, 255.),
		         interpolate_lin(mbt.cpoint.imag, mb.min().imag, 0., mb.max().imag, 255.),
		         0 )

class MandelbrotSetConverter(object):
    def __init__(self, mandelbrotset: MandelbrotSet):
        self.__mbset = mandelbrotset

    def to_rgb_array(self, color_func: Callable[[MandelbrotSet, FractalPoint], tuple]):
        map = self.__mbset.map()
        width = self.__mbset.width()
        height = self.__mbset.height()
        buffsize = width*height*3

        result = array.array('f',(0.0,)*buffsize)

        for y in range(height):
            y_ = y * width
            y_3 = y_ * 3
            for x in range(width):
               idx = y_ + x
               r, g, b = color_func(self.__mbset, map[idx])
               col_idx = y_3 + (x*3)
               result[col_idx] = r
               result[col_idx+1] = g
               result[col_idx+2] = b

        return result
