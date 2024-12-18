import copy
import heapq

# for demo 6 and for input 70
map_size = 6 + 1

def read_input(file_name):
    bytes_coordinates = []
    with open(file_name) as file:
        for line in file: 
            numbers = line.strip().split(",")
            bytes_coordinates.append((int(numbers[0]), int(numbers[1])))
    return bytes_coordinates


def create_empty_map(map_size):
    new_map = []
    for i in range(map_size):
        new_map.append(["." for j in range(map_size)])
    return new_map


def simulate_memory_corruption(current_map, bytes_coordinates, step_start=0, step_stop=-1):
    current_map = copy.deepcopy(current_map)
    bytes_to_consider = bytes_coordinates[step_start:step_stop]
    for (x,y) in bytes_to_consider:
        # x distance to left edge
        # y distance to top edge

        current_map[y][x] = "#"
    return current_map

def print_pretty(map_array):
    for l in map_array:
        print("".join(l))
        

def get_directions():
    directions = {"UP": (-1,0),
                  "DOWN": (1, 0),
                  "LEFT": (0, -1),
                  "RIGHT": (0, 1)}
    return directions

def heursitic(a,b):
    x_a, y_a = a[0], a[1]
    x_b, y_b = b[0], b[1]
    distance = abs(x_a - x_b) + abs(y_a - y_b)
    return distance 

def a_start_search(maze):

    rows, cols = len(maze), len(maze[0])

    def is_valid(x, y):
        in_bound = 0 <= x < rows and 0<= y < cols
        if in_bound:
            return maze[x][y] != "#"
        else:
            return False

    start_coord = (0,0)
    end_coord = (len(maze)-1, len(maze[0])-1)
    #print(f"Start coordinate is {start_coord}")
    #print(f"End coordinate is {end_coord}")
    
    # total_cost = current_cost + heuristic_cost 
    # (total_cost, current_cost, x, y, current_direction )
    pq = []

    heapq.heappush(pq, (0, 0, start_coord[0], start_coord[1], "RIGHT"))
    visited_nodes = set()  

    while pq:
        total_cost, current_actual_cost, x, y, current_dir = heapq.heappop(pq)

        if (x,y, current_dir) in visited_nodes:
            continue
        visited_nodes.add((x, y, current_dir))
    
        if (x,y) == end_coord:
            return total_cost
        
        for new_direction, (dx, dy) in get_directions().items():
            #print(pq)
            nx, ny = x + dx, y + dy
            
            if not is_valid(nx, ny):
                continue
            
            # actual_cost = current_cost + move_cost
            # total_cost = actual_cost + heursitic 
            move_cost = 1
            if new_direction!= current_dir: 
                # turn cost 
                move_cost += 0
            
            new_actual_cost = current_actual_cost + move_cost
            new_total_cost = new_actual_cost + heursitic((nx, ny), end_coord)
            
            heapq.heappush(pq, (new_total_cost, new_actual_cost, nx, ny, new_direction))
        
    return float('inf')

# for demo 6 and for input 70
map_size = 6 + 1

bytes_coordinates = read_input("demo.txt")
empty_map = create_empty_map(map_size)

step_to_consider = 1024
corrupted_map = simulate_memory_corruption(empty_map, bytes_coordinates, step_start=0, step_stop=step_to_consider)
#print_pretty(corrupted_map)

final_score = a_start_search(corrupted_map)
print(final_score)

def simulate_exit(empty_map, bytes_coordinates):
    for step_to_consider in range(1024, len(bytes_coordinates)):
        corrupted_map = simulate_memory_corruption(empty_map, bytes_coordinates, step_start=0, step_stop=step_to_consider)
        blocked = bytes_coordinates[0:step_to_consider][-1]
        final_score = a_start_search(corrupted_map)
        if final_score != float('inf'):
            print(f"Exit found for {step_to_consider}")
        else:
            print(f"Exit not found for {step_to_consider} with byte {blocked}")
            return blocked
    return None

map_size = 70 + 1

bytes_coordinates = read_input("input.txt")
empty_map = create_empty_map(map_size)

blocking_byte = simulate_exit(empty_map, bytes_coordinates)
print(f"The final bytes where the exit is blocked is {blocking_byte}")