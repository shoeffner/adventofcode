from queue import Empty, Full
import numpy as np

from intcomputer import IntComputer, load_program


FREE = 0
UNEXPLORED = 255
WALL = 127
OXYGEN = 200

NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4

FAILURE, SUCCESS, FOUND = 0, 1, 2


def print_flood(map_):
    pmap = np.asarray(map_.copy(), dtype=str)
    pmap[map_ == -1] = ' '
    pmap[map_ == -2] = '░'
    pmap[map_ > -1] = '◌'
    print('\n'.join(''.join(map(str, row)) for row in pmap))


def print_map(map_, position=None):
    pmap = np.zeros_like(map_, dtype=str)
    pmap[map_ == FREE] = ' '
    pmap[map_ == UNEXPLORED] = '.'
    pmap[map_ == WALL] = '░'
    pmap[map_ == OXYGEN] = 'X'
    if position is not None:
        pmap[position] = 'D'
    print('\n'.join(''.join(map(str, row)) for row in pmap))


def position_from(position, command):
    if command == NORTH:
        new_position = (position[0] - 1, position[1])
    elif command == SOUTH:
        new_position = (position[0] + 1, position[1])
    elif command == WEST:
        new_position = (position[0], position[1] - 1)
    elif command == EAST:
        new_position = (position[0], position[1] + 1)
    return new_position


def solve_maze(maze, position, act, steps=1, verbose=False):
    if UNEXPLORED in maze:
        for move, counter_move in [(NORTH, SOUTH), (EAST, WEST), (SOUTH, NORTH), (WEST, EAST)]:
            new_pos = position_from(position, move)
            if maze[new_pos] == UNEXPLORED:
                # move there, or stay?
                if verbose:
                    print_map(maze, new_pos)
                response = act(move)
                if response in [FOUND, SUCCESS]:
                    maze[new_pos] = OXYGEN if response == FOUND else FREE
                    if response == FOUND:
                        print(steps)

                    success = solve_maze(maze, new_pos, act, steps + 1, verbose)
                    if success:
                        return True
                    else:
                        # move back
                        response = act(counter_move)
                        if response == FAILURE:
                            print('FAIL when moving back!')
                            return False
                # stay on failure, try next move
                elif response == FAILURE:
                    maze[new_pos] = WALL
            elif maze[new_pos] == OXYGEN:
                return True
            # else if wall: next direction
    return False


def flood_map(maze, position, flood=None, steps=0, verbose=False):
    if flood is None:
        flood = np.zeros_like(maze, dtype=np.int) - 1

    if steps <= 1000:
        flood[position] = steps
        for move in [NORTH, EAST, SOUTH, WEST]:
            new_pos = position_from(position, move)
            if flood[new_pos] == -1:
                if maze[new_pos] == WALL:
                    flood[new_pos] = -2
                else:
                    success = flood_map(maze, new_pos, flood, steps + 1, verbose)
                    if success:
                        return True
            else:
                if flood[new_pos] > steps + 1:
                    success = flood_map(maze, new_pos, flood, steps + 1, verbose)
                    if success:
                        return True
        return False
    return False


def robot():  # noqa
    map_ = np.ones((41, 41), dtype=np.uint8) * UNEXPLORED
    map_[0, :] = WALL
    map_[-1, :] = WALL
    map_[:, 0] = WALL
    map_[:, -1] = WALL
    start_position = map_.shape[0] // 2 + 1, map_.shape[1] // 2 + 1
    ic = IntComputer(load_program('15/input'))
    with ic as proc:
        def act(command):
            try:
                proc.stdin.put(command, block=True, timeout=.2)
            except Full:
                pass
            try:
                response = proc.stdout.get(block=True, timeout=.2)
            except Empty:
                pass
            return response

        solve_maze(map_, start_position, act)
        map_[map_ == UNEXPLORED] = WALL
        print_map(map_, start_position)

        oxygen_position = np.where(map_ == OXYGEN)
        oxygen_position = oxygen_position[0][0], oxygen_position[1][0]
        flood = np.zeros_like(map_, dtype=np.int) - 1
        flood_map(map_, oxygen_position, flood)
        print(np.max(flood))
        print_flood(flood)


if __name__ == '__main__':
    robot()
