from itertools import product
import numpy as np
from pathlib import Path

X, M, A, S = map(ord, "XMAS")
filters = np.array(
    [
        [
            [M, 0, S],
            [0, A, 0],
            [M, 0, S],
        ],
        [
            [M, 0, M],
            [0, A, 0],
            [S, 0, S],
        ],
        [
            [S, 0, M],
            [0, A, 0],
            [S, 0, M],
        ],
        [
            [S, 0, S],
            [0, A, 0],
            [M, 0, M],
        ],
    ]
)

mask = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])

grid = np.array(
    [
        [(ord(x) if x != "X" else 0) for x in line]
        for line in Path("input").read_text().splitlines()
    ]
)

count = 0
for i, j in product(range(1, grid.shape[0] - 1), range(1, grid.shape[1] - 1)):
    patch = grid[i - 1 : i + 2, j - 1 : j + 2] * mask
    masked_patch = patch * mask
    for filter in filters:
        filtered = masked_patch == filter
        result = np.all(filtered, axis=(0, 1))
        count += result.sum()
print(count)
