import itertools
import numpy as np
from pathlib import Path

content = Path("example" if __debug__ else "input").read_text()

# content = """AAAA
# BBCD
# BBCC
# EEEC"""

# content = """OOOOO
# OXOXO
# OOOOO
# OXOXO
# OOOOO"""

# content = """EEEEE
# EXXXX
# EEEEE
# EXXXX
# EEEEE"""

# content = """AAAAAA
# AAABBA
# AAABBA
# ABBAAA
# ABBAAA
# AAAAAA"""

garden = np.array(list(map(list, content.splitlines())))


def perimeter(x: np.ndarray):
    padded = np.pad(x, 1, mode="empty")

    r = np.zeros_like(padded, dtype=int)
    for i, row in enumerate(x, 1):
        for j, cell in enumerate(row, 1):
            perim = 0
            perim += 1 if padded[i - 1, j] != cell else 0
            perim += 1 if padded[i + 1, j] != cell else 0
            perim += 1 if padded[i, j - 1] != cell else 0
            perim += 1 if padded[i, j + 1] != cell else 0
            r[i, j] = perim
    return r[1:-1, 1:-1]


def region(
    x: np.ndarray,
    ri: int,
    ci: int,
    val,
    mask: np.ndarray,
    visited: np.ndarray | None = None,
):
    if ri < 0 or ri >= x.shape[0]:
        return False
    if ci < 0 or ci >= x.shape[1]:
        return False
    if visited is None:
        visited = np.zeros_like(x, dtype=bool)
    if visited[ri, ci]:
        return False
    visited[ri, ci] = True
    mask[ri, ci] = x[ri, ci] == val
    for ro, co in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (
            ri + ro >= 0
            and ri + ro < x.shape[0]
            and ci + co >= 0
            and ci + co < x.shape[1]
            and x[ri + ro, ci + co] == val
        ):
            region(x, ri + ro, ci + co, val, mask, visited)
    return mask


def labels(x: np.ndarray):
    a = np.ones_like(x, dtype=int) * -1
    label = 0
    for i, j in itertools.product(range(x.shape[0]), range(x.shape[1])):
        if a[i, j] >= 0:
            continue
        mask = np.zeros_like(x, dtype=bool)
        region(x, i, j, x[i, j], mask=mask)
        a[mask] = label
        label += 1
    return a


def has_bound_in_direction(
    areas: np.ndarray, pos: tuple[int, int], dir: tuple[int, int]
):
    dirpos = np.asarray(pos) + np.asarray(dir)
    shape = np.asarray(areas.shape)
    if np.any(dirpos < 0) or np.any(dirpos >= shape):
        return True
    result = areas[*pos] != areas[*dirpos]
    return result


def sides(areas: np.ndarray):
    dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
    s = np.zeros_like(areas, dtype=bool)
    s.resize((4,) + areas.shape)
    total = 0
    for area in np.unique(areas):
        for i, j in zip(*np.where(areas == area)):
            for d, dir in enumerate(dirs):
                s[d, i, j] = has_bound_in_direction(areas, (i, j), dir)
        areabounds = s & (areas == area)
        num_sides = 0
        for i, direction in enumerate(areabounds):
            if i & 1:
                direction = direction.transpose()
            for row in direction:
                in_run = False
                for col in row:
                    if col and not in_run:
                        in_run = True
                        num_sides += 1
                    elif not col:
                        in_run = False
        size = np.count_nonzero(areas == area)
        total += size * num_sides
    return total


areas = labels(garden)
fence = perimeter(areas)
price = 0
for area in np.unique(areas):
    price += sum(peri := fence[np.where(areas == area)]) * peri.size
print(price)
bulk_price = sides(areas)

print(bulk_price)
