import string
from pathlib import Path
from itertools import zip_longest
from functools import reduce

total_priorities = 0
for rucksack in Path('input').read_text().splitlines():
    items_per_comp = len(rucksack) // 2
    comp1, comp2 = rucksack[:items_per_comp], rucksack[items_per_comp:]
    duplicate = (set(comp1) & set(comp2)).pop()
    priority = string.ascii_letters.index(duplicate) + 1
    total_priorities += priority
print(total_priorities)

total_priorities = 0
for group in zip(*[iter(Path('input').read_text().splitlines())] * 3):
    badge = reduce(set.intersection, map(set, group)).pop()
    priority = string.ascii_letters.index(badge) + 1
    total_priorities += priority
print(total_priorities)