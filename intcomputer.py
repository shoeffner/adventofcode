import itertools


class IntComputer:
    def __init__(self, memory=None):
        self.memory = memory if memory is not None else []
        self.instruction_pointer = 0
        self.opcodes = {
            1: Opcode(1, 4, add),
            2: Opcode(2, 4, multiply),
            99: Opcode(99, 1, halt)
        }

    def __call__(self):
        max_steps = 10000
        for step in itertools.count():
            if step == max_steps:
                print(f'Max steps {max_steps} reached')
                break
            op = self.opcodes[self.memory[self.instruction_pointer]]
            try:
                self.instruction_pointer = op(self.memory, self.instruction_pointer)
            except StopIteration:
                break

    def __getitem__(self, key):
        return self.memory[key]

    def __setitem__(self, key, value):
        self.memory[key] = value


def add(memory, summand0_addr, summand1_addr, result_addr):
    memory[result_addr] = memory[summand0_addr] + memory[summand1_addr]


def multiply(memory, factor0_addr, factor1_addr, result_addr):
    memory[result_addr] = memory[factor0_addr] * memory[factor1_addr]


def halt(memory):
    raise StopIteration()


class Opcode:
    def __init__(self, code, stride, callfun):
        self.code = code
        self.stride = stride
        self.callfun = callfun

    def __call__(self, memory, instruction_pointer):
        values = memory[instruction_pointer + 1:instruction_pointer + self.stride]
        self.callfun(memory, *values)
        return instruction_pointer + self.stride
