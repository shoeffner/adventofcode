from multiprocessing import Pool, freeze_support
from functools import lru_cache, partial
from pathlib import Path


def main(steps=25):
    stones = list(
        map(int, Path("example" if __debug__ else "input").read_text().strip().split())
    )
    with Pool(8) as p:
        print(sum(p.imap_unordered(partial(num, steps=steps), stones)))


@lru_cache(maxsize=None)
def next_stones(stone):
    if stone == 0:
        return (1,)
    elif not ((length := len(stst := str(stone))) & 1):
        return int(stst[: length // 2]), int(stst[length // 2 :])
    else:
        return (stone * 2024,)


@lru_cache(maxsize=None)
def num(stone, steps):
    if steps == 0:
        return 1
    new = next_stones(stone)
    return sum(num(st, steps - 1) for st in new)


if __name__ == "__main__":
    freeze_support()
    main(25)
    main(75)
