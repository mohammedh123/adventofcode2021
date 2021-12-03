from collections import Counter


def most_common_bit_at_idx(binary_strings, idx):
    counter = Counter(s[idx] for s in binary_strings)
    return '1' if counter['0'] == counter['1'] else counter.most_common()[0][0]

    
def least_common_bit_at_idx(binary_strings, idx):
    counter = Counter(s[idx] for s in binary_strings)
    return '0' if counter['0'] == counter['1'] else counter.most_common()[-1][0]


def get_filtered_rating_value(binary_strings, predicate):
    current = binary_strings
    current_bit_idx = 0
    while len(current) > 1:
        filter_value = predicate(current, current_bit_idx)        
        current = [s for s in current if s[current_bit_idx] == filter_value]
        current_bit_idx += 1
    return int(current[0], 2)


with open('input') as f:
    binary_strings = [l.strip() for l in f.readlines()]
    
gamma_rate_str = ''.join(most_common_bit_at_idx(binary_strings, n) for n in range(len(binary_strings[0])))
gamma_rate = int(gamma_rate_str, 2)

# Flip the gamma rate bitstring and convert it to decimal
epsilon_rate = int(''.join('1' if c == '0' else '0' for c in gamma_rate_str), 2)
print(f'Part 1 answer: {gamma_rate * epsilon_rate}')

oxygen_generator_rating = get_filtered_rating_value(binary_strings, most_common_bit_at_idx)
co2_scrubber_rating = get_filtered_rating_value(binary_strings, least_common_bit_at_idx)

print(f'Part 2 answer: {oxygen_generator_rating * co2_scrubber_rating}')