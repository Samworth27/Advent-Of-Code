import re

from aoc_util.inputs import parse_input, fields

DAY = 19
YEAR = 2015

data = parse_input((DAY, YEAR))


replacements = {}
for replacement in data[:-2]:
    mol1, mol2 = fields(replacement, split_char='=>',
                        field_func=lambda x: x.strip())
    if mol1 not in replacements:
        replacements[mol1] = []
    replacements[mol1].append(mol2)


def inverse_replacements(replacements):
    inverted_replacements = {}
    for target, options in replacements.items():
        for option in options:
            if option not in inverted_replacements:
                inverted_replacements[option] = []
            inverted_replacements[option].append(target)
    return inverted_replacements


def possible_swaps(start_molecule, replacements):
    new_molecules = set()
    for target in replacements:
        for match in re.finditer(target, start_molecule):
            swap_start, swap_finish = match.span()
            target = start_molecule[swap_start:swap_finish]
            for replacement in replacements[target]:
                new_molecule = start_molecule[:swap_start] + \
                    replacement+start_molecule[swap_finish:]
                new_molecules.add(new_molecule)
    return new_molecules


def valid_swaps(all_swaps):
    def valid(x):
        if x == 'e':
            return True
        if 'e' not in x:
            return True
        return False

    return [swap for swap in all_swaps if valid(swap)]


test_case = {
    'e': ["H", "O"],
    'H': ["HO", "OH"],
    "O": ["HH"]
}

# print(inverse_replacements(test_case))


def reverse_engineer(target_molecule, replacements):
    replacements = inverse_replacements(replacements)
    memo = {}
    test = {}
    stats = {
        'calcs': 0,
        'access': 0,
        'solutions': 0
    }

    def dfs(string, i):
        if string == 'e':
            stats['solutions'] += 1
            print(f"\nSolution at {i} steps\n")
            return i
        if string not in memo:
            stats['calcs'] += 1
            best = float('inf')
            candidates = valid_swaps(possible_swaps(string, replacements))
            for candidate in sorted(candidates, key=lambda x: len(x)):
                best = min(best, dfs(candidate, i+1))
            memo[string] = best
        else:
            stats['access'] += 1

        print(
            f"Calculations: {stats['calcs']:07} Memo Access: {stats['access']:07} Solutions Found {stats['solutions']:05}", end='\r')
        return memo[string]

    return dfs(target_molecule, 0)

# print(reverse_engineer('HOHOHO', test_case))


reverse_engineer(data[-1], replacements)
