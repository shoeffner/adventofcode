import sys


def trajectory(wire):
    t = [(0, 0)]
    for command in wire:
        current = t[-1]
        direction, step = command[0], int(command[1:])
        for i in range(1, step + 1):
            if direction == 'R':
                new = current[0] + i, current[1]
            elif direction == 'L':
                new = current[0] - i, current[1]
            elif direction == 'U':
                new = current[0], current[1] + i
            elif direction == 'D':
                new = current[0], current[1] - i
            else:
                raise ValueError(f'Can not process {command}')
            t.append(new)
    return t


wires = [l.split(',') for l in sys.stdin.readlines()]
trajectories = [trajectory(wire) for wire in wires]


def find_intersections(trajectories):
    shortest = 1e10
    intersections = []
    for i, t1 in enumerate(trajectories[1]):
        if t1 == (0, 0):
            continue
        for j, t0 in enumerate(trajectories[0]):
            if t0 < t1:
                del trajectories[0][j]
            elif t0 == t1:
                dist = sum(map(abs, t1))
                if dist < shortest:
                    shortest = dist
                intersections.append(t1)
            elif t0 > t1:
                break
    print(f'Closest intersection is {shortest} away.')
    return intersections


def walk_to(intersection, trajectory):
    return trajectory.index(intersection)


intersections = find_intersections(list(sorted(set(t)) for t in trajectories))

closest = (0, 0)
steps = 1e10
for intersection in intersections:
    nsteps = sum(map(lambda t: t.index(intersection), trajectories))
    if nsteps < steps:
        steps = nsteps
        closest = intersection

print(closest, steps)
