import math
import itertools
import operator
from multiprocessing import Pool, freeze_support
from pathlib import Path

DO_PART_TWO = True


def make_calibration(line):
    result, values = line.split(":")
    return int(result), list(map(int, values.split()))


def concatenation(a, b):
    return a * 10 ** math.ceil(math.log10(b + 1)) + b


def calibration_result(calibration):
    operators = [operator.add, operator.mul]
    if DO_PART_TWO:
        operators.append(concatenation)
    target, values = calibration
    for ops in itertools.product(operators, repeat=len(values) - 1):
        result = values[0]
        for val, op in zip(values[1:], ops):
            result = op(result, val)
            if result > target:
                break
        if __debug__:
            print(
                target,
                "==" if result == target else "!=",
                result,
                "(",
                values,
                [o.__name__ for o in ops],
                ")",
            )
        if result == target:
            return target
    return 0


def main():
    lines = Path("example" if __debug__ else "input").read_text().splitlines()
    calibrations = map(make_calibration, lines)
    cores = 8
    per_core = len(lines) // cores
    with Pool(cores) as p:
        results = p.map(calibration_result, calibrations, per_core)
        if __debug__:
            print(results)
    print(sum(results))


if __name__ == "__main__":
    freeze_support()
    main()
