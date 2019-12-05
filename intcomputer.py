import sys
import argparse
import itertools
from pathlib import Path


class IntComputer:
    def __init__(self, memory=None):
        self.memory = memory if memory is not None else []
        self.instruction_pointer = 0
        self.opcodes = {
            1: Opcode(1, 4, add),
            2: Opcode(2, 4, multiply),
            3: Opcode(3, 2, read_input),
            4: Opcode(4, 2, write_output),
            99: Opcode(99, 1, halt)
        }

    def __call__(self):
        max_steps = 10000
        output_buffer = []
        for step in itertools.count():
            if step == max_steps:
                print(f'Max steps {max_steps} reached', file=sys.stderr)
                break
            instruction = self.memory[self.instruction_pointer]
            instruction, opcode = divmod(instruction, 100)

            parameter_modes = []
            while instruction:
                instruction, mode = divmod(instruction, 10)
                parameter_modes.append(mode)
            op = self.opcodes[opcode]
            try:
                self.instruction_pointer, output = op(self.memory, self.instruction_pointer, parameter_modes)
                if output is not None:
                    output_buffer.append(output)
            except StopIteration:
                break
        return int(''.join(map(str, output_buffer)))

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
    memory[addr] = int(sys.stdin.readline().strip())


def write_output(memory, modes, value):
    return handle_mode(memory, modes[0], value)


def halt(memory, modes):
    raise StopIteration()


class Opcode:
    def __init__(self, code, stride, callfun):
        self.code = code
        self.stride = stride
        self.callfun = callfun

    def __call__(self, memory, instruction_pointer, parameter_modes=None):
        if parameter_modes is None:
            parameter_modes = [0] * (self.stride - 1)
        elif len(parameter_modes) < (self.stride - 1):
            parameter_modes += [0] * (self.stride - 1 - len(parameter_modes))

        parameters = memory[instruction_pointer + 1:instruction_pointer + self.stride]
        try:
            print(f'{self.code} [{self.callfun.__name__}]{parameters}{parameter_modes}')
            output = self.callfun(memory, parameter_modes, *parameters)
        except IndexError as e:
            print(f'Error in {self.callfun.__name__}: {parameters}', file=sys.stderr)
            print(memory, instruction_pointer, file=sys.stderr)
            raise e
        return instruction_pointer + self.stride, output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('program', type=lambda x: list(map(int, Path(x).read_text().split(','))))
    args = parser.parse_args()

    print(f'Program: {args.program}')
    computer = IntComputer(args.program)
    output = computer()
    print(f'Output: {output}')
    print(f'Memory: {computer.memory}')
