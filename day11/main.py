from functools import lru_cache
from itertools import count


MAX_ENERGY = 9


def neighbors(x, y):
    yield (x - 1, y - 1)
    yield (x, y - 1)
    yield (x + 1, y - 1)
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x - 1, y + 1)
    yield (x, y + 1)
    yield (x + 1, y + 1)


with open('input') as f:
    grid = [[int(c) for c in l.strip()] for l in f.readlines()]
    assert len(grid) == len(grid[0])
    grid_size = len(grid)

total_flash_count = 0
p1_solution = None
p2_solution = None

current_step = 1
while not p1_solution or not p2_solution:
    coordinates_to_flash = set()

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] += 1
            if grid[y][x] > MAX_ENERGY:
                coordinates_to_flash.add((x, y))

    flashed_coords = set()
    while coordinates_to_flash:
        x, y = coordinates_to_flash.pop()
        if (x, y) in flashed_coords:
            continue

        total_flash_count += 1
        for nx, ny in neighbors(x, y):
            if nx < 0 or nx >= grid_size or ny < 0 or ny >= grid_size:
                continue

            grid[ny][nx] += 1
            if grid[ny][nx] > MAX_ENERGY:
                coordinates_to_flash.add((nx, ny))

        flashed_coords.add((x, y))

    for x, y in flashed_coords:
        grid[y][x] = 0

    # Part 1: get the total flash count after step 100
    if current_step == 100:
        p1_solution = total_flash_count

    # Part 2: get the first step number where all octopuses flash
    if len(flashed_coords) == grid_size * grid_size and not p2_solution:
        p2_solution = current_step

    current_step += 1


print(f'Part 1 solution: {p1_solution}')
print(f'Part 2 solution: {p2_solution}')