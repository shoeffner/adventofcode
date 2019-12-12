from itertools import combinations


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

    # def __add__(self, other):
    #     if not isinstance(other, Vec):
    #         raise TypeError(f'Cannot add {type(other)} to Vec.')
    #     return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

    # def __radd__(self, other):
    #     if not isinstance(other, Vec):
    #         raise TypeError(f'Cannot add {type(other)} to Vec.')
    #     return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

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


def simulate(moons, steps=1000, verbose=False):
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

    print(f'After {steps} steps:')
    for moon in moons:
        print(moon)
    print('Energy:', sum(map(lambda m: m.energy, moons)))
    print()


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

    simulate(moons, 10, 1)


def test2():
    io = Moon(Vec(-8, -10, 0))
    europa = Moon(Vec(5, 5, 10))
    ganymede = Moon(Vec(2, -7, 3))
    callisto = Moon(Vec(9, -8, -3))
    moons = [io, europa, ganymede, callisto]

    simulate(moons, 100, 10)


if __name__ == '__main__':
    test1()
    test2()
    main()
