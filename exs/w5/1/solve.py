# coding: utf-8
def solve(arr):
    import numpy as np
    total_tails = np.sum(arr)
    total_tosses = len(arr) * 20
    probability_tails = total_tails / total_tosses
    return probability_tails
