days = 256
fish = [0] * 9

infish = list(map(int, input().split(',')))
for f in infish:
    fish[f] += 1

for day in range(days):
    spawners = fish.pop(0)
    fish[6] += spawners
    fish.append(spawners)

print(sum(fish))
