import itertools
from pathlib import Path

content = Path("example" if __debug__ else "input").read_text()
costA = 3
costB = 1
max_presses = 100
upper_bound = max_presses * costA + max_presses * costB + 1


class Machine:
    def __init__(self, diffax, diffay, diffbx, diffby, px, py):
        self.da = (diffax, diffay)
        self.db = (diffbx, diffby)
        self.p = (px, py)

    @classmethod
    def from_desc(cls, desc):
        a, b, prize = desc.splitlines()
        ax, ay = [int(but.split("+")[1]) for but in a.split(":")[1].split(",")]
        bx, by = [int(but.split("+")[1]) for but in b.split(":")[1].split(",")]
        px, py = [int(p.split("=")[1]) for p in prize.split(":")[1].split(",")]
        return cls(ax, ay, bx, by, px, py)

    def win(self):
        lowest = upper_bound
        for pressa, pressb in itertools.product(
            range(0, max_presses + 1), range(0, max_presses + 1)
        ):
            if (
                pressa * self.da[0] + pressb * self.db[0],
                pressa * self.da[1] + pressb * self.db[1],
            ) == self.p:
                if (cost := pressa * costA + pressb * costB) < lowest:
                    lowest = cost
        if lowest == upper_bound:
            return 0
        return lowest


def bisect(target, low, high, fun):
    mid = (high + low) // 2
    if high >= low:
        return False
    res = fun(mid)
    if res == target:
        return mid
    if res < target:
        return bisect(target, low, mid)
    return bisect(target, mid, high)


class CorrectedMachine(Machine):
    def __init__(self, diffax, diffay, diffbx, diffby, px, py):
        unit_offset = 10000000000000
        super().__init__(
            diffax, diffay, diffbx, diffby, px + unit_offset, py + unit_offset
        )

    def win(self):
        numerator = self.p[1] * self.da[0] - self.p[0] * self.da[1]
        denominator = self.db[1] * self.da[0] - self.db[0] * self.da[1]
        b = numerator / denominator
        a = (self.p[0] - b * self.db[0]) / self.da[0]
        if int(a) == a and int(b) == b:
            return int(costA * a + costB * b)
        return 0


def part1():
    machines = list(map(Machine.from_desc, content.split("\n\n")))
    total = 0
    for machine in machines:
        total += machine.win()
    return total


def part2():
    machines = list(map(CorrectedMachine.from_desc, content.split("\n\n")))
    total = 0
    for machine in machines:
        total += machine.win()
    return total


print(part1())
print(part2())
