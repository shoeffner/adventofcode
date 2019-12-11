import pexpect
from pexpect.replwrap import REPLWrapper
import numpy as np
import matplotlib.pyplot as plt

panel = np.zeros((201, 201), dtype=np.uint8)
painted = np.zeros(panel.shape, dtype=np.bool)
# 0: up, 1: right, 2: down, 3: left, ... use mod 4
robotrow, robotcol, robotdir = panel.shape[0] // 2, panel.shape[1] // 2, 0

# Pt. 2: Start on white pixel
panel[robotrow, robotcol] = 1

computer = REPLWrapper(f'python3 ../intcomputer.py -p "> " program', '> ', None)

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
print(painted.sum(), i)
plt.gray()
plt.imshow(panel, vmin=0, vmax=1)
plt.savefig('identifier.png')
