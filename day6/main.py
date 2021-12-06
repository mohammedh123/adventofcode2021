from collections import defaultdict, deque

RESPAWN_TIMER = 7
SPAWN_DELAY = 2


def simulate_life(initial_timers, num_days):
    fish_timers = deque([0] * (RESPAWN_TIMER + SPAWN_DELAY))
    for n in initial_timers:
        fish_timers[n] += 1

    for current_day in range(num_days):
        fish_timers.rotate(-1)

        # Each fish that went through its lifecycle
        # (initially found at fish_timers[0], now at fish_timers[-1])
        # spawns another fish with a lifecycle of respawn timer + delay
        # (handled by the rotation)
        # and has its own lifecycle back at the respawn timer, so update
        # the corresponding index with the new additions
        fish_timers[RESPAWN_TIMER - 1] += fish_timers[-1]

    return fish_timers


with open('input') as f:
    initial_timers = [int(n) for n in f.readline().split(',')]

print(f'Part 1 solution: {sum(simulate_life(initial_timers, 80))}')
print(f'Part 2 solution: {sum(simulate_life(initial_timers, 256))}')
