import sys
sys.path.append('..')
from intcomputer import IntComputer  # noqa

memory = [int(x) for x in sys.stdin.read().split(',')]


def crun(memory, noun, verb, control):
    computer = IntComputer(memory)
    computer[1], computer[2] = noun, verb
    computer()
    if computer[0] == control:
        return 100 * noun + verb


def run(memory, noun, verb, control):
    memory[1], memory[2] = noun, verb
    op_idx = 0
    while memory[op_idx] in [1, 2, 99]:
        opcode = memory[op_idx]
        if opcode == 99:
            if memory[0] == control:
                return 100 * noun + verb
            else:
                return False
        r0, r1, r2 = op_idx + 1, op_idx + 2, op_idx + 3
        if opcode == 1:
            memory[memory[r2]] = memory[memory[r0]] + memory[memory[r1]]
        elif opcode == 2:
            memory[memory[r2]] = memory[memory[r0]] * memory[memory[r1]]
        op_idx += 4
    else:
        return False


for noun in range(99):
    for verb in range(99):
        result = crun(memory.copy(), noun, verb, 19690720)
        if result:
            print(result)
            sys.exit(0)
