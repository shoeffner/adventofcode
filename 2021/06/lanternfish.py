import simpy


class Lanternfish:
    def __init__(self, env, pond, timer=6):
        self.env = env
        self.pond = pond
        self.timer = timer
        self.action = self.env.process(self.run())

    def run(self):
        while True:
            while self.timer > 0:
                yield self.env.timeout(1)
                self.timer -= 1
            yield self.env.timeout(1)
            self.pond.spawn(8)
            self.timer = 6

    def __str__(self):
        return str(self.timer)


class Pond:
    def __init__(self, env, initial_fish, report=True):
        self.env = env
        self.fish = [Lanternfish(self.env, self, t) for t in initial_fish]
        if report:
            self.action = self.env.process(self.report())

    def report(self):
        while True:
            print(self)
            yield self.env.timeout(1)

    def spawn(self, t):
        self.fish.append(Lanternfish(self.env, self, t))

    def __str__(self):
        if self.env.now == 0:
            s = ': '
        else:
            s = 's:'
        prefix = f'[{len(self.fish):>6d}] After {self.env.now+1:>2d} day{s} '
        if self.env.now == -1:
            prefix = f'[{len(self.fish):>6d}] Initial state: '

        fishlist = ','.join(map(str, self.fish))
        return prefix + fishlist


def main():
    env = simpy.Environment(-1)
    pond = Pond(env, map(int, input().split(',')), report=False)
    env.run(until=80)
    print(len(pond.fish))


if __name__ == '__main__':
    main()
