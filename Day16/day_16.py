
import heapq 

def read_input(file_name):
    result = []
    with open(file_name) as file:
        for l in file:
            line = [c for c in l.strip()]
            result.append(line)
    return result

def print_pretty(map_array):
    for l in map_array:
        print("".join(l))

maze = read_input("input.txt")
#print_pretty(maze)
        
        
def parse_maze(maze):
    start_coord = end_coord = None
    for i, r in enumerate(maze):
        for j, col in enumerate(r):
            if col == 'S':
                start_coord = (i, j)
            elif col == 'E':
                end_coord = (i, j)
    return start_coord, end_coord

COST_TURN = 1000

def heursitic(a,b):
    x_a, y_a = a[0], a[1]
    x_b, y_b = b[0], b[1]
    distance = abs(x_a - x_b) + abs(y_a - y_b)
    return distance 

def get_directions():
    directions = {"UP": (-1,0),
                  "DOWN": (1, 0),
                  "LEFT": (0, -1),
                  "RIGHT": (0, 1)}
    return directions

def a_start_search(maze):

    rows, cols = len(maze), len(maze[0])

    def is_valid(x, y):
        in_bound = 0 <= x < rows and 0<= y < cols
        if in_bound:
            return maze[x][y] != "#"
        else:
            return False

    start_coord, end_coord = parse_maze(maze)
    print(f"Start coordinate is {start_coord}")
    print(f"End coordinate is {end_coord}")
    
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
                move_cost += COST_TURN
            
            new_actual_cost = current_actual_cost + move_cost
            new_total_cost = new_actual_cost + heursitic((nx, ny), end_coord)
            
            heapq.heappush(pq, (new_total_cost, new_actual_cost, nx, ny, new_direction))
        
    return float('inf')

final_score = a_start_search(maze)
print(f"the final score is {final_score}")

# Part 2 
def a_start_search_all_optimal_paths(maze, known_minimum_score):

    rows, cols = len(maze), len(maze[0])

    def is_valid(x, y):
        in_bound = 0 <= x < rows and 0<= y < cols
        if in_bound:
            return maze[x][y] != "#"
        else:
            return False

    start_coord, end_coord = parse_maze(maze)

    # total_cost = current_cost + heuristic_cost 
    # (total_cost, current_cost, x, y, current_direction )
    pq = []

    heapq.heappush(pq, (0, 0, start_coord[0], start_coord[1], "RIGHT", [start_coord]))
    visited_nodes = dict()
    best_paths = [] 
    
    while pq:
        #print(pq)
        total_cost, current_actual_cost, x, y, current_dir, current_path = heapq.heappop(pq)
        if (x,y) == end_coord:
            #print("end reached")
            if total_cost == known_minimum_score:
                best_paths.append(current_path)
                
        # Key improvment is here I accept already visisted nodes if they are visited with the correct budget :) 
        key = (x,y, current_dir)
        if key in visited_nodes and (x,y) != end_coord:
            if visited_nodes[key] < current_actual_cost:
                continue
            else:
                visited_nodes[key] = current_actual_cost   
        else:
            visited_nodes[key] = current_actual_cost

        for new_direction, (dx, dy) in get_directions().items():
            nx, ny = x + dx, y + dy
            
            if not is_valid(nx, ny):
                continue
            
            # actual_cost = current_cost + move_cost
            # total_cost = actual_cost + heursitic 
            move_cost = 1
            if new_direction!= current_dir: 
                # turn cost 
                move_cost += COST_TURN
            
            new_actual_cost = current_actual_cost + move_cost
            new_total_cost = new_actual_cost + heursitic((nx, ny), end_coord)
            
            if new_actual_cost <= known_minimum_score:
                heapq.heappush(pq, (new_total_cost, new_actual_cost, nx, ny, new_direction, current_path + [(nx, ny)]))
        
    return best_paths


paths = a_start_search_all_optimal_paths(maze, final_score)
optimal_nodes = set ()
for p in paths:
    for node in p:
        optimal_nodes.add(node)
print(f"Number of optimal seats is {len(optimal_nodes)}")