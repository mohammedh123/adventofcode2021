from collections import deque
from functools import reduce


def get_basin_size(grid, x, y):
    # aka floodfill
    seen = set()
    queue = deque([(x, y)])
    size = 0
    while queue:
        x, y = queue.popleft()

        if (x, y) in seen or grid[y][x] == 9:
            continue

        size += 1
        seen.add((x, y))

        if x - 1 >= 0: queue.append((x - 1, y))
        if y - 1 >= 0: queue.append((x, y - 1))
        if x + 1 < len(grid[y]): queue.append((x + 1, y))
        if y + 1 < len(grid): queue.append((x, y + 1))

    return size


with open('input') as f:
    grid = [[int(c) for c in line.strip()] for line in f.readlines()]

low_points = []
for y in range(len(grid)):
    for x in range(len(grid[0])):
        current = grid[y][x]

        if x - 1 >= 0 and current >= grid[y][x - 1]: continue
        if x + 1 < len(grid[0]) and current >= grid[y][x + 1]: continue
        if y - 1 >= 0 and current >= grid[y - 1][x]: continue
        if y + 1 < len(grid) and current >= grid[y + 1][x]: continue
        low_points.append((current, (x, y)))

print(f'Part 1 solution: {sum(1 + n for n, _ in low_points)}')

largest_basins = sorted(get_basin_size(grid, x, y) for _, (x, y) in low_points)
print(f'Part 2 solution: {reduce(lambda a, b: a * b, largest_basins[-3::])}')