import sys
from pathlib import Path

image = Path(sys.argv[1]).read_text().strip()

w = 25
h = 6
l = len(image) // w // h

fewest_zeros = w * h + 1
checksum = 0
for i in range(l):
    start = i * w * h
    end = start + w * h
    zeros = image[start:end].count('0')
    if zeros < fewest_zeros:
        fewest_zeros = zeros
        checksum = image[start:end].count('1') * image[start:end].count('2')
print(checksum)


decoded = ['2'] * w * h
for x in range(w):
    for y in range(h):
        for z in range(l):
            if decoded[y * w + x] == '2':
                decoded[y * w + x] = image[z * w * h + y * w + x]

decoded = ''.join(decoded)
for row in range(h):
    print(decoded[row * w:(row + 1) * w])
