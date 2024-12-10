import re
from itertools import chain
from pathlib import Path

hor_lr = Path("input").read_text().splitlines()
width = len(hor_lr[0])
height = len(hor_lr)
ver_down = [[] for _ in range(width)]
for row in hor_lr:
    for i, c in enumerate(row):
        ver_down[i].append(c)
ver_down = ["".join(r) for r in ver_down]

dia_tlbr = [[] for _ in range(width + height - 1)]
for row_idx in range(height - 1, 0, -1):
    col_idx = 0
    dia_idx = height - 1 - row_idx
    while row_idx < height and col_idx < width:
        dia_tlbr[dia_idx].append(hor_lr[row_idx][col_idx])
        row_idx += 1
        col_idx += 1

for col_idx in range(width):
    row_idx = 0
    dia_idx = height - 1 + col_idx
    while row_idx < height and col_idx < width:
        dia_tlbr[dia_idx].append(hor_lr[row_idx][col_idx])
        row_idx += 1
        col_idx += 1

dia_tlbr = ["".join(r) for r in dia_tlbr]

dia_bltr = [[] for _ in range(width + height - 1)]
for row_idx in range(height):
    col_idx = 0
    dia_idx = row_idx
    while row_idx >= 0 and col_idx < width:
        dia_bltr[dia_idx].append(hor_lr[row_idx][col_idx])
        row_idx -= 1
        col_idx += 1
for col_idx in range(1, width):
    row_idx = height - 1
    dia_idx = height + col_idx - 1
    while row_idx >= 0 and col_idx < width:
        dia_bltr[dia_idx].append(hor_lr[row_idx][col_idx])
        row_idx -= 1
        col_idx += 1
dia_bltr = ["".join(r) for r in dia_bltr]


def r(x):
    return [y[::-1] for y in x]


xmas = re.compile("XMAS")
count = 0
for i, row in enumerate(
    chain(
        hor_lr,
        r(hor_lr),
        ver_down,
        r(ver_down),
        dia_tlbr,
        r(dia_tlbr),
        dia_bltr,
        r(dia_bltr),
    )
):
    num = sum(1 for _ in xmas.finditer(row))
    count += num
print(count)
