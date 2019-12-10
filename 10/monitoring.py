import numpy as np
import sys
from pathlib import Path


asteroids = [[f for f in l] for l in Path(sys.argv[1]).read_text().splitlines()]
asteroids = np.array(asteroids)
print(asteroids)

best_count = 0
for oy in range(asteroids.shape[0]):
    for ox in range(asteroids.shape[1]):
        if asteroids[oy, ox] != '#':
            continue
        angles = []
        count = 0
        for y, row in enumerate(asteroids):
            for x, col in enumerate(row):
                if x == ox and y == oy:
                    continue
                if col == '#':
                    angle = np.angle(complex(oy - y, ox - x))
                    if angle in angles:
                        continue
                    count += 1
                    angles.append(angle)

        if count > best_count:
            best_count = count
            best = (ox, oy)
print(best, best_count)
