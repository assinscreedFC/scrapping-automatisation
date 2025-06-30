from random import uniform

def sleep_between(min:int, max:int):
    if min > max or min < 0:
        raise ValueError("min and max must be positive")
    else:
        return uniform(min, max)
