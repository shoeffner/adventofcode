from itertools import combinations
import numpy as np


class Vec:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'<x={self.x:3d}, y={self.y:3d}, z={self.z:3d}>'

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f'Key {key} does not exist.')

    def __setitem__(self, key, val):
        if hasattr(self, key):
            return setattr(self, key, val)
        raise KeyError(f'Key {key} does not exist.')

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self


class Moon:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vec(0, 0, 0)

    def __str__(self):
        return f'pos={self.pos}, vel={self.vel}'

    @property
    def potential_energy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    @property
    def kinetic_energy(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)

    @property
    def energy(self):
        return self.potential_energy * self.kinetic_energy


def simulate(moons, steps=1000, verbose=False, early_stopping=False):
    history_x = set()
    history_y = set()
    history_z = set()
    for timestep in range(steps):
        if verbose and timestep % verbose == 0:
            print(f'After {timestep} steps:')
            for moon in moons:
                print(moon)
            print('Energy:', sum(map(lambda m: m.energy, moons)))
            print()

        # apply gravity
        new_moons = moons.copy()
        for (i0, m0), (i1, m1) in combinations(enumerate(moons), 2):
            # gan 3 < cal 5
            for c in 'xyz':
                if m0.pos[c] < m1.pos[c]:
                    new_moons[i0].vel[c] += 1
                    new_moons[i1].vel[c] -= 1
                elif m0.pos[c] > m1.pos[c]:
                    new_moons[i0].vel[c] -= 1
                    new_moons[i1].vel[c] += 1

        moons = new_moons
        # apply velocity
        for moon in moons:
            moon.pos += moon.vel

        # part 2: find cycles
        if early_stopping:
            x = tuple((moon.pos.x, moon.vel.x) for moon in moons)
            y = tuple((moon.pos.y, moon.vel.y) for moon in moons)
            z = tuple((moon.pos.z, moon.vel.z) for moon in moons)
            if x in history_x and y in history_y and z in history_z:
                break
            if x not in history_x:
                history_x.add(x)
            if y not in history_y:
                history_y.add(y)
            if z not in history_z:
                history_z.add(z)

    print(f'After {timestep + 1} steps:')
    for moon in moons:
        print(moon)
    print('Energy:', sum(map(lambda m: m.energy, moons)))
    print()
    if early_stopping:
        return len(history_x), len(history_y), len(history_z)


def main():
    io = Moon(Vec(-8, -18, 6))
    europa = Moon(Vec(-11, -14, 4))
    ganymede = Moon(Vec(8, -3, -10))
    callisto = Moon(Vec(-2, -16, 1))
    moons = [io, europa, ganymede, callisto]

    simulate(moons, 1000, False)


def test1():
    io = Moon(Vec(-1, 0, 2))
    europa = Moon(Vec(2, -10, -7))
    ganymede = Moon(Vec(4, -8, 8))
    callisto = Moon(Vec(3, 5, -1))
    moons = [io, europa, ganymede, callisto]

    simulate(moons, 2772, 1)


def test2():
    io = Moon(Vec(-8, -10, 0))
    europa = Moon(Vec(5, 5, 10))
    ganymede = Moon(Vec(2, -7, 3))
    callisto = Moon(Vec(9, -8, -3))
    moons = [io, europa, ganymede, callisto]

    simulate(moons, 100, 10)


def test3():
    io = Moon(Vec(-8, -10, 0))
    europa = Moon(Vec(5, 5, 10))
    ganymede = Moon(Vec(2, -7, 3))
    callisto = Moon(Vec(9, -8, -3))
    moons = [io, europa, ganymede, callisto]

    x, y, z = simulate(moons, 20000, False, True)
    print('Orbit of length:', np.lcm.reduce([x, y, z]))


def test4():
    io = Moon(Vec(-1, 0, 2))
    europa = Moon(Vec(2, -10, -7))
    ganymede = Moon(Vec(4, -8, 8))
    callisto = Moon(Vec(3, 5, -1))
    moons = [io, europa, ganymede, callisto]

    x, y, z = simulate(moons, 20000, False, True)
    print('Orbit of length:', np.lcm.reduce([x, y, z]))


def main2():
    io = Moon(Vec(-8, -18, 6))
    europa = Moon(Vec(-11, -14, 4))
    ganymede = Moon(Vec(8, -3, -10))
    callisto = Moon(Vec(-2, -16, 1))
    moons = [io, europa, ganymede, callisto]

    x, y, z = simulate(moons, 1000000, False, True)
    print('Orbit of length:', np.lcm.reduce([x, y, z]))


if __name__ == '__main__':
    test1()
    test2()
    main()
    test3()
    test4()
    main2()
