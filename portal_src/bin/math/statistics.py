import math

one_to_three = 1./3.

def middle_arithmetic(x1:float, x2:float, x3:float, x4:float) -> float:
    return (x1 + x2 + x3 + x4) * 0.25


def middle_arithmetic2(x1:float, x2) -> float:
    return (x1 + x2) * 0.5

def middle_harmonic(x1:float, x2:float, x3:float, x4:float) -> float:
    return 4. / (1. / x1 + 1. / x2 + 1. / x3 + 1. / x4)


def middle_harmonic2(x1:float, x2) -> float:
    return 2. / (1. / x1 + 1. / x2)


def middle_quantil(x1:float, x2:float, x3:float, x4:float) -> float:
    values = [x1, x2, x3, x4]
    values.sort()
    return (values[0] + values[2]) / 2.


def middle_median(x1:float, x2:float, x3:float, x4:float) -> float:
    values = [x1, x2, x3, x4]
    values.sort()
    return (values[1] + values[2]) / 2.


def middle_quad(x1:float, x2:float, x3:float, x4:float) -> float:
    return math.sqrt(((x1 * x1) + (x2 * x2) + (x3 * x3) + (x4 * x4)) * 0.25)


def middle_quad2(x1:float, x2) -> float:
    return math.sqrt(((x1 * x1) + (x2 * x2)) * 0.5)


def middle_cubic(x1:float, x2:float, x3:float, x4:float) -> float:
    return (((x1 * x1 * x1) + (x2 * x2 * x2) + (x3 * x3 * x3) + (x4 * x4 * x4)) * 0.25) ** one_to_three


def middle_cubic2(x1:float, x2) -> float:
    return (((x1 * x1 * x1) + (x2 * x2 * x2)) * 0.5) ** one_to_three


def middle_geometric(x1:float, x2:float, x3:float, x4:float) -> float:
    return (x1 * x2 * x3 * x4) ** 0.25


def middle_geometric2(x1:float, x2) -> float:
    return (x1 * x2) ** 0.5


def middle_hoelder(x1:float, x2:float, x3:float, x4:float) -> float:
    return (((x1 * x1 * x1 * x1) + (x2 * x2 * x2 * x2) + (x3 * x3 * x3 * x3) + (x4 * x4 * x4 * x4)) * 0.25) ** 0.25


def middle_hoelder2(x1:float, x2) -> float:
    return (((x1 * x1) + (x2 * x2)) * 0.5) ** 0.5
