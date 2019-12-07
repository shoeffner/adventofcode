import itertools
from pathlib import Path
import sys
from subprocess import run
from multiprocessing import Pool
from functools import partial

import pexpect
from pexpect.replwrap import REPLWrapper


def thrust_signal(phase_settings, program_path, cwd=str(Path.cwd() / '..')):
    signal = 0
    for phase in phase_settings:
        input = f'{phase}\n{signal}\n'
        signal = int(run(f'python3 intcomputer.py {program_path}'.split(),
                         input=input.encode('utf-8'),
                         cwd=cwd, capture_output=True).stdout)
    return int(signal)


def feedback_loop(phase_settings, program_path, cwd=str(Path.cwd() / '..')):
    amplifiers = [REPLWrapper(f'python3 ../intcomputer.py -p "> " {program_path}', '> ', None) for i in 'abcde']
    # init phases
    for amplifier, phase in zip(amplifiers, phase_settings):
        try:
            amplifier.run_command(str(phase), timeout=2)
        except (pexpect.TIMEOUT, pexpect.EOF):
            print('Failed at initialization')
    signal = str(0)
    running = True
    while running:
        for c, amplifier in zip('abcde', amplifiers):
            try:
                signal = amplifier.run_command(signal, timeout=1).splitlines()[0]
            except (pexpect.EOF, OSError):
                running = False
                break
    return int(signal)


def main2():
    program = Path(sys.argv[1]).resolve()

    phase_settings = itertools.permutations(range(5, 10), 5)
    fl = partial(feedback_loop, program_path=program)
    with Pool(16) as p:
        signals = p.map(fl, phase_settings)
    print('Best signal part 2:', max(signals))


def main():
    program = Path(sys.argv[1]).resolve()

    phase_settings = itertools.permutations(range(5), 5)
    ts = partial(thrust_signal, program_path=program)
    with Pool(16) as p:
        signals = p.map(ts, phase_settings)

    print('Best signal part 1:', max(signals))


if __name__ == '__main__':
    main()
    main2()
