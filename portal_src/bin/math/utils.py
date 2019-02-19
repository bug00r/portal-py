def interpolate_lin(x: float, x0: float, f0: float, x1: float, f1: float) -> float:
    result = 0.

    if f0 != 0.0:
        result += f0 * ((x1 - x) / (x1 - x0))
    else:
        result = f0

    if f1 != 0.0:
        result += f1 * ((x - x0) / (x1 - x0))

    return result