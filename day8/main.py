SIMPLE_SEGMENT_COUNTS = frozenset([2, 4, 3, 7])  # 1, 4, 7, 8
SEGMENT_SUPERSET = frozenset('abcdefg')
PATTERN_TO_DIGIT = {
    frozenset('abcefg'): 0,
    frozenset('cf'): 1,
    frozenset('acdeg'): 2,
    frozenset('acdfg'): 3,
    frozenset('bcdf'): 4,
    frozenset('abdfg'): 5,
    frozenset('abdefg'): 6,
    frozenset('acf'): 7,
    frozenset('abcdefg'): 8,
    frozenset('abcdfg'): 9,
}

with open('input') as f:
    lines = [s.strip().split(' | ') for s in f.readlines()]

    # Array of (signal patterns, four digit output), everything as a frozenset
    lines = [
        ([frozenset(p) for p in l[0].split()], [frozenset(p) for p in l[1].split()])
        for l in lines
    ]

total_simple_segment_count = sum(1 for l in lines for n in l[1] if len(n) in SIMPLE_SEGMENT_COUNTS)
print(f'Part 1 solution: {total_simple_segment_count}')

# 1 and 7 share two segments, 1 ^ 7 must be equivalent to a (set symmetric difference)
# 0, 6, 9 (all 6 lengths), if subtracted from the superset, result in 3 segments (c, d, e)
#   - when (c, d, e) is intersected with 1, you get c
#   - getting c implies you get f
#   - when (c, d, e) subtracts 4, you get e
#   - getting c and e implies you get d
# 4 - cdf = b
# Having all of them sans g means you have g

output_sum = 0
for patterns, digit_patterns in lines:
    one_pattern = four_pattern = seven_pattern = eight_pattern = None
    len_six_patterns = []
    for pattern in patterns:
        match len(pattern):
            case 2:
                one_pattern = pattern
            case 4:
                four_pattern = pattern
            case 3:
                seven_pattern = pattern
            case 7:
                eight_pattern = pattern
            case 6:
                len_six_patterns.append(pattern)

    cde_segments = set()
    for pattern in len_six_patterns:
        cde_segments.update(SEGMENT_SUPERSET - pattern)

    # Need to use tuple unpacking for single element sets unfortunately
    (a_seg,) = one_pattern ^ seven_pattern
    (c_seg,) = one_pattern & cde_segments
    (f_seg,) = one_pattern - {c_seg}
    (e_seg,) = cde_segments - four_pattern
    (d_seg,) = cde_segments - {c_seg, e_seg}
    (b_seg,) = four_pattern - {c_seg, d_seg, f_seg}
    (g_seg,) = SEGMENT_SUPERSET - {a_seg, b_seg, c_seg, d_seg, e_seg, f_seg}

    translation_map = {
        a_seg: 'a',
        b_seg: 'b',
        c_seg: 'c',
        d_seg: 'd',
        e_seg: 'e',
        f_seg: 'f',
        g_seg: 'g',
    }

    translated_patterns = {p: frozenset(translation_map[c] for c in p) for p in patterns}

    output = 0
    for digit_pattern in digit_patterns:
        output *= 10
        output = (output + PATTERN_TO_DIGIT[translated_patterns[digit_pattern]])
    output_sum += output

print(f'Part 2 solution: {output_sum}')