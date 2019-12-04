import re

count0 = 0
count1 = 0
for p in range(153517, 630395):
    sp = str(p)
    if sp != ''.join(sorted(sp)):
        continue
    m = re.search(r'(.)(\1)', sp)
    if m is None:
        continue
    nums = '0123456789'
    for i in nums:
        if sp.count(i) == 2:
            count1 += 1
            break
    count0 += 1

print(count0, count1)
