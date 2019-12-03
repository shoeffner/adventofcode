import sys

memory = [int(x) for x in sys.stdin.read().split(',')]
memory[1], memory[2] = 12, 2

op_idx = 0
while memory[op_idx] in [1, 2, 99]:
    opcode = memory[op_idx]
    if opcode == 99:
        print(memory[0])
        sys.exit(0)
    r0, r1, r2 = op_idx + 1, op_idx + 2, op_idx + 3
    if opcode == 1:
        memory[memory[r2]] = memory[memory[r0]] + memory[memory[r1]]
    elif opcode == 2:
        memory[memory[r2]] = memory[memory[r0]] * memory[memory[r1]]
    op_idx += 4
else:
    sys.exit(1)
