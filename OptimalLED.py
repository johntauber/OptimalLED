import numpy as np
import pandas as pd
from itertools import combinations

empirical = pd.read_csv('empirical_intensity.csv', header=None)
empirical = np.array(empirical)
empirical = empirical.squeeze()

x = np.arange(2.5, 50, 5)
y = np.arange(2.5, 50, 5)
x_coords, y_coords = np.meshgrid(x, y)
grid = np.array([y_coords, x_coords])


# helper functions
def int2grid(integer):
    gridmap = np.arange(1, 101).reshape(10, 10)
    return np.where(np.isin(gridmap, integer))


def get_intensity(angle, d2i_map):
    if angle > 40:
        return 0
    else:
        approx_angle = np.round(angle)
        return d2i_map[int(approx_angle)]


# Generate intensity grid library

height = 40
intensity_library = np.zeros((10, 10, 10, 10))
for x in range(10):
    for y in range(10):
        intensities = np.zeros((10, 10))
        x_0 = grid[:, x, y]
        for i in range(10):
            for j in range(10):
                norm = np.linalg.norm(grid[:, i, j] - x_0)
                angle = np.degrees(np.arctan(norm / height))
                intensities[i, j] = get_intensity(angle, empirical)
        intensity_library[x, y, :] = intensities

# Iterate through all possible LED position combinations to find best intensity grid
x = [x for x in range(1, 101)]
optimal_variance = {}
optimal_mean = {}
i = 0
for comb in combinations(x, 5):
    #    i += 1
    #    if i >= 100:
    #        break
    summed = np.zeros((10, 10))
    for led in comb:
        x, y = int2grid(led)
        summed += intensity_library[int(x), int(y), :, :]

    if not optimal_variance:
        optimal_variance['array'] = summed
        optimal_variance['var'] = summed.var()
        optimal_variance['combination'] = comb

        optimal_mean['array'] = summed
        optimal_mean['mean'] = summed.mean()
        optimal_mean['combination'] = comb

    if summed.var() < optimal_variance['var']:
        optimal_variance['array'] = summed
        optimal_variance['var'] = summed.var()
        optimal_variance['combination'] = comb

    if summed.mean() > optimal_mean['mean']:
        optimal_mean['array'] = summed
        optimal_mean['mean'] = summed.mean()
        optimal_mean['combination'] = comb