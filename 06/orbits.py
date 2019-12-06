from collections import defaultdict
import itertools
import sys

orbits = [l.strip() for l in sys.stdin.readlines()]

vertices = set(itertools.chain.from_iterable(o.split(')') for o in orbits))
edges = list(o.split(')') for o in orbits)

# print(vertices)
# print(edges)

g = defaultdict(list)

for l, r in edges:
    g[l].append(r)


def count_steps(g, root, node, depth):
    if node not in g:
        # leaf found
        return depth
    c = 0
    for n in g[node]:
        c += count_steps(g, node, n, depth + 1)
    return depth + c

c = 0
for n in g['COM']:
    c += count_steps(g, 'COM', n, 1)
print(c)
