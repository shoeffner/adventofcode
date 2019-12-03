import sys

module_fuels = [int(line) // 3 - 2 for line in sys.stdin]
fuel = []
for module_fuel in module_fuels:
    fuel.append(module_fuel)
    fuel_fuel = fuel[-1] // 3 - 2
    while fuel_fuel > 0:
        fuel[-1] += fuel_fuel
        fuel_fuel = fuel_fuel // 3 - 2
print(sum(module_fuels), sum(fuel))
