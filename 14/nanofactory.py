import sys
from pathlib import Path
from collections import defaultdict
from pprint import pprint


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


def resolve_ingredient(material, quantity, reactions, remainders=None):
    ingredients = reactions[material][0]
    produces = reactions[material][1][material]
    # print(quantity, material, 'required:', ingredients, '=>', produces)

    if remainders is not None and material in remainders:
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
        remainders[material] = produces - remainder
    return {m: q * reaction_times for m, q in ingredients.items()}, remainders


def calculate(reactions):
    fuel_reaction = reactions['FUEL'].copy()
    fuel_quantity = fuel_reaction[1]['FUEL']
    only_ore_required = False
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
        ingredients, _remainder = resolve_ingredient(mat, quant, reactions, {})
        ore = ingredients['ORE']
        # print(f'{quant} {mat} requires {ore} ORE')
        total += ore
    return fuel_quantity * total


def main():
    reactions = parse(sys.argv[1])
    # pprint(reactions)
    num_ore = calculate(reactions)
    print(f'Number of ORE needed: {num_ore}')


if __name__ == '__main__':
    main()
