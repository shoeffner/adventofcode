import re

count = 0
for p in range(153517, 630395):
    sp = str(p)
    if sp != ''.join(sorted(sp)):
        continue
    if re.match(r'.*(.)(\1).*', sp) is None:
        continue
    count += 1
print(count)

