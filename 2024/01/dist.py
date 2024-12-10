from pathlib import Path
la, lb = [], []
for l in Path('input').read_text().splitlines():
    a, b = l.split()
    la.append(int(a))
    lb.append(int(b))
la = sorted(la)
lb = sorted(lb)

print(sum(abs(a-b) for a, b in zip(la, lb)))

counts = {}
for n in lb:
    counts[n] = counts.get(n, 0) + 1

print(sum(a * counts.get(a, 0) for a, b in zip(la, lb)))
