import numpy as np
def replace_odd(arr):
    arr[arr % 2 == 1] = -1
    return arr