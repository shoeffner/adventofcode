import pexpect
from pexpect.replwrap import REPLWrapper
import numpy as np

panel = np.zeros((1001, 1001), dtype=np.uint8)
painted = np.zeros((1001, 1001), dtype=np.bool)
# 0: up, 1: right, 2: down, 3: left, ... use mod 4
robotrow, robotcol, robotdir = 500, 500, 0

computer = REPLWrapper(f'python3 ../intcomputer.py -v -l log.log -p "> " program', '> ', None)

max_steps = 10000
for i in range(max_steps):
    try:
        output = computer.run_command(str(panel[robotrow, robotcol]), timeout=2)
    except (pexpect.EOF, pexpect.TIMEOUT, OSError):
        break
    try:
        output = int(output)
    except ValueError:
        print('Output no int:', output)
        break
    color, turn = divmod(output, 10)
    painted[robotrow, robotcol] = True
    panel[robotrow, robotcol] = color

    robotdir = (robotdir + -1 * (1 - turn) + turn) % 4
    if robotdir == 0:
        robotrow -= 1
    elif robotdir == 1:
        robotcol += 1
    elif robotdir == 2:
        robotrow += 1
    elif robotdir == 3:
        robotcol -= 1
else:
    print('max steps reached')
import matplotlib.pyplot as plt
plt.imshow(panel)
print(painted.sum())
