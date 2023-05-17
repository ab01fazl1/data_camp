import numpy as np

def p2p_distance(input):
    output = np.linalg.norm(input - input[:, np.newaxis], axis=2)
    return output