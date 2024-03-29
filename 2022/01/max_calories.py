from pathlib import Path

elves = [sum(map(int, elf.splitlines())) for elf in Path('input').read_text().split('\n\n')]

print(max(elves))

print(sum(sorted(elves)[-3:]))
