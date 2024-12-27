from functools import lru_cache
import numpy as np
from pathlib import Path

content = Path("example" if __debug__ else "input").read_text()
# content = """\
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# <^^>>>vv<v>>v<<
# """

warehouse, moves = content.split("\n\n")
moves = moves.replace("\n", "")


@lru_cache
def offset(direction):
    match direction:
        case "<":
            return np.array((0, -1))
        case ">":
            return np.array((0, 1))
        case "^":
            return np.array((-1, 0))
        case "v":
            return np.array((1, 0))


class Entity:
    def __init__(self, grid, xy):
        self.grid = grid
        self.pos = np.array(xy)
        self.grid[self.pos] = self

    def can_move(self, direction):
        off = offset(direction)
        if (entity := self.grid[self.pos + off]) is Free:
            return True
        return entity.can_move(direction)

    def move(self, direction):
        if not self.can_move(direction):
            return
        off = offset(direction)
        self.grid[self.pos + off].move(direction)
        self.grid[self.pos] = Free
        self.pos += off
        self.grid[self.pos] = self

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pos})"

    def __str__(self):
        return "?"


class FreeEntity(Entity):
    def __init__(self):
        self.pos = ""

    def can_move(self, direction):
        return False

    def __str__(self):
        return "."


class Wall(Entity):
    def can_move(self, direction):
        return False

    def __str__(self):
        return "#"


class Robot(Entity):
    def __str__(self):
        return "@"


class Box(Entity):
    def __str__(self):
        return "O"


class BigBox(Entity):
    right_offset = offset(">")

    def __init__(self, grid, xy):
        super().__init__(grid, xy)
        self.grid[self.pos + BigBox.right_offset] = self

    def can_move(self, direction):
        if direction in "^v":
            left_part = super().can_move(direction)
            self.pos += BigBox.right_offset
            right_part = super().can_move(direction)
            self.pos -= BigBox.right_offset
            return left_part and right_part
        if direction == ">":
            self.pos += BigBox.right_offset
            right_part = super().can_move(direction)
            self.pos -= BigBox.right_offset
            return right_part
        if direction == "<":
            return super().can_move(direction)
        raise ValueError("Unknown direction")

    def move(self, direction):
        if not self.can_move(direction):
            return
        off = offset(direction)
        if direction == ">":
            self.grid[self.pos + off + BigBox.right_offset].move(direction)
            self.grid[self.pos] = Free
            self.pos += off
            self.grid[self.pos + BigBox.right_offset] = self
        if direction == "<":
            self.grid[self.pos + off].move(direction)
            self.grid[self.pos + BigBox.right_offset] = Free
            self.pos += off
            self.grid[self.pos] = self
        if direction in "^v":
            self.grid[self.pos + off].move(direction)
            self.grid[self.pos + off + BigBox.right_offset].move(direction)
            self.grid[self.pos] = Free
            self.grid[self.pos + BigBox.right_offset] = Free
            self.pos += off
            self.grid[self.pos] = self
            self.grid[self.pos + BigBox.right_offset] = self

    def __str__(self):
        return "[]"


Free = FreeEntity()
Invalid = FreeEntity()


class Grid:
    def __init__(self, height, width):
        self.data = [[Free for w in range(width)] for h in range(height)]

    def __getitem__(self, xy: tuple | np.ndarray):
        x, y = xy
        try:
            return self.data[x][y]
        except IndexError:
            return Invalid

    def __setitem__(self, xy: tuple, entity: Entity):
        x, y = xy
        self.data[x][y] = entity

    def __str__(self):
        s = ""
        bbleft = True
        for row in self.data:
            for col in row:
                if isinstance(col, BigBox):
                    if bbleft:
                        bbleft = False
                    else:
                        bbleft = True
                        continue
                s += str(col)
            s += "\n"
        return s[:-1]

    def evaluate(self):
        gps = 0
        counted = False
        for x, row in enumerate(self.data):
            for y, col in enumerate(row):
                if isinstance(col, Box):
                    gps += 100 * x + y
                if isinstance(col, BigBox):
                    if not counted:
                        counted = True
                        gps += 100 * x + y
                    else:
                        counted = False
        return gps


def generate(warehouse):
    lines = warehouse.splitlines()
    grid = Grid(len(lines), len(lines[0]))
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            match c:
                case "O":
                    EntityClass = Box
                case "#":
                    EntityClass = Wall
                case "@":
                    EntityClass = Robot
                case _:
                    continue
            entity = EntityClass(grid, (x, y))
            if c == "@":
                robot = entity
    return grid, robot


def generate_2(warehouse):
    lines = warehouse.splitlines()
    grid = Grid(len(lines), len(lines[0]) * 2)
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            y = y * 2
            match c:
                case "O":
                    BigBox(grid, (x, y))
                case "#":
                    Wall(grid, (x, y))
                    Wall(grid, (x, y + 1))
                case "@":
                    robot = Robot(grid, (x, y))
                case _:
                    continue
    return grid, robot


grid, robot = generate(warehouse)
if __debug__:
    print("Initial state:", grid, sep="\n")
for move in moves:
    robot.move(move)
    if __debug__:
        print("\nMove:", move)
        print(grid)
print(grid.evaluate())


grid, robot = generate_2(warehouse)
if __debug__:
    print("Initial state:", grid, sep="\n")
for move in moves:
    robot.move(move)
    if __debug__:
        print("\nMove:", move)
        print(grid)
print(grid.evaluate())
