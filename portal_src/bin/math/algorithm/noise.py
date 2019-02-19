import array
import random
from portal_src.bin.math.statistics import *
from portal_src.bin.math.utils import interpolate_lin

def seed_reduction_add(seed: float, reduction: float) -> float :
    return seed + reduction

def seed_reduction_sub(seed: float, reduction: float) -> float :
    return seed - reduction

def seed_reduction_mul(seed: float, reduction: float) -> float :
    return seed * reduction

def seed_reduction_div(seed: float, reduction: float) -> float :
    return seed / reduction

def seed_reduction_add_sqrt(seed: float, reduction: float) -> float :
    return seed + math.sqrt(reduction)

def seed_reduction_sub_sqrt(seed: float, reduction: float) -> float :
    return seed - math.sqrt(reduction)

def seed_reduction_mul_sqrt(seed: float, reduction: float) -> float :
    return seed * math.sqrt(reduction)

def seed_reduction_div_sqrt(seed: float, reduction: float) -> float :
    return seed / math.sqrt(reduction)

def seed_reduction_pow2_p_r_div_pow2_m_r(seed: float, reduction: float) -> float :
    return seed * (((seed**2) + reduction)/((seed**2) - reduction))

def seed_reduction_pow2_m_r_div_pow2_p_r(seed: float, reduction: float) -> float :
    return seed * (((seed**2) - reduction)/((seed**2) + reduction))

def seed_reduction_arithmetic_add( seed: float,  reduction: float) -> float :
    return seed + middle_arithmetic2(seed, reduction)

def seed_reduction_arithmetic_sub( seed: float,  reduction: float) -> float :
    return seed - middle_arithmetic2(seed, reduction)

def seed_reduction_arithmetic_mul( seed: float,  reduction: float) -> float :
    return seed * middle_arithmetic2(seed, reduction)

def seed_reduction_arithmetic_div( seed: float,  reduction: float) -> float :
    return seed / middle_arithmetic2(seed, reduction)

def seed_reduction_hoelder_add( seed: float,  reduction: float) -> float :
    return seed + middle_hoelder2(seed, reduction)

def seed_reduction_hoelder_sub( seed: float,  reduction: float) -> float :
    return seed - middle_hoelder2(seed, reduction)

def seed_reduction_hoelder_mul( seed: float,  reduction: float) -> float :
    return seed * middle_hoelder2(seed, reduction)

def seed_reduction_hoelder_div( seed: float,  reduction: float) -> float :
    return seed / middle_hoelder2(seed, reduction)

def seed_reduction_geometric_add( seed: float,  reduction: float) -> float :
    return seed + middle_geometric2(seed, reduction)

def seed_reduction_geometric_sub( seed: float,  reduction: float) -> float :
    return seed - middle_geometric2(seed, reduction)

def seed_reduction_geometric_mul( seed: float,  reduction: float) -> float :
    return seed * middle_geometric2(seed, reduction)

def seed_reduction_geometric_div( seed: float,  reduction: float) -> float :
    return seed / middle_geometric2(seed, reduction)

def seed_reduction_cubic_add( seed: float,  reduction: float) -> float :
    return seed + middle_cubic2(seed, reduction)

def seed_reduction_cubic_sub( seed: float,  reduction: float) -> float :
    return seed - middle_cubic2(seed, reduction)

def seed_reduction_cubic_mul( seed: float,  reduction: float) -> float :
    return seed * middle_cubic2(seed, reduction)

def seed_reduction_cubic_div( seed: float,  reduction: float) -> float :
    return seed / middle_cubic2(seed, reduction)

def seed_reduction_quad_add( seed: float,  reduction: float) -> float :
    return seed + middle_quad2(seed, reduction)

def seed_reduction_quad_sub( seed: float,  reduction: float) -> float :
    return seed - middle_quad2(seed, reduction)

def seed_reduction_quad_mul( seed: float,  reduction: float) -> float :
    return seed * middle_quad2(seed, reduction)

def seed_reduction_quad_div( seed: float,  reduction: float) -> float :
    return seed / middle_quad2(seed, reduction)

def seed_reduction_harmonic_add( seed: float,  reduction: float) -> float :
    return seed + middle_harmonic2(seed, reduction)

def seed_reduction_harmonic_sub( seed: float,  reduction: float) -> float :
    return seed - middle_harmonic2(seed, reduction)

def seed_reduction_harmonic_mul( seed: float,  reduction: float) -> float :
    return seed * middle_harmonic2(seed, reduction)

def seed_reduction_harmonic_div( seed: float,  reduction: float) -> float :
    return seed / middle_harmonic2(seed, reduction)

class Noise(object):
    def __init__(self, width: int, height: int):
        self.__size = (width, height)
        self.__map = array.array('f',(0.0,)*(self.__size[0]*self.__size[1]))
        self.__min = float("inf")
        self.__max = float("-inf")

    def reset(self):
        self.__max = float("-inf")
        self.__min = float("inf")

    def new_val(self, min_: float, max_: float) -> float:
        val = random.uniform(min_, max_)
        self.__min = min(self.__min, val)
        self.__max = max(self.__max, val)
        return val

    def set_newval_at_idx(self, index:int, min_: float, max_: float):
        self.__map[index] = self.new_val(min_, max_)

    def set_val_at_idx(self, index:int, _val: float):
        self.__map[index] = _val

    def size(self):
        return self.__size

    def map(self):
        return self.__map

    def min(self):
        return self.__min

    def set_min(self, min: float):
        self.__min = min

    def max(self):
        return self.__max

    def set_max(self, max: float):
        self.__max = max


class DsBase(object):
   def __init__(self, width: int, height: int):
        self._noise = Noise(width, height)
        self._length = width - 1
        self._startseed = 1.0
        self._seed = 1.0
        self._reduction = 0.5
        self._middlefunc = middle_arithmetic
        self._seedreducefunc = seed_reduction_mul

   def interpolate(self, int_min, int_max):
        min_ = self._noise.min()
        max_ = self._noise.max()
        return [ interpolate_lin(x, min_, int_min, max_, int_max) for x in self._noise.map()]

   def noise(self):
       return self._noise

class MdBase(DsBase):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self._middlefunc2 = middle_arithmetic2


class MidpointDisplacement(MdBase):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    def create(self):
        startseed = self._startseed
        seed = self._seed
        length = self._length
        noise = self._noise
        noise_array = self._noise.map()
        noise_width  = self._noise.size()[0]
        cntsquare = int((noise_width - 1) / length)
        middle = length >> 1
        middlefunc = self._middlefunc
        middlefunc2 = self._middlefunc2
        seedreducefunc = self._seedreducefunc

        if cntsquare == 1:
            self._noise.set_newval_at_idx(0, -startseed, startseed)
            self._noise.set_newval_at_idx(length, -startseed, startseed)
            self._noise.set_newval_at_idx(length*length + length, -startseed, startseed)
            self._noise.set_newval_at_idx(length*length + (2*length), -startseed, startseed)

        l_nw = length * noise_width
        m_nw = middle * noise_width
        min_ = noise.min()
        max_ = noise.max()
        for sqy in range(0,cntsquare):
            y = (sqy * length) + middle
            sqy_l_nw = sqy * l_nw
            sqy_1 = sqy + 1
            sqy_1_l_nw = sqy_1 * l_nw
            y_nw = y * noise_width

            y_mm_nw = y_nw - m_nw
            y_pm_nw = y_nw + m_nw

            for sqx in range(0, cntsquare):
                sqx_l = sqx * length
                sqx_2 = sqx_l + length

                lt_val = noise_array[sqy_l_nw + sqx_l]
                rt_val = noise_array[sqy_l_nw + sqx_2]
                lb_val = noise_array[sqy_1_l_nw + sqx_l]
                rb_val = noise_array[sqy_1_l_nw + sqx_2]

                # middlepoint
                x = (sqx * length) + middle

                y_nw_x = y_nw + x
                y_nw_x_pm = y_nw_x + middle
                y_nw_x_mm = y_nw_x - middle
                y_mm_nw_px = y_mm_nw + x
                y_pm_nw_px = y_pm_nw + x

                rand = random.uniform(-seed, seed)

                colval = middlefunc2(lt_val, rt_val)
                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                noise_array[y_mm_nw_px] = colval

                colval = middlefunc2(lb_val, rb_val)
                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                noise_array[y_pm_nw_px] = colval

                colval = middlefunc2(lt_val, lb_val)
                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                noise_array[y_nw_x_mm] = colval

                colval = middlefunc2(rt_val, rb_val)
                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                noise_array[y_nw_x_pm] = colval


                colval = middlefunc( noise_array[y_mm_nw_px],
                                     noise_array[y_pm_nw_px],
                                     noise_array[y_nw_x_mm],
                                     noise_array[y_nw_x_pm])

                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                noise_array[y_nw_x] = colval

        noise.set_min(min_)
        noise.set_max(max_)

        if middle >= 2:
            #elf._seed = seed * self._reduction
            self._seed = seedreducefunc(seed, self._reduction)
            self._length = middle
            self.create()

class DiamondSquare(DsBase):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    def create(self):
        startseed = self._startseed
        seed = self._seed
        length = self._length
        noise = self._noise
        noise_array = self._noise.map()
        noise_width = self._noise.size()[0]
        maxidx = noise_width - 1
        usedwidth = maxidx
        maxidx *= maxidx
        cntsquare = int((noise_width - 1) / length)
        middle  = length >> 1
        middlefunc = self._middlefunc
        seedreducefunc = self._seedreducefunc

        if cntsquare == 1:
            self._noise.set_newval_at_idx(0, -startseed, startseed)
            self._noise.set_newval_at_idx(length, -startseed, startseed)
            self._noise.set_newval_at_idx(length*length + length, -startseed, startseed)
            self._noise.set_newval_at_idx(length*length + (2*length), -startseed, startseed)

        l_nw = length * noise_width
        min_ = noise.min()
        max_ = noise.max()
        for sqy in range(0,cntsquare):
            y = (sqy * length) + middle
            sqy_l_nw = sqy * l_nw
            sqy_1 = sqy + 1
            sqy_1_l_nw = sqy_1 * l_nw
            y_nw = y * noise_width
            for sqx in range(0, cntsquare):
                sqx_l = sqx * length
                sqx_2 = sqx_l + length

                lt = sqy_l_nw + sqx_l
                rt = sqy_l_nw + sqx_2
                lb = sqy_1_l_nw + sqx_l
                rb = sqy_1_l_nw + sqx_2

                # middlepoint
                x = (sqx * length) + middle
                y_nw_x = y_nw + x

                colval = (noise_array[lt] + noise_array[rt] + noise_array[lb] + noise_array[rb])*0.25
                colval += random.uniform(-seed, seed)
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                noise_array[y_nw_x] = colval

        for sqy in range(0,cntsquare):
            y = (sqy * length) + middle
            sqy_l_nw = sqy * l_nw
            sqy_1 = sqy + 1
            sqy_1_l_nw = sqy_1 * l_nw
            y_nw = y * noise_width
            for sqx in range(0, cntsquare):
                sqx_l = sqx * length
                sqx_2 = sqx_l + length

                lt_val = noise_array[sqy_l_nw + sqx_l]
                rt_val = noise_array[sqy_l_nw + sqx_2]
                lb_val = noise_array[sqy_1_l_nw + sqx_l]
                rb_val = noise_array[sqy_1_l_nw + sqx_2]

                # middlepoint
                x = (sqx * length) + middle
                y_nw_x = y_nw + x

                middleidx_val = noise_array[y_nw_x]

                # sidepoints
                # up
                y2 = y - length
                if y2 < 0.:
                    y2 += usedwidth

                rand = random.uniform(-seed, seed)

                colval = middlefunc(lt_val, rt_val, middleidx_val, noise_array[y2 * noise_width + x])
                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                y2 = y - middle
                noise_array[y2 * noise_width + x] = colval

                # down
                y2 = y + length
                if y2 > usedwidth:
                    y2 -= usedwidth


                colval = middlefunc(lb_val, rb_val, middleidx_val, noise_array[y2 * noise_width + x])
                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                y2 = y + middle
                noise_array[y2 * noise_width + x] = colval

                # left
                x2 = x - length
                if x2 < 0.:
                    x2 += usedwidth

                colval = middlefunc(lt_val, lb_val, middleidx_val, noise_array[y * noise_width + x2])
                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                x2 = x - middle
                noise_array[y * noise_width + x2] = colval

                # right
                x2 = x + length
                if x2 > usedwidth:
                    x2 -= usedwidth

                colval = middlefunc(rt_val, rb_val, middleidx_val, noise_array[y * noise_width + x2])
                colval += rand
                min_ = min(min_, colval)
                max_ = max(max_, colval)
                x2 = x + middle
                noise_array[y * noise_width + x2] = colval

        noise.set_min(min_)
        noise.set_max(max_)

        if middle >= 2:
            #elf._seed = seed * self._reduction
            self._seed = seedreducefunc(seed, self._reduction)
            self._length = middle
            self.create()