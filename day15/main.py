import heapq

from collections import defaultdict



def p1_get_value(grid, x, y):
    return grid[y][x]


def p2_get_value(grid, x, y):
    original_size = len(grid)
    tile_x = x // original_size
    tile_y = y // original_size
    tile_manhattan_dist = tile_x + tile_y
    reference_x = x % original_size
    reference_y = y % original_size
    return ((grid[reference_y][reference_x] + tile_manhattan_dist - 1) % 9) + 1


def get_lowest_total_risk(grid, tile_grid_size, grid_value_func):
    INFINITE = 99999
    size = tile_grid_size * len(grid) - 1
    best_distance = defaultdict(lambda: INFINITE)
    best_distance[0, 0] = 0

    queue = []
    heapq.heapify(queue)
    heapq.heappush(queue, (0, 0, 0))
    visited = set()

    while queue:
        _, x, y = heapq.heappop(queue)
        visited.add((x, y))

        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx <= size and 0 <= ny <= size and (nx, ny) not in visited:
                new_distance = best_distance[x, y] + grid_value_func(grid, nx, ny)
                if new_distance < best_distance[nx, ny]:
                    best_distance[nx, ny] = new_distance
                    heapq.heappush(queue, (new_distance, nx, ny))
    return best_distance[size, size]


with open('input') as f:
    grid = [[int(r) for r in l.strip()] for l in f.readlines()]

print(f'Part 1 solution: {get_lowest_total_risk(grid, 1, grid_value_func=p1_get_value)}')
print(f'Part 2 solution: {get_lowest_total_risk(grid, 5, grid_value_func=p2_get_value)}')