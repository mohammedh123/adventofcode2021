with open('input') as f:
    lines = [l.strip() for l in f.readlines()]

depth = 0
x_pos = 0
for l in lines:
    dir, num_units = l.split(' ')
    num_units = int(num_units)
    
    if dir == 'forward':
        x_pos += num_units
    elif dir == 'down':
        depth += num_units
    elif dir == 'up':
        depth -= num_units

print(f'Part 1 solution: {depth * x_pos}')

depth = 0
x_pos = 0
aim = 0
for l in lines:
    dir, num_units = l.split(' ')
    num_units = int(num_units)
    
    if dir == 'forward':
        x_pos += num_units
        depth += aim * num_units
    elif dir == 'down':
        aim += num_units
    elif dir == 'up':
        aim  -= num_units

print(f'Part 2 solution: {depth * x_pos}')