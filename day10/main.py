from collections import deque
from functools import reduce

OPENING_PARENS = '([{<'
CLOSING_PARENS = ')]}>'
REVERSE_PARENS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
SYNTAX_CHECKER_SCORE_MAP = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
AUTOCOMPLETE_SCORE_MAP = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

with open('input') as f:
    lines = [l.strip() for l in f.readlines()]

first_invalid_chars = []
autocomplete_scores = []
for line in lines:
    stack = deque()
    repair_sequence = []
    invalid_line = False
    for c in line:
        if c in OPENING_PARENS:
            stack.append(c)
            continue

        # no else, because we assume input has only either open/closed parens
        if not stack or stack.pop() != REVERSE_PARENS[c]:
            invalid_line = True
            first_invalid_chars.append(c)
            break

    if not invalid_line:  # If it's not invalid, then it must be incomplete
        autocomplete_scores.append(reduce(
            lambda a, b: (a * 5) + AUTOCOMPLETE_SCORE_MAP[b],
            (REVERSE_PARENS[c] for c in reversed(stack)),
            0,
        ))

print(autocomplete_scores)
print(f'Part 1 solution: {sum(SYNTAX_CHECKER_SCORE_MAP[c] for c in first_invalid_chars)}')

autocomplete_scores.sort()
print(f'Part 2 solution: {autocomplete_scores[len(autocomplete_scores) // 2]}')