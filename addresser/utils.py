import math
import numbers


def is_number(x):
    try:
        if x == math.inf or math.isnan(x):
            return False
    except TypeError:  # raised if x is not a number or NaN/inf
        pass

    if isinstance(x, numbers.Number):
        return True

    try:
        float(x)
    except ValueError:
        return False
    else:
        return True
