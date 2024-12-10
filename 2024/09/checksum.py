import itertools
from pathlib import Path

diskmap = Path("example" if __debug__ else "input").read_text().strip()
if len(diskmap) & 1:
    diskmap = itertools.chain(diskmap, ["0"])
diskmap = list(map(int, diskmap))
disk = []
for fileid, (filesize, freespace) in enumerate(itertools.batched(diskmap, n=2)):
    disk.extend([fileid] * filesize)
    disk.extend([None] * freespace)
if __debug__:
    print(len(disk))


def compact_naive(indisk):
    disk = indisk.copy()
    left = 0
    right = len(disk) - 1
    while left < right:
        if __debug__:
            print("".join(map(str, map(lambda x: "." if x is None else x, disk))))
        while disk[left] is not None:
            left += 1
        while disk[right] is None:
            right -= 1
        if left >= right:
            break
        if __debug__:
            print(" " * left, "L", " " * (right - left - 1), "R", sep="")
        disk[left], disk[right] = disk[right], None
        left += 1
        right -= 1
    if __debug__:
        print("".join(map(str, map(lambda x: "." if x is None else x, disk))))
    return disk


def compact_blocks(indisk, diskmap):
    filepos = {fileid: indisk.index(fileid) for fileid in range(len(diskmap) // 2)}
    free = {}
    pos = 0
    for filesize, freespace in itertools.batched(diskmap, n=2):
        pos += filesize
        free[pos] = freespace
        pos += freespace
    if __debug__:
        print("files", filepos)
        print("free", free)

    files = list(enumerate(diskmap[::2]))
    freespace = list(enumerate(diskmap[1::2]))
    if __debug__:
        print(files)
        print(freespace)

    for fileid, size in reversed(files):
        for ptr, space in sorted(free.items()):
            if ptr >= filepos[fileid]:
                continue
            if space >= size:
                break
        else:
            continue
        free[ptr + size] = space - size
        del free[ptr]
        filepos[fileid] = ptr

    disk = [None] * len(indisk)
    for fileid, size in files:
        pos = filepos[fileid]
        for i in range(pos, pos + size):
            disk[i] = fileid

    if __debug__:
        print("".join(map(str, map(lambda x: "." if x is None else x, disk))))

    return disk


def checksum(disk):
    chksum = 0
    for idx, block in enumerate(disk):
        if block is None:
            continue
        chksum += idx * block
    return chksum


print(checksum(compact_naive(disk)))
print(checksum(compact_blocks(disk, diskmap)))
