from pathlib import Path
import functools

import numpy as np


def fft(signal, pattern):
    complete_pattern = np.empty((len(signal), len(signal)), dtype=np.int)
    for num, elem in enumerate(signal, 1):
        tile_pattern = np.tile(np.repeat(pattern, num), len(signal) // len(pattern) + 1)[1:len(signal) + 1]
        complete_pattern[num - 1] = tile_pattern
    complete_signal = np.tile(signal, [len(signal), 1])
    return np.abs(np.sum(complete_signal * complete_pattern, axis=1)) % 10


def fast_fft(signal, pattern):
    n_signal = np.empty_like(signal)
    for num, _elem in enumerate(signal, 1):
        tile_pattern = np.tile(np.repeat(pattern, num), len(signal) // len(pattern) + 1)[1:len(signal) + 1]
        n_signal[num - 1] = np.abs(signal @ tile_pattern) % 10
    return n_signal


@functools.lru_cache()
def prepare_pattern(len_signal, digit):
    pattern = [0, 1, 0, -1]
    tile_pattern = np.tile(np.repeat(pattern, digit), len_signal // len(pattern) + 1)[1:len_signal + 1]
    return tile_pattern


def super_fast_fft(signal, offset):
    N = len(signal)
    for i in range(N):
        start_plus = i
        start_minus = 2 + 3 * (i + offset)
        step = 4 * (i + offset + 1)
        for j in range(min(i + offset + 1, N - i)):
            if j == 0:
                signal[i] = sum(signal[start_plus + j::step]) - sum(signal[start_minus + j::step])
            else:
                signal[i] += sum(signal[start_plus + j::step]) - sum(signal[start_minus + j::step])
        signal[i] = abs(signal[i]) % 10
    return signal


def lower_right_quadrant_fft(signal):
    for i in range(len(signal) - 1, 0, -1):
        signal[i - 1] = abs(signal[i - 1] + signal[i]) % 10
    return signal


def main():
    test = False
    if test:
        signal = '03036732577212944063491565474664'
        offset = int(signal[:7])
        repeat = 10000
        phases = 100
    else:
        signal = Path('16/input').read_text().strip()
        offset = int(signal[:7])
        repeat = 10000
        phases = 100
    signal = np.array(list(map(int, signal)) * repeat, dtype=np.int)[offset:]
    print('Offset:', offset)
    print('Len signal:', len(signal))

    import time
    start = time.time()
    last = start
    for phase in range(phases):
        print(f'Phase {phase + 1} begins')
        signal = lower_right_quadrant_fft(signal)
        this = time.time()
        print(f'Phase {phase + 1}: Time: {this - last:.2f} s')
        last = this
    print(f'Total time: {last - start:.2f} s')
    print(''.join(map(str, signal[:8])))


if __name__ == '__main__':
    main()
