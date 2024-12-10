import itertools
from pathlib import Path

import numpy as np


def print_map(antennas, antinodes):
    a = antennas.copy()
    a[antinodes] = "#"
    for row in a:
        print("".join(row))


lines = Path("example" if __debug__ else "input").read_text().splitlines()
antennas = np.array([list(line) for line in lines])
antinodes = np.zeros_like(antennas, dtype=bool)
if __debug__:
    print(antennas)
    print(antinodes)
frequencies = set(np.unique(antennas)) - set(".")
if __debug__:
    print(frequencies)

for frequency in frequencies:
    if __debug__:
        print(frequency, np.where(antennas == frequency))
    for a, b in itertools.permutations(
        map(np.array, zip(*np.where(antennas == frequency))), r=2
    ):
        if __debug__:
            print(frequency, a, b, a + (a - b))
        for multiplier in range(-100, 101):
            antinode = a + multiplier * (a - b)
            if np.any(antinode < 0) or np.any(antinode >= antennas.shape):
                continue
            antinodes[*antinode] = True
if __debug__:
    print_map(antennas, antinodes)
print(np.sum(antinodes))
