import sys

depths = list(map(int, sys.stdin.read().splitlines()))
print(sum(x < y for x, y in zip(depths[0:-1], depths[1:])))
