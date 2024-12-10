from collections import deque


def file_to_2d_array(file_path):
    array_2d = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            array_2d.append([int(x) if x.isdigit() else -1 for x in line])

    return array_2d

grid = file_to_2d_array("input.txt")
#print(grid)
rows, cols = len(grid), len(grid[0])

def find_starting_points(grid):
    starting_point = []
    for i, x in enumerate(grid):
        for j, y in enumerate(x):
            if grid[i][j] == 0:
                starting_point.append((i,j))
    return starting_point

starting_points = find_starting_points(grid)
#print(starting_points)

def is_valid(r, c, previous_value):
    return 0<= r < rows and 0<= c < cols and grid[r][c] == previous_value + 1

def bfs(start):
    all_paths = list()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    queue = deque([(start, [start])])  # (current position, current path)

    while queue:
        (cur_r, cur_c), path = queue.popleft()
        current_value = grid[cur_r][cur_c]

        # If we reach a cell with 9, record the path
        if current_value == 9:
            all_paths.append(path)
            continue

        # Explore neighbors
        for dr, dc in directions:
            new_r, new_c = cur_r + dr, cur_c + dc
            if is_valid(new_r, new_c, current_value):
                queue.append(((new_r, new_c), path + [(new_r, new_c)]))
    return all_paths

starting_to_paths = {}

def find_unique_last_elements(paths):
    unique_ends = set()
    unique_counts = 0
    for p in paths:
        end = p[-1]
        if not (end in unique_ends):
            unique_ends.add(end)
            unique_counts += 1
    return unique_counts
    
# Perform BFS for each start position
count = 0
score = 0 
trailheads_ratings = 0
for start_pos in starting_points:
    paths = bfs(start_pos)
    starting_to_paths[start_pos] = paths
    if paths:
        score += find_unique_last_elements(paths)
        trailheads_ratings += len(paths)

print(f"Total score is {score}")
print(f"Total raitng for is {trailheads_ratings}")
