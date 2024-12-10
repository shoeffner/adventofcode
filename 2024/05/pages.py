from collections import defaultdict
from pathlib import Path


content = Path("input").read_text()
rules, printings = content.split("\n\n")

graph = defaultdict(set)
inv_graph = defaultdict(set)
for rule in rules.splitlines():
    before, after = map(int, rule.split("|"))
    graph[after].add(before)


def is_ordered(pages):
    for page, next_page in zip(pages[:-1], pages[1:]):
        if next_page in graph[page]:
            return False
    return True


def order(pages):
    while not is_ordered(pages):
        for i, (p, np) in enumerate(zip(pages[:-1], pages[1:])):
            if np in graph[p]:
                pages[i], pages[i + 1] = pages[i + 1], pages[i]
                break
    return pages


middle_pages = 0
middle_pages_corrected = 0
for printing in printings.splitlines():
    current_order_idx = 0
    pages = list(map(int, printing.split(",")))
    if is_ordered(pages):
        middle_pages += pages[len(pages) // 2]
    else:
        middle_pages_corrected += order(pages)[len(pages) // 2]
print(middle_pages)
print(middle_pages_corrected)
