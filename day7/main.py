def calculate_total_fuel_cost_p1(initial_positions, destination):
    # The number distance from initial N to destination X is delta D
    # D = abs(N - X)
    # The cost in fuel is equivalent to:
    # D
    return sum(abs(n - destination) for n in initial_positions)


def calculate_total_fuel_cost_p2(initial_positions, destination):
    # The number distance from initial N to destination X is delta D
    # D = abs(N - X)
    # The cost in fuel is equivalent to:
    # (D^2 + D) / 2
    return sum(((n - destination)**2 + abs(n - destination)) // 2 for n in initial_positions)


def solution(initial_positions, total_fuel_cost_func):
    minimum_fuel = None
    previous = total_fuel_cost_func(initial_positions, 0)  # Move to 0
    for l in range(1, max(initial_positions) + 1):
        current = total_fuel_cost_func(initial_positions, l)
        if current > previous:
            break
        previous = current

    return previous


with open('input') as f:
    initial_positions = [int(n) for n in f.readline().split(',')]

print(f'Part 1 solution: {solution(initial_positions, calculate_total_fuel_cost_p1)}')
print(f'Part 2 solution: {solution(initial_positions, calculate_total_fuel_cost_p2)}')