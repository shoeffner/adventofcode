import sys

depths = list(map(int, sys.stdin.read().splitlines()))
depths = list(map(sum, zip(depths, depths[1:], depths[2:])))
print(sum(x < y for x, y in zip(depths[:-1], depths[1:])))
