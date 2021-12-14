import numpy as np


def create_even_number_of_particles(num_particles, dimension, seed=17657):
    if num_particles % 2 != 0:
        raise ValueError('num_particles must be even')

    np.random.seed(seed)
    return [[np.random.random() for i in range(dimension)] for j in range(num_particles)]
