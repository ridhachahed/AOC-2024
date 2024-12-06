import copy
from collections import defaultdict

def file_to_2d_array(file_path):
    with open(file_path, 'r') as file:
        array_2d = [list(line.strip()) for line in file]
    return array_2d


map_array = file_to_2d_array("input.txt")
map_array_initial = copy.deepcopy(map_array)

def find_position(map_array, character):
    saved_index = []
    for i, row in enumerate(map_array):
        for j, column in enumerate(row):
            if column == character:
                saved_index.append((i,j))
    return saved_index

starting_index = find_position(map_array, "^")[0]
obstacles_index = find_position(map_array, "#")


def turn(current_orientation):
    if current_orientation == "^":
        return ">"
    elif current_orientation == ">":
        return "v"
    elif current_orientation == "v":
        return "<"
    elif current_orientation == "<":
        return "^"
    else:
        raise ValueError(f"Unknown orientation {current_orientation}")

def advance(current_orientation):
    if current_orientation == "^":
        return (-1, 0) # Move up 
    elif current_orientation == ">":
        return (0, 1) # Move right
    elif current_orientation == "v":
        return (1, 0) # Move down
    elif current_orientation == "<":
        return (0, -1) # Move left
    else:
        raise ValueError(f"Unknown orientation {current_orientation}")


def detect_cycle(path_visited, position, orientation):
    path_visited.get(position)
    
    return 
    
def navigate(map_array, starting_index):
    
    rows, cols = len(map_array), len(map_array[0])
    
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols
    
    # try to advance forward 
    current_position = starting_index
    current_orientation = map_array[current_position[0]][current_position[1]]
    map_array[current_position[0]][current_position[1]] = "X"
    path_visited = defaultdict(set) # dict of node() : set(directions ^)
    
    while True:
        try:
            dx, dy = advance(current_orientation)
        except:
            return map_array, path_visited, True

        new_position =  (current_position[0] + dx, current_position[1] + dy)

        if is_valid(new_position[0], new_position[1]):

            # Check for cycles
            visited_orientation = path_visited[new_position]
            if current_orientation in visited_orientation:
                return map_array, path_visited, True
        
            if current_position != starting_index: 
                path_visited[current_position].add(current_orientation)

            next_location = map_array[new_position[0]][new_position[1]]

            # there is an obstacle need to turn...
            if next_location == "#":
                current_orientation = turn(current_orientation)
                continue
            else:
                current_position = new_position
                map_array[current_position[0]][current_position[1]] = "X"
        else:
            # the gard is out
            break
    
    return map_array, path_visited, False

navigation, node_visited, loop_detected = navigate(map_array, starting_index)

def count_navigation(navigation):
    counter = 0
    for row in navigation:
        for column in row:
            if column == "X":
                counter += 1
    return counter

with open("output.txt", "w") as file:
    for row in navigation:
        file.write(" ".join(map(str, row)) + "\n")

total_navigation = count_navigation(navigation)
print(f"The total number of distinct positions is {total_navigation}")


# part 2 
def simulate_block(map_array, node):
    map_array_to_use = copy.deepcopy(map_array)
    map_array_to_use[node[0]][node[1]] = "#"
    navigation, node_visited, loop_detected = navigate(map_array_to_use, starting_index)
    ##if loop_detected:
        ##print(node)
    return loop_detected
    

def find_loop(map_array):
    loop_counter = 0
    print(f"Checking blocking {len(node_visited)} nodes")
    for node in node_visited.keys():
        map_array_to_use = copy.deepcopy(map_array)
        # try to n the visited node
        if simulate_block(map_array_to_use, node):
            loop_counter += 1
    return loop_counter

print("Simulate a block")
print(simulate_block(map_array_initial, (8,3)))
loop_counter = find_loop(map_array_initial)
print(f"Total number of loop is {loop_counter}")
