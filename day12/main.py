from collections import defaultdict, deque


def get_distinct_paths(start_cave, goal_cave, adjacency_map, *, allow_single_double_visit):

    result_paths = []
    visit_count_by_cave = {cave: 0 for cave in adjacency_map.keys()}
    prohibited_double_visits = frozenset([start_cave, goal_cave])
    
    def _dfs(current_path, visited_cave_twice):
        current_cave = current_path[-1]
        
        visit_count_by_cave[current_cave] += 1         
        
        if current_cave == goal_cave:
            result_paths.append(list(current_path))
        else:            
            for neighbor in adjacency_map[current_cave]:
                is_small_cave = neighbor.islower()

                # Need to try visiting it for the first time, as well as the 
                # second time if it's a small cave and not start/end and we
                # haven't already visited another small cave twice
                if not is_small_cave or visit_count_by_cave[neighbor] == 0:
                    current_path.append(neighbor)    
                    
                    _dfs(current_path, visited_cave_twice)
                                      
                    current_path.pop()

                if (allow_single_double_visit and is_small_cave and 
                        visit_count_by_cave[neighbor] == 1 and 
                        not visited_cave_twice and
                        neighbor not in prohibited_double_visits):                    
                    current_path.append(neighbor)    
                    
                    _dfs(current_path, True)
                                      
                    current_path.pop()
        
        visit_count_by_cave[current_cave] -= 1

    _dfs(['start'], False)
    return result_paths


with open('input') as f:
    pairs = [tuple(l.strip().split('-')) for l in f.readlines()]
    adjacency_map = defaultdict(set)
    for pair in pairs:
        adjacency_map[pair[0]].add(pair[1])
        adjacency_map[pair[1]].add(pair[0])

distinct_paths = get_distinct_paths('start', 'end', adjacency_map, allow_single_double_visit=False)
print(f'Part 1: {len(distinct_paths)}')

distinct_paths = get_distinct_paths('start', 'end', adjacency_map, allow_single_double_visit=True)
print(f'Part 2: {len(distinct_paths)}')