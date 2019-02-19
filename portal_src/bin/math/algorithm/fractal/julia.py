from typing import Callable
import array
from portal_src.bin.math.utils import interpolate_lin
import cmath

class FractalPoint(object):
    def __init__(self, cpoint_, spoint_, abs_, iterations_, isin_):
        self.cpoint = cpoint_
        self.spoint = spoint_
        self.abs = abs_
        self.iterations = iterations_
        self.isin = isin_

class JuliaSet(object):
    def __init__(self, width: int, height:int, min:complex, max:complex, constant: complex,
                 polyfunc: Callable[[complex, complex], complex]):
        self.__map = [FractalPoint(cpoint_=complex(),
                                   spoint_=complex(),
                                   abs_=0.0, iterations_=0, isin_=False) for i in range(width * height)]
        self.__min = min
        self.__max = max
        self.__width = width
        self.__height = height
        self.__cntiterations = 20
        self.__polyfunc = polyfunc
        self.__c = constant

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

    def constant(self):
        return self.__c

    def polyfunc(self):
        return self.__polyfunc

    def set_min(self, min: complex):
        self.__min = min

    def set_max(self, max_: complex):
        self.__max = max_

    def set_cntiterations(self, its: int):
        self.__cntiterations = its

    def set_constant(self, c_: complex):
        self.__c = c_

    def set_polyfunc(self, polyfunc: Callable[[complex, complex], complex]):
        self.__polyfunc = polyfunc

    def __inside_julia(self, p_real, p_imag, result: FractalPoint):
        cur_complex = complex(p_real, p_imag)
        curabs = 0.0
        inside = True
        needed_i = 0

        for i in range(1,self.__cntiterations+1):
            needed_i = i
            cur_complex = self.__polyfunc(cur_complex, self.__c)
            curabs = abs(cur_complex)
            if curabs > 2:
                inside = False
                break

        result.cpoint = cur_complex
        result.spoint = complex(p_real, p_imag)
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
                self.__inside_julia(cur_real, cur_imag , self.__map[curh * mwidth + curw])
                cur_real += step.real
            cur_real = self.__min.real
            cur_imag += step.imag


def julia_color_line_int_rgb(mb: JuliaSet, mbt: FractalPoint):
    if not mbt.isin:
        cpabs = mbt.iterations / mb.cntiterations() *0.2
        return cpabs * 255, 0, 0
    else:
        return 0,0,0

def julia_color_line_int_8_bit(mb: JuliaSet, mbt: FractalPoint):
    if not mbt.isin:
        colfactor_real = interpolate_lin(mbt.spoint.real, mb.min().real, 0., mb.max().real, 255.) / 255.
        colfactor_imag = interpolate_lin(mbt.spoint.imag, mb.min().real, 0., mb.max().real, 255.) / 255.
        return ( interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.18, 255.) * colfactor_real,
                 interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.18, 255.) * ((colfactor_real + colfactor_imag)/8.),
                 interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.18, 255.) * colfactor_imag)
    else:
        return ( interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.3, 255.),
		         interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.2, 255.),
                 interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.1, 255.) )

def julia_color_line_int_8_bit_2(mb: JuliaSet, mbt: FractalPoint):
    if not mbt.isin:
        colfactor_real = interpolate_lin(mbt.spoint.real, mb.min().real, 0., mb.max().real, 255.) / 255.
        colfactor_imag = interpolate_lin(mbt.spoint.imag, mb.min().real, 0., mb.max().real, 255.) / 255.
        return ( interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.18, 255.) * colfactor_real,
                 interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.18, 255.) * ((colfactor_real + colfactor_imag)/8.),
                 interpolate_lin(mbt.iterations, 0., 0., mb.cntiterations() * 0.18, 255.) * colfactor_imag)
    else:
        return 0, 0, 0

class JuliaSetConverter(object):
    def __init__(self, juzliase: JuliaSet):
        self.__mbset = juzliase

    def to_rgb_array(self, color_func: Callable[[JuliaSet, FractalPoint], tuple]):
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

def julia_pfunc_quad_plus_c(cp: complex, c: complex) -> complex:
  return cp**2 + c

def julia_pfunc_third_plus_c(cp: complex, c: complex) -> complex:
    return cp**3 + c

def julia_pfunc_fourth_plus_c(cp: complex, c: complex) -> complex:
    return cp**4+ c

def julia_pfunc_exp_plus_c(cp: complex, c: complex) -> complex:
    return cmath.exp(cp**3) - c

def julia_pfunc_ten_plus_c(cp: complex, c: complex) -> complex:
    return cp**10 + c

def julia_pfunc_quad_plus_c_2(cp: complex, c: complex) -> complex:
    pow2_z = cp * cp
    return (pow2_z + c) / (pow2_z - c)

def julia_pfunc_quad_plus_c_1_2(cp: complex, c: complex) -> complex:
    pow2_z = cp**2
    return (pow2_z - c) / (pow2_z + c)

def julia_pfunc_sqrt_plus_c(cp: complex, c: complex) -> complex:
    return cmath.sqrt(cp) + c

def julia_pfunc_sqrt_minus_c(cp: complex, c: complex) -> complex:
    return cmath.sqrt(cp) - c

def julia_pfunc_quad_plus_c_3(cp: complex, c: complex) -> complex:
    pow3_z = cp**3
    return (pow3_z + c) / (pow3_z - c)

def julia_pfunc_3_2_div_pc(cp: complex, c: complex) -> complex:
    pow2 = cp**2
    pow3 = pow2 * cp
    calc = (cp - (pow2 / 2.)) * (cp - (pow2 / 2.))
    return ((1. - (pow3/6.)) / calc) + c

def julia_pfunc_pow_3_p_2_p_1_p_c(cp: complex, c: complex) -> complex:
    pow2 = cp**2
    pow3 = pow2 * cp
    return pow3 + pow2 + cp + c

