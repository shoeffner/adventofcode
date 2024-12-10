from pathlib import Path
import re


mem = Path("input").read_text()
mul_regex = r"mul\((\d{1,3}),(\d{1,3})\)"
do_regex = r"do\(\)"
dont_regex = r"don't\(\)"
acc = 0
do = True
for m in re.finditer(rf"({mul_regex}|{do_regex}|{dont_regex})", mem):
    if m.group(0) == "do()":
        do = True
    elif m.group(0) == "don't()":
        do = False
    else:
        if do:
            acc += int(m.group(2)) * int(m.group(3))

print(acc)
