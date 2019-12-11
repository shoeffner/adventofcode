import sys
from pathlib import Path
from collections import defaultdict
import functools

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np


def part1(asteroids):
    best_count = 0
    for oy in range(asteroids.shape[0]):
        for ox in range(asteroids.shape[1]):
            if asteroids[oy, ox] != '#':
                continue
            angles = []
            count = 0
            for y, row in enumerate(asteroids):
                for x, col in enumerate(row):
                    if x == ox and y == oy:
                        continue
                    if col == '#':
                        angle = np.angle(complex(oy - y, ox - x))
                        if angle in angles:
                            continue
                        count += 1
                        angles.append(angle)

            if count > best_count:
                best_count = count
                best = (ox, oy)
    print(best, best_count)
    return best


def main():
    asteroids = [[f for f in l] for l in Path(sys.argv[1]).read_text().splitlines()]
    asteroids = np.array(asteroids)
    best = part1(asteroids)

    # method_1(best, asteroids.copy())
    # method_2(best, asteroids.copy())
    method_3(best, asteroids.copy())


def pprint(a):
    print('\n'.join(''.join(c) for c in a))
    print()


def check_solution(s):
    return 1011 < s < 1815 and s not in [1011, 1016, 1031, 1815, 2008]


def method_1(station, asteroids):  # noqa
    sx, sy = station
    asteroids[sy, sx] = 'X'
    prec = 10  # 2 too high (2008), 3 too low (1011), 4+ too high (1815)
    bet_on = 200

    angles = []
    for y, r in enumerate(asteroids):
        for x, c in enumerate(r):
            angles.append(round(np.angle(complex(sx - x, sy - y)), prec))
    angles = list(sorted(set(angles)))

    while abs(angles[0] - round(np.angle(complex(0, 1)), prec)) >= 1e-10:
        angles.append(angles.pop(0))
    # we only care for the first "bet on" hits
    destroyed = 0
    last = sx, sy

    while destroyed < bet_on and np.any(asteroids == '#'):
        for angle in angles:
            candidates = []
            for y, row in enumerate(asteroids):
                for x, col in enumerate(row):
                    if col in 'X.':
                        continue
                    if abs(np.round(np.angle(complex(sx - x, sy - y)), prec) - angle) <= .5e-2:
                        candidates.append((x, y))
            if candidates:
                closest = (sx, sy)
                closest_distance = 1e8
                for cx, cy in candidates:
                    sq_dist = (sx - cx) ** 2 + (sy - cy) ** 2
                    if sq_dist < closest_distance:
                        closest = (cx, cy)
                        closest_distance = sq_dist
                destroyed += 1
                last = closest
                asteroids[last[1], last[0]] = 'O'
                asteroids[last[1], last[0]] = '.'
                if destroyed == bet_on:
                    break
            if destroyed == bet_on:
                break
    solution = last[0] * 100 + last[1]
    print('Method 1:', f'({prec})', solution, check_solution(solution))


def method_2(station, asteroids):
    sx, sy = station
    asteroids[sy, sx] = 'X'

    bet_on = 200

    angles = []
    hashed = defaultdict(list)
    for y, r in enumerate(asteroids):
        for x, c in enumerate(r):
            angle = np.angle(complex(sx - x, sy - y))
            angles.append(angle)
            hashed[angle].append((x, y))
    angles = list(sorted(set(angles)))
    while abs(angles[0] - np.pi / 2) >= 1e-8:
        angles.append(angles.pop(0))

    sort_hashed = {}
    for k, v in hashed.items():
        sort_hashed[k] = sorted(v, key=lambda v: np.sqrt((sx - v[0]) ** 2 + (sy - v[1]) ** 2))

    destroyed = 0
    last = sx, sy
    while destroyed < bet_on:
        for angle in angles:
            if sort_hashed[angle]:
                destroyed += 1
                last = sort_hashed[angle].pop(0)
                if destroyed in [1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299]:
                    print(destroyed, last)
                if destroyed == bet_on:
                    break
    solution = last[0] * 100 + last[1]
    print('Method 2:', solution, check_solution(solution))


def method_3(station, asteroids):  # noqa
    asteroids[station[1], station[0]] = 'X'
    station = np.array(station)
    pprint(asteroids)
    ys, xs = np.where(asteroids == '#')

    class LaserBeam:
        def __init__(self, station, asteroid):
            self.s = station
            self.a = asteroid

        def plot(self, ax):
            line = mlines.Line2D(*zip(self.s, self.a), c='red', lw=0.3)
            ax.add_line(line)
            return line

        @property
        @functools.lru_cache()
        def angle(self):
            return np.angle(complex(self.a[0] - self.s[0], self.a[1] - self.s[1]))

        @property
        @functools.lru_cache()
        def dist(self):
            return np.linalg.norm(self.a - self.s)

        def __repr__(self):
            return f'{self.a} (a = {self.angle}, d = {self.dist})'

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_facecolor('black')
    ax.set_xlim([-0.5, asteroids.shape[1] - 0.5])
    ax.set_ylim([asteroids.shape[0] - 0.5, -0.5])
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    ax.scatter(xs, ys, marker='.', c='gray')
    ax.scatter(*station, marker='x', c='darkgreen')

    beams = [LaserBeam(station, (x, y)) for x, y in zip(xs, ys)]
    beams = sorted(beams, key=lambda b: b.angle)
    while abs(beams[0].angle + np.pi / 2) > 1e-9:
        beams.append(beams.pop(0))
    angles = sorted(set([b.angle for b in beams]))
    while abs(angles[0] + np.pi / 2) > 1e-9:
        angles.append(angles.pop(0))

    lookup = defaultdict(list)
    for beam in beams:
        lookup[beam.angle].append(beam)
        lookup[beam.angle] = sorted(lookup[beam.angle], key=lambda b: b.dist)

    shot = []
    while np.any(asteroids == '#'):
        for angle in angles:
            if lookup[angle]:
                beam = lookup[angle].pop(0)
                shot.append(beam)
                asteroids[beam.a[1], beam.a[0]] = '.'
    for beam in shot:
        beam.plot(ax)

    for i in [1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299]:
        print(i, shot[i - 1])
    solution = shot[199].a[0] * 100 + shot[199].a[1]
    print('Method 3:', solution, check_solution(solution))

    fig.waitforbuttonpress()


if __name__ == '__main__':
    main()
