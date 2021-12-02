import time
from queue import Empty, Full
import numpy as np

from intcomputer import IntComputer, load_program


def countblocks():
    ic = IntComputer(load_program('13/input'))
    blocks = set()
    with ic as proc:
        while not proc.terminated:
            x = proc.stdout.get()
            y = proc.stdout.get()
            t = proc.stdout.get()
            if t == 2:
                blocks.add((x, y))
            else:
                blocks.discard((x, y))
    return len(blocks)


def print_game(game):
    print('\n'.join(''.join(map(str, row)) for row in game))


def play(blocks, manual=False, verbose=True):  # noqa
    score = 0
    blocks += 1  # 1 for initial score
    ic = IntComputer(load_program('13/input'))
    ic.memory[0] = 2
    game = np.zeros((20, 44), dtype=np.uint8)
    paddle = (0, 0)
    ball = (0, 0)
    with ic as proc:
        ctrl = None
        while not proc.terminated:
            for px in range(game.shape[0] * game.shape[1] + 1):
                try:
                    x = proc.stdout.get(block=True, timeout=.2)
                    y = proc.stdout.get(block=True, timeout=.2)
                    t = proc.stdout.get(block=True, timeout=.2)
                except Empty:
                    break
                if x == -1:
                    blocks -= 1
                    score = t
                else:
                    if t == 3:
                        paddle = (x, y)
                    elif t == 4:
                        ball = (x, y)
                    game[y, x] = t
            if verbose:
                print_game(game)
                print('\n--------\n', score)
            else:
                print('\r', ' ' * 20, '\r', f'{score:6d} {blocks:3d}', end='')

            if not manual:
                offset = ball[0] - paddle[0]
                if offset < 0:
                    ctrl = -1
                elif offset > 0:
                    ctrl = 1
                else:
                    ctrl = 0
                try:
                    proc.stdin.put(ctrl, block=True, timeout=.2)
                    ctrl = None
                except Full:
                    pass
            else:
                try:
                    while ctrl is None:
                        try:
                            ctrl = int(input('JOY: '))
                        except ValueError:
                            ctrl = None
                    proc.stdin.put(ctrl, block=True, timeout=1)
                    ctrl = None
                except Full:
                    pass
    print()
    return score


if __name__ == '__main__':
    blocks = countblocks()
    print('blocks', blocks)
    print('Score', play(blocks, verbose=False, manual=False))
