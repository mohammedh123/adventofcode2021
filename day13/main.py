import re


def print_dots(dots):
    width = max(x for x, y in dots) + 1
    height = max(y for x, y in dots) + 1
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    for x, y in dots:
        grid[y][x] = '#'

    for row in grid:
        print(''.join(map(str, row)))


def fold_up(current_dots, fold_y):
    height = max(y for x, y in current_dots) + 1
    updated_dots = set()
    for x, y in current_dots:
        new_x, new_y = x, y
        if y >= fold_y:
            new_y = height - 1 - y

        updated_dots.add((new_x, new_y))

    return updated_dots


def fold_left(current_dots, fold_x):
    width = max(x for x, y in current_dots) + 1
    updated_dots = set()
    for x, y in current_dots:
        new_x, new_y = x, y
        if x >= fold_x:
            new_x = width - 1 - x

        updated_dots.add((new_x, new_y))

    return updated_dots


def fold_paper(dots, folds_to_perform):
    current_dots = dots
    for fold_type, fold_location in folds_to_perform:
        if fold_type == 'y':
            current_dots = fold_up(current_dots, fold_location)
        elif fold_type == 'x':
            current_dots = fold_left(current_dots, fold_location)
    return current_dots


with open('input') as f:
    folds = []
    dots = set()
    for l in f.readlines():
        l = l.strip()
        if l.startswith('fold'):
            if (matches := re.findall(r'fold along (\w+)=(\d+)', l)):
                folds.append((matches[0][0], int(matches[0][1])))
        elif l:
            dots.add(tuple(map(int, l.split(','))))

p1_dots = fold_paper(dots, folds[0:1])
print(f'Part 1 solution: {len(p1_dots)}')

final_dots = fold_paper(dots, folds)
print(f'Part 2 solution:')
print_dots(final_dots)