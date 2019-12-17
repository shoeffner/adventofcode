from intcomputer import IntComputer, load_program
import queue

# ic = IntComputer(load_program('17/input'))
#
# lines = [[]]
# with ic as proc:
#     while True:
#         try:
#             char = ic.stdout.get(timeout=0.2)
#             if char != 10:
#                 lines[-1].append(char)
#             else:
#                 lines.append([])
#         except queue.Empty:
#             break
#
# lines = lines[:-2]
# total = 0
# for ri, row in enumerate(lines[1:-1], 1):
#     for ci, val in enumerate(row[1:-1], 1):
#         if 35 == val == lines[ri - 1][ci] == lines[ri + 1][ci] == lines[ri][ci - 1] == lines[ri][ci + 1]:
#             total += ri * ci
# print('alignment', total)



P = list(map(ord, 'B,C,C,B,C,A,B,A,C,A')) + [10]
A = list(map(ord, 'R,12,L,6,L,6,L,8')) + [10]
B = list(map(ord, 'L,4,L,6,L,8,L,12')) + [10]
C = list(map(ord, 'L,8,R,12,L,12')) + [10]
V = [ord('n'), 10]

program_input = P + A + B + C + V
print(program_input)
ic = IntComputer(load_program('17/input'))
ic.memory[0] = 2
with ic as proc:
    N = 0
    while True:
        try:
            print(chr(proc.stdout.get(timeout=.3)), end='')
            N += 1
        except queue.Empty:
            print('map loaded')
            break

    for i, x in enumerate(program_input):
        try:
            ic.stdin.put(x, block=True, timeout=.3)
        except queue.Full:
            pass

    result = []
    while True:
        try:
            r = proc.stdout.get(timeout=.3)
            result.append(r)
        except queue.Empty:
            print('error in output')
            break
    print(result[-1])
