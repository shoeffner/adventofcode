from pathlib import Path

elves = []
calories = 0
for line in Path('input').read_text().splitlines():
    if line:
        calories += int(line)
    else:
        elves.append(calories)
        calories = 0

print(max(elves))
total = 0
for i in range(3):
    highest = max(elves)
    elves.remove(highest)
    total += highest
print(total)
