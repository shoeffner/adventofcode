import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
import intcomputer as c  # noqa

panel = np.zeros((201, 201), dtype=np.uint8)
painted = np.zeros(panel.shape, dtype=np.bool)
# 0: up, 1: right, 2: down, 3: left, ... use mod 4
robotrow, robotcol, robotdir = panel.shape[0] // 2, panel.shape[1] // 2, 0

# Pt. 2: Start on white pixel
panel[robotrow, robotcol] = 0

computer = c.IntComputer(c.load_program('11/program'))

with computer as ic:
    while not ic.terminated:
        ic.stdin.put(panel[robotrow, robotcol])
        color = ic.stdout.get()
        turn = ic.stdout.get()

        # color, turn = divmod(output, 10)
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
print(painted.sum())

plt.gray()
plt.imshow(panel, vmin=0, vmax=1)
plt.savefig('identifier.png')
