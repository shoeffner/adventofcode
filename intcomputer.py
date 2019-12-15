import time
import threading
import queue
from functools import lru_cache
from enum import IntEnum
from pathlib import Path


def parse_program(string):
    return map(int, string.split(','))


def load_program(program_file_name):
    return parse_program((Path(__file__).parent / program_file_name).read_text())


class ParameterTypes(IntEnum):
    READ = 0
    WRITE = 1


class Opcode:
    def __init__(self, function, *parameter_types):
        self.function = function
        self.parameter_types = parameter_types

    @property
    @lru_cache()
    def stride(self):
        return len(self.parameter_types) + 1

    def __call__(self, *params):
        return self.function(*params)

    def __str__(self):
        return f'[{self.function.__name__.split("_")[-1]}/{self.stride - 1}]'


class Memory(list):
    def ensure_length(self, key):
        if isinstance(key, int):
            min_size = key
        else:
            min_size = key.stop
        if min_size < 0:
            raise IndexError('Negative indices are not allowed.')
        while min_size >= len(self):
            self.append(0)

    def __setitem__(self, key, value):
        self.ensure_length(key)
        super().__setitem__(key, value)

    def __getitem__(self, key):
        self.ensure_length(key)
        return super().__getitem__(key)


class IntComputer(threading.Thread):
    def __init__(self, memory=None, timeout=.3):
        self.instruction_pointer = 0
        self.relative_base = 0
        self.memory = Memory(memory if memory is not None else [99])
        self.timeout = timeout
        self._terminated = False
        self.stdin = queue.Queue(1)
        self.stdout = queue.Queue(1)
        self.lock = threading.Semaphore()
        R = ParameterTypes.READ
        W = ParameterTypes.WRITE
        self.opcodes = {
            1: Opcode(self._op_add, R, R, W),
            2: Opcode(self._op_multiply, R, R, W),
            3: Opcode(self._op_input, W),
            4: Opcode(self._op_output, R),
            5: Opcode(self._op_jump_if_true, R, R),
            6: Opcode(self._op_jump_if_false, R, R),
            7: Opcode(self._op_less_than, R, R, W),
            8: Opcode(self._op_equals, R, R, W),
            9: Opcode(self._op_relative_base_offset, R),
            99: Opcode(self._op_halt)
        }

    def _parse_instruction(self, instruction):
        instruction, opcode = divmod(instruction, 100)
        op = self.opcodes[opcode]
        parameters = []
        for i, t in zip(range(1, op.stride), op.parameter_types):
            instruction, mode = divmod(instruction, 10)
            if mode == 0:
                addr = self.memory[self.instruction_pointer + i]
                if t == ParameterTypes.READ:
                    parameters.append(self.memory[addr])
                else:
                    parameters.append(addr)
            elif mode == 1:
                value = self.memory[self.instruction_pointer + i]
                parameters.append(value)
            elif mode == 2:
                addr = self.memory[self.instruction_pointer + i] + self.relative_base
                if t == ParameterTypes.READ:
                    parameters.append(self.memory[addr])
                else:
                    parameters.append(addr)
        return op, parameters

    @property
    def terminated(self):
        self.lock.acquire()
        t = self._terminated
        self.lock.release()
        return t

    @terminated.setter
    def terminated(self, value):
        self.lock.acquire()
        self._terminated = value
        self.lock.release()

    def __call__(self):
        while not self.terminated:
            try:
                instruction = self.memory[self.instruction_pointer]
                op, parameters = self._parse_instruction(instruction)
                self.instruction_pointer += op.stride
                op(*parameters)
            except StopIteration:
                self.terminated = True

    def thread(self):
        return threading.Thread(target=self.__call__, name='IntComputerProcess')

    def __enter__(self):
        self._thread = self.thread()
        self._thread.start()
        return self

    def __exit__(self, error, value, traceback):
        # self._thread.join()
        pass

    def _op_add(self, a, b, c):
        self.memory[c] = a + b

    def _op_multiply(self, a, b, c):
        self.memory[c] = a * b

    def _op_input(self, a):
        try:
            self.memory[a] = self.stdin.get(timeout=self.timeout)
        except queue.Empty:
            self.terminated = True

    def _op_output(self, a):
        try:
            self.stdout.put(a, timeout=self.timeout)
        except queue.Full:
            self.terminated = True

    def _op_jump_if_true(self, a, b):
        if a != 0:
            self.instruction_pointer = b

    def _op_jump_if_false(self, a, b):
        if a == 0:
            self.instruction_pointer = b

    def _op_less_than(self, a, b, c):
        self.memory[c] = int(a < b)

    def _op_equals(self, a, b, c):
        self.memory[c] = int(a == b)

    def _op_relative_base_offset(self, a):
        self.relative_base += a

    def _op_halt(self):
        raise StopIteration()


def main():
    ic = IntComputer(load_program('day5.input'))
    with ic as proc:
        proc.stdin.put(1)
        while not ic.terminated:
            time.sleep(0.1)
            if not proc.stdout.empty():
                out = proc.stdout.get()
                print(out)
    print(ic.memory)


if __name__ == '__main__':
    main()
