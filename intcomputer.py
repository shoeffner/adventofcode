import sys
import argparse
import itertools
from pathlib import Path


PROMPT = ''
LOGFILE = None
MEMFILE = None


class IntComputer:
    def __init__(self, memory=None):
        self.memory = memory if memory is not None else []
        self.instruction_pointer = 0
        self.opcodes = {
            1: Opcode(1, 4, add),
            2: Opcode(2, 4, multiply),
            3: Opcode(3, 2, read_input),
            4: Opcode(4, 2, write_output),
            5: Opcode(5, 3, jump_if_true),
            6: Opcode(6, 3, jump_if_false),
            7: Opcode(7, 4, less_than),
            8: Opcode(8, 4, equals),
            99: Opcode(99, 1, halt)
        }

    def __call__(self, verbose=False):
        max_steps = 10000
        for step in itertools.count():
            if step == max_steps:
                print(f'Max steps {max_steps} reached', file=LOGFILE)
                break
            instruction = self.memory[self.instruction_pointer]
            instruction, opcode = divmod(instruction, 100)

            parameter_modes = []
            while instruction:
                instruction, mode = divmod(instruction, 10)
                parameter_modes.append(mode)
            op = self.opcodes[opcode]
            try:
                self.instruction_pointer = op(self.memory, self.instruction_pointer, parameter_modes, verbose)
            except StopIteration:
                if PROMPT:
                    print('\n', end=PROMPT, file=sys.stdout)
                break
        return 0

    def __getitem__(self, key):
        return self.memory[key]

    def __setitem__(self, key, value):
        self.memory[key] = value


def handle_mode(memory, mode, value):
    if mode == 0:
        return memory[value]
    if mode == 1:
        return value
    raise ValueError(f'Unknown mode {mode}')


def add(memory, modes, summand0, summand1, result_addr):
    summand0 = handle_mode(memory, modes[0], summand0)
    summand1 = handle_mode(memory, modes[1], summand1)
    memory[result_addr] = summand0 + summand1


def multiply(memory, modes, factor0, factor1, result_addr):
    factor0 = handle_mode(memory, modes[0], factor0)
    factor1 = handle_mode(memory, modes[1], factor1)
    memory[result_addr] = factor0 * factor1


def read_input(memory, modes, addr):
    memory[addr] = int(input(PROMPT))
    if LOGFILE:
        print('INPUT:', memory[addr], file=LOGFILE)


def write_output(memory, modes, value):
    value = handle_mode(memory, modes[0], value)
    print(value, file=sys.stdout, end='')
    if LOGFILE:
        print('OUTPUT:', value, file=LOGFILE)


def jump_if_true(memory, modes, comp, jump_addr):
    comp = handle_mode(memory, modes[0], comp)
    jump_addr = handle_mode(memory, modes[1], jump_addr)
    if comp != 0:
        return jump_addr


def jump_if_false(memory, modes, comp, jump_addr):
    comp = handle_mode(memory, modes[0], comp)
    jump_addr = handle_mode(memory, modes[1], jump_addr)
    if comp == 0:
        return jump_addr


def less_than(memory, modes, comp0, comp1, result_addr):
    comp0 = handle_mode(memory, modes[0], comp0)
    comp1 = handle_mode(memory, modes[1], comp1)
    memory[result_addr] = int(comp0 < comp1)


def equals(memory, modes, comp0, comp1, result_addr):
    comp0 = handle_mode(memory, modes[0], comp0)
    comp1 = handle_mode(memory, modes[1], comp1)
    memory[result_addr] = int(comp0 == comp1)


def halt(memory, modes):
    raise StopIteration()


class Opcode:
    def __init__(self, code, stride, callfun):
        self.code = code
        self.stride = stride
        self.callfun = callfun

    def __call__(self, memory, instruction_pointer, parameter_modes=None, verbose=False):
        if parameter_modes is None:
            parameter_modes = [0] * (self.stride - 1)
        elif len(parameter_modes) < (self.stride - 1):
            parameter_modes += [0] * (self.stride - 1 - len(parameter_modes))

        parameters = memory[instruction_pointer + 1:instruction_pointer + self.stride]
        instruction_pointer += self.stride
        try:
            if verbose:
                print(f'{self.code} [{self.callfun.__name__}]{parameters}{parameter_modes}', file=LOGFILE)
            ip = self.callfun(memory, parameter_modes, *parameters)
            if MEMFILE:
                print(memory, file=MEMFILE)
            if ip is not None:
                instruction_pointer = ip
        except IndexError as e:
            print(f'Error in {self.callfun.__name__}: {parameters}', file=LOGFILE)
            print(memory, instruction_pointer, file=LOGFILE)
            raise e
        return instruction_pointer


def main(sys_argv=sys.argv):
    global PROMPT, LOGFILE, MEMFILE
    parser = argparse.ArgumentParser()
    parser.add_argument('program', type=lambda x: list(map(int, Path(x).read_text().split(','))))
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-p', '--prompt', nargs='?', default=PROMPT)
    parser.add_argument('-l', '--logfile', nargs='?', type=argparse.FileType('w'))
    parser.add_argument('-m', '--memfile', nargs='?', type=argparse.FileType('w'))
    args = parser.parse_args()
    PROMPT = args.prompt
    LOGFILE = args.logfile
    MEMFILE = args.memfile

    if args.verbose:
        print(f'Program: {args.program}', file=LOGFILE)
    computer = IntComputer(args.program)
    computer(verbose=args.verbose)
    if args.verbose:
        print(f'Memory: {computer.memory}', file=LOGFILE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
