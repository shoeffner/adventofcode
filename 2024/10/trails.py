from functools import partial
import numpy as np
from multiprocessing import Pool, freeze_support
from pathlib import Path

directions = list(map(np.array, ((-1, 0), (1, 0), (0, -1), (0, 1))))


def trail_score(
    topo, coord, expected_height=0, current_score=0, visited=None, variant="score"
):
    if __debug__:
        print("c", coord, "s", current_score, "v", variant)
    if visited is None:
        visited = np.zeros_like(topo)
    if np.any(coord < (0, 0)):
        return 0
    if np.any(coord >= topo.shape):
        return 0

    if __debug__:
        print("v", visited[*coord], "t", topo[*coord], "h", expected_height)

    if visited[*coord] == 1:
        return 0
    if topo[*coord] != expected_height:
        return 0
    if variant == "score":
        visited[*coord] = 1
    if topo[*coord] == 9:
        if __debug__:
            print("path")
            print(visited)
        return 1

    if __debug__:
        print("try dirs")
    reached_any_top = 0
    for direction in directions:
        if variant == "rating":
            visited[*coord] = 1
        reached_any_top += trail_score(
            topo,
            coord + direction,
            expected_height + 1,
            current_score,
            visited,
            variant,
        )
        if variant == "rating":
            visited[*coord] = 0
    if variant == "score" and not reached_any_top:
        visited[*coord] = 0
    return current_score + reached_any_top


def trail_rating(*args, **kwargs):
    return trail_score(*args, **kwargs, variant="rating")


def main():
    lines = Path("example" if __debug__ else "input").read_text().splitlines()
    topo = np.array(list(list(map(int, line)) for line in lines))
    cases = list(zip(*np.where(topo == 0)))
    with Pool(8) as p:
        scores = list(p.imap(partial(trail_score, topo), cases))
        ratings = list(p.imap(partial(trail_rating, topo), cases))
    if __debug__:
        print(scores)
    print(sum(scores))
    if __debug__:
        print(ratings)
    print(sum(ratings))


if __name__ == "__main__":
    freeze_support()
    main()
