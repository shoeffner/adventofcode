from pathlib import Path

unsafe, safe = 0, 0
for line in Path("input").read_text().splitlines():
    maybe_count = False
    first, second, *others = map(int, line.split())
    if first < second:  # inc
        for n in [second] + others:
            if n <= first or n - first > 3:
                if maybe_count:
                    unsafe += 1
                    break
                else:
                    maybe_count = True
            first = n
        else:
            safe += 1
    else:  # dec
        for n in [second] + others:
            if n >= first or first - n > 3:
                if maybe_count:
                    unsafe += 1
                    break
                else:
                    maybe_count = True
            first = n
        else:
            safe += 1

print(safe)
