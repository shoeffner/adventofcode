import sys
from pathlib import Path
from collections import defaultdict
from pprint import pprint
from copy import deepcopy


def parse(filename):
    reactions = {}
    for line in Path(filename).read_text().splitlines():
        reaction = [{}, {}]
        inputs, outputs = line.split(' => ')
        raw_ins = inputs.split(', ')
        for raw in raw_ins:
            quant, mat = raw.split(' ')
            reaction[0][mat.strip()] = int(quant)
        quant, mat = outputs.split(' ')
        reaction[1][mat.strip()] = int(quant)
        reactions[mat] = reaction
    return reactions


def resolve_ingredient(material, quantity, reactions, remainders=None, reduce_remainders=True):
    ingredients = reactions[material][0]
    produces = reactions[material][1][material]
    # print(quantity, material, 'required:', ingredients, '=>', produces)

    if remainders is not None and material in remainders and reduce_remainders:
        remains = remainders[material]
        if remains <= quantity:
            quantity -= remains
            del remainders[material]
        else:
            remainders[material] -= quantity
            quantity = 0

    reaction_times, remainder = divmod(quantity, produces)
    if remainder:
        reaction_times += 1
        remainders[material] = remainders.get(material, 0) + produces - remainder
    return {m: q * reaction_times for m, q in ingredients.items()}, remainders


def calculate(reactions, remainders=None):
    fuel_reaction = deepcopy(reactions['FUEL'])
    only_ore_required = False
    if remainders is None:
        remainders = {}
    while not only_ore_required:
        only_ore_required = True
        for mat, quant in fuel_reaction[0].copy().items():
            ingredients, remainders = resolve_ingredient(mat, quant, reactions, remainders)
            if 'ORE' in ingredients:
                # print('ORE in', ingredients)
                continue
            # print('Result:', ingredients, '\n')
            only_ore_required = False
            del fuel_reaction[0][mat]
            for ing, quant in ingredients.items():
                if ing in fuel_reaction[0]:
                    fuel_reaction[0][ing] += quant
                else:
                    fuel_reaction[0][ing] = quant
            break
    # print(fuel_reaction[0])
    total = 0
    for mat, quant in fuel_reaction[0].items():
        ingredients, remainders = resolve_ingredient(mat, quant, reactions, remainders, False)
        ore = ingredients['ORE']
        # print(f'{quant} {mat} requires {ore} ORE')
        total += ore
    return total, remainders


def bisection(reactions, low, high, goal, tol=1):
    mem = {}
    N = 0
    while N < 100:
        mid = (low + high) // 2
        lr = deepcopy(reactions)
        mr = deepcopy(reactions)
        hr = deepcopy(reactions)

        for k in lr['FUEL'][0]:
            lr['FUEL'][0][k] *= low
            mr['FUEL'][0][k] *= mid
            hr['FUEL'][0][k] *= high
        lr['FUEL'][1]['FUEL'] = low
        mr['FUEL'][1]['FUEL'] = mid
        hr['FUEL'][1]['FUEL'] = high

        if mid not in mem:
            ore_mid, _rem = calculate(mr)
            mem[mid] = ore_mid
        else:
            ore_mid = mem[mid]

        if ore_mid - goal == 0 or high == low + 1:
            return low

        if high not in mem:
            ore_high, _rem = calculate(hr)
            mem[high] = ore_high
        else:
            ore_high = mem[high]

        if low not in mem:
            ore_low, _rem = calculate(lr)
            mem[low] = ore_low
        else:
            ore_low = mem[low]

        if ore_mid < goal:
            low = mid
        if ore_mid > goal:
            high = mid
        N += 1


def main():
    reactions = parse(sys.argv[1])
    remainders = {}
    num_ore, remainders = calculate(reactions, remainders)
    print('Minimum ORE required for 1 FUEL:', num_ore)
    max_ore = 1000000000000
    fuel_min = max_ore // num_ore + 1
    fuel_max = int(fuel_min * 1.3)
    max_fuel = bisection(reactions, fuel_min, fuel_max, max_ore)
    print(f'Maximum FUEL using {max_ore} ORE:', max_fuel)


if __name__ == '__main__':
    main()
