import itertools
import math


with open('input') as f:
    ranges = f.readline().strip()[13:].split(', ')
    x_range = [int(x) for x in ranges[0][2:].split('..')]
    x_min, x_max = min(x_range), max(x_range)
    y_range = [int(y) for y in ranges[1][2:].split('..')]
    y_min, y_max = min(y_range), max(y_range)

global_highest_y = -9999999
starting_pos = set()
for dx in range(1, x_max + 1):
    max_possible_x_dist = dx * (dx + 1) / 2
    if max_possible_x_dist < x_min:
        continue
        
    # Find the number of steps it takes to at least get to the box
    min_steps_to_box = 0
    x = 0
    while x < x_min:
        x += dx - min_steps_to_box
        min_steps_to_box += 1

    # If the minimum number of steps causes them to overshoot, then it
    # cannot possibly ever land in the box, no matter what dy we choose
    if x > x_max:
        continue
        
    n = min_steps_to_box
    dy_min = math.ceil((y_min + n*(n-1)/2)/n)
    for dy in range(dy_min, 150):
        x = 0
        y = 0
        ys = set([0])
        
        finished = True
        for n in itertools.count(0):
            ddx = max(dx - n, 0)
            ddy = dy - n
            x += ddx
            y += ddy
            ys.add(y)
            if x_min <= x <= x_max and y_min <= y <= y_max:
                global_highest_y = max(global_highest_y, max(ys))
                starting_pos.add((dx, dy))
            
            if y < y_min and ddy < 0:  # Falling and below the minimum
                break

print(f'Part 1 solution: {global_highest_y}')
print(f'Part 2 solution: {len(starting_pos)}')