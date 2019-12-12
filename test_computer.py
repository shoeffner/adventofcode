import unittest

from computer import IntComputer, load_program, parse_program


class TestSimpleSingleOpcodes(unittest.TestCase):
    def test_halt(self):
        ic = IntComputer([99])
        ic()
        self.assertEqual(ic.terminated, True)


class TestDay2(unittest.TestCase):
    def test_day2_example1(self):
        ic = IntComputer(parse_program('1,9,10,3,2,3,11,0,99,30,40,50'))
        ic()
        self.assertEqual(ic.memory[0], 3500)

    def test_day2_small_examples(self):
        examples = [[[1, 0, 0, 0, 99], [2, 0, 0, 0, 99]],
                    [[2, 3, 0, 3, 99], [2, 3, 0, 6, 99]],
                    [[2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]],
                    [[1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]]]
        for memin, memout in examples:
            ic = IntComputer(memin)
            ic()
            self.assertEqual(ic.memory, memout, f'{memin} yields {ic.memory}, should be {memout}')

    def test_day2_result_part1(self):
        ic = IntComputer(load_program('test_programs/day2.input'))
        ic.memory[1] = 12
        ic.memory[2] = 2
        ic()
        self.assertEqual(ic.memory[0], 2894520)

    def test_day2_result_part2(self):
        program = load_program('test_programs/day2.input')
        ic = IntComputer(program)
        ic.memory[1] = 93
        ic.memory[2] = 42
        ic()
        self.assertEqual(ic.memory[0], 19690720)


class TestDay5(unittest.TestCase):
    def test_in_is_out(self):
        program = [3, 0, 4, 0, 99]
        ic = IntComputer(program)
        with ic as proc:
            proc.stdin.put(5)
            a = proc.stdout.get()
        self.assertEqual(a, 5)

    def test_result_part1(self):
        ic = IntComputer(load_program('test_programs/day5.input'))
        import time
        with ic as proc:
            proc.stdin.put(1)
            while not ic.terminated:
                time.sleep(0.1)
                if not proc.stdout.empty():
                    dc = proc.stdout.get()
        self.assertEqual(dc, 10987514)

    def test_result_part2(self):
        ic = IntComputer(load_program('test_programs/day5.input'))
        import time
        with ic as proc:
            proc.stdin.put(5)
            while not ic.terminated:
                time.sleep(0.1)
                if not proc.stdout.empty():
                    dc = proc.stdout.get()
        self.assertEqual(dc, 14195011)


class TestDay7(unittest.TestCase):
    def test_result_part1(self):
        program = list(load_program('test_programs/day7.input'))
        from itertools import permutations
        best = 0
        for phases in permutations(range(5)):
            amps = [IntComputer(program) for i in 'abcde']
            threads = [amp.thread() for amp in amps]
            for amp, thread, phase in zip(amps, threads, phases):
                thread.start()
                amp.stdin.put(phase)
            out = 0
            for amp in amps:
                amp.stdin.put(out)
                out = amp.stdout.get()
            for thread in threads:
                thread.join()
            if out > best:
                best = out
        self.assertEqual(best, 19650)

    def test_result_part2(self):
        program = list(load_program('test_programs/day7.input'))
        from itertools import permutations
        best = 0
        for phases in permutations(range(5, 10)):
            amps = [IntComputer(program) for i in 'abcde']
            threads = [amp.thread() for amp in amps]
            for amp, thread, phase in zip(amps, threads, phases):
                thread.start()
                amp.stdin.put(phase)
            out = 0
            while not amps[0].terminated:
                for amp in amps:
                    amp.stdin.put(out)
                    out = amp.stdout.get()
            for thread in threads:
                thread.join()
            if out > best:
                best = out
        self.assertEqual(best, 35961106)


class TestDay9(unittest.TestCase):
    def test_result_part1(self):
        ic = IntComputer(load_program('test_programs/day9.input'))
        with ic as proc:
            proc.stdin.put(1)
            out = proc.stdout.get()
        self.assertEqual(out, 2682107844)

    def test_result_part2(self):
        ic = IntComputer(load_program('test_programs/day9.input'))
        with ic as proc:
            proc.stdin.put(2)
            out = proc.stdout.get()
        self.assertEqual(out, 34738)
