from pathlib import Path

pairs = Path('input').read_text().splitlines()

fully_contained = 0
overlap = 0
for pair in pairs:
    (lb_a, ub_a), (lb_b, ub_b) = [tuple(map(int, x.split('-'))) for x in  pair.split(',')]
    if (lb_a >= lb_b and ub_a <= ub_b) or (lb_b >= lb_a and ub_b <= ub_a):
        fully_contained += 1
    if not (ub_a < lb_b or ub_b < lb_a):
        overlap += 1
print(fully_contained)
print(overlap)