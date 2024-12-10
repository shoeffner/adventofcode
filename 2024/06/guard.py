import itertools
from pathlib import Path
import numpy as np

OBSTACLE = "#"
NEW_OBSTACLE = "O"
START = "^"
PATH = "X"


content = Path("input").read_text().splitlines()
grid = np.array(list(map(list, content)))

pos = np.array(np.where(grid == START)).flatten()
directions = itertools.cycle(((-1, 0), (0, 1), (1, 0), (0, -1)))
direction = next(directions)
grid[*pos] = PATH
while (
    0 <= pos[0] + direction[0] < grid.shape[0]
    and 0 <= pos[1] + direction[1] < grid.shape[1]
):
    while grid[*(pos + direction)] == OBSTACLE:
        direction = next(directions)
    pos += direction
    grid[*pos] = PATH
print(np.count_nonzero(grid == PATH))


def print_grid(grid):
    for row in grid:
        print("".join(row))


TURN = "T"
cycles = 0
original_grid = np.array(list(map(list, content)))
total = np.sum(original_grid == ".")
for num, (row, col) in enumerate(zip(*np.where(original_grid == "."))):
    print(f"\r{num:05}/{total}", end="")
    grid = original_grid.copy()
    grid[row, col] = NEW_OBSTACLE
    directions = itertools.cycle(((-1, 0), (0, 1), (1, 0), (0, -1)))
    direction = next(directions)
    pos = np.array(np.where(grid == START)).flatten()
    grid[*pos] = PATH
    has_cycle = False
    while (
        0 <= pos[0] + direction[0] < grid.shape[0]
        and 0 <= pos[1] + direction[1] < grid.shape[1]
    ):
        turned = False
        while grid[*(pos + direction)] in (OBSTACLE, NEW_OBSTACLE):
            if grid[*pos] == TURN:
                has_cycle = True
                break
            direction = next(directions)
            turned = True
        if has_cycle:
            cycles += 1
            break
        grid[*pos] = PATH if not turned else TURN
        pos += direction
    grid[*pos] = PATH if not turned else TURN

print("\n", cycles)
