from matplotlib.animation import FuncAnimation
import numpy as np
from collections import Counter
from functools import reduce
import operator
from pathlib import Path
from matplotlib.widgets import Slider
from matplotlib import pyplot as plt

content = Path("example" if __debug__ else "input").read_text()

height = 7 if __debug__ else 103
width = 11 if __debug__ else 101

time = 100


def parse(content):
    strs = [line.split() for line in content.splitlines()]
    pvs = [
        (
            tuple(map(int, s[0].split("=")[1].split(","))),
            tuple(map(int, s[1].split("=")[1].split(","))),
        )
        for s in strs
    ]
    return pvs


robots = parse(content)


def sim(p: tuple, v: tuple, time=1):
    return ((p[0] + v[0] * time) % width, (p[1] + v[1] * time) % height)


def quadrant(robot: tuple):
    mid_w = width // 2
    mid_h = height // 2
    if robot[0] < mid_w and robot[1] < mid_h:
        return 0
    if robot[0] > mid_w and robot[1] < mid_h:
        return 1
    if robot[0] > mid_w and robot[1] > mid_h:
        return 2
    if robot[0] < mid_w and robot[1] > mid_h:
        return 3
    return -1


def sim_many(robots, step):
    return list(sim(*r, step) for r in robots)


c = Counter(map(quadrant, sim_many(robots, time)))
print(reduce(operator.mul, (c[i] for i in range(4))))


def as_ndarray(robots: list[tuple]):
    arr = np.zeros((width, height))
    for robot in robots:
        arr[*robot] += 1
    return arr.transpose()

    # def update(time):
    # trial and error shows 7858
    time = 81 + time * 101
    arr = as_ndarray(sim_many(robots, time))
    plt_ax.matshow(arr)
    plt_ax.set_title(f"Step {time}")


# slider
# fig, axes = plt.subplots(2, 1)
# plt_ax, slider_ax = axes
# plt_ax.matshow(arr)
# slider = Slider(slider_ax, label="Time [s]", valmin=0, valmax=1000, valstep=1)
# slider.on_changed(update)

# anim
# fig, plt_ax = plt.subplots(1, 1)
# ani = FuncAnimation(fig, func=update, cache_frame_data=False)

# comp
# fig, ax = plt.subplots(2, 2)
# ax[0][0].matshow(as_ndarray(sim_many(robots, 81)))
# ax[0][1].matshow(as_ndarray(sim_many(robots, 182)))
# ax[1][0].matshow(as_ndarray(sim_many(robots, 283)))
# ax[1][1].matshow(as_ndarray(sim_many(robots, 384)))

print(7858)
arr = as_ndarray(sim_many(robots, 7858))
plt.matshow(arr)
plt.show()
