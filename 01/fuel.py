import sys

print(sum(int(line) // 3 - 2 for line in sys.stdin))
