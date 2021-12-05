from collections import defaultdict


def linear_interpolation(x1, y1, x2, y2):
    # Assumes the pairs of coordinates make a straight or diagonal line
    dx, dy = 0, 0

    if x2 > x1: 
        dx = 1
    elif x1 > x2:
        dx = -1

    if y2 > y1:
        dy = 1
    elif y1 > y2:
        dy = -1
    
    cx, cy = x1, y1
    while True:
        yield (cx, cy)
        
        if (cx, cy) == (x2, y2):
            break
        
        cx += dx
        cy += dy


with open('input') as f:
    pairs = [tuple(tuple(map(int, s.split(','))) for s in l.split(' -> ')) for l in f.readlines()]

grid = defaultdict(int)
for (x1, y1), (x2, y2) in pairs:
    if abs(y2 - y1) == abs(x2 - x1):  # Ignore diagonals
        continue

    for x, y in linear_interpolation(x1, y1, x2, y2):
        grid[(x, y)] += 1

overlap_total = sum(1 for (x, y) in grid if grid[(x, y)] > 1)
print(f'Part 1 solution: {overlap_total}')

grid = defaultdict(int)
for (x1, y1), (x2, y2) in pairs:
    for x, y in linear_interpolation(x1, y1, x2, y2):
        grid[(x, y)] += 1

overlap_total = sum(1 for (x, y) in grid if grid[(x, y)] > 1)
print(f'Part 2 solution: {overlap_total}')