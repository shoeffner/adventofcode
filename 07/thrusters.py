import itertools
from pathlib import Path
import sys
import subprocess
from multiprocessing import Pool
from functools import partial


def thrust_signal(phase_setting, program_path, cwd=str(Path.cwd() / '..')):
    signal = 0
    for phase in phase_setting:
        input = f'{phase}\n{signal}\n'
        signal = int(subprocess.run(f'python3 intcomputer.py {program_path}'.split(),
                                    input=input.encode('utf-8'),
                                    cwd=cwd, capture_output=True).stdout)
    return int(signal)


def main():
    program = Path(sys.argv[1]).resolve()

    phase_settings = itertools.permutations(range(5), 5)
    ts = partial(thrust_signal, program_path=program)
    with Pool(16) as p:
        signals = p.map(ts, phase_settings)

    print(max(signals))


if __name__ == '__main__':
    main()
