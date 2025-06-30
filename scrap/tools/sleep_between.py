from random import uniform
from time import sleep

def sleep_between(min:int, max:int):
    if min > max or min < 0:
        raise ValueError("min and max must be positive")
    else:
        sleep(uniform(min, max))
