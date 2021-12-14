from collections import defaultdict, Counter
from itertools import chain


def get_solution_statistic_from_letter_counts(letter_counts):
    most_common = letter_counts.most_common()
    return most_common[0][1] - most_common[-1][1]


with open('input') as f:
    polymer_template = f.readline().strip()
    f.readline()

    pair_to_element = defaultdict(str)
    for pair, element in map(lambda l: l.strip().split(' -> '), f.readlines()):
        pair_to_element[pair] = element

    pair_counts = defaultdict(int)
    for i in range(len(polymer_template) - 1):
        window = polymer_template[i:i + 2]

        pair_counts[window] += 1

    letter_counts = Counter(polymer_template)

TOTAL_STEPS = 40
for current_step in range(1, TOTAL_STEPS + 1):
    temp_pair_counts = dict(pair_counts)
    for pair, count in temp_pair_counts.items():
        if count <= 0:
            continue

        new_char = pair_to_element[pair]
        pair_counts[pair] -= count
        pair_counts[f'{pair[0]}{new_char}'] += count
        pair_counts[f'{new_char}{pair[1]}'] += count
        letter_counts[new_char] += count

    if current_step == 10:
        print(f'Part 1 solution: {get_solution_statistic_from_letter_counts(letter_counts)}')
    elif current_step == 40:
        print(f'Part 2 solution: {get_solution_statistic_from_letter_counts(letter_counts)}')