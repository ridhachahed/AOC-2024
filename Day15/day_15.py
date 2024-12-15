import copy 

def read_input(file_name):
    map_array = []
    instructions = []
    move_to_instructions = False
    with open(file_name) as file:
        for l in file:
            line = [x for x in l.strip()]
            if not line:
                move_to_instructions = True
                continue
            if not move_to_instructions:
                map_array.append(line)
            else:
                instructions += line
    return map_array, instructions

#map_array, instructions = read_input("demo_small.txt")


def find_position(map_array):
    for i, r in enumerate(map_array):
        for j, col in enumerate(r):
            if col == "@":
                return (i, j)
            

def move(map_array, current_position, instruction):
    intended_move = None
    move_successful = False
    if instruction == "^": # go up 
        intended_move = (-1, 0)
    elif instruction == ">": # go right
        intended_move = (0 , 1)
    elif instruction == "v": # go down
        intended_move = (1, 0)
    elif instruction == "<": # go left
        intended_move = (0, -1) 
    else:
        raise ValueError(f"Unknown orientation {instruction}")
    
    new_r = current_position[0] + intended_move[0]
    new_c = current_position[1] + intended_move[1]
    next_position = (new_r, new_c)

    next_symbol = map_array[new_r][new_c]
    #print(next_symbol)
    # not next the well 
    if next_symbol!= "#":
        # found a box need to move it
        if next_symbol == "O":
            next_move_successful, _ = move(map_array, next_position, instruction)
            # if boxe moved next to move mine now
            if next_move_successful:
                advance(map_array, current_position, next_position)
                move_successful = True
        # move directly
        else:
            advance(map_array, current_position, next_position)
            move_successful = True
    return move_successful, next_position
    

def advance(map_array, current_position, next_position):
    tmp = map_array[next_position[0]][next_position[1]]
    map_array[next_position[0]][next_position[1]] = map_array[current_position[0]][current_position[1]]
    map_array[current_position[0]][current_position[1]] = tmp



def simulate(map_array):
    map_array = copy.deepcopy(map_array)
    initial_position = find_position(map_array)
    position = initial_position
    for instruction in instructions:
        #print(instruction)
        move_successful, next_position = move(map_array, position, instruction)
        if move_successful:
            position = next_position
        #print_pretty(map_array)
    return map_array


def print_pretty(map_array):
    for l in map_array:
        print("".join(l))

#final_map = simulate(map_array)
#print_pretty(final_map)


def compute_gps_coordinate(map_array):
    total_sum = 0
    for i, r in enumerate(map_array):
        for j, col in enumerate(r):
            if col == "O":
                total_sum += i * 100 + j 

    return total_sum

#total_sum_gps = compute_gps_coordinate(final_map)
#print(f"total sum is {total_sum_gps}")



# Part 2 

map_array, instructions = read_input("input.txt")


def move_bigger(map_array, current_position, instruction, move_companion_also=True):
    intended_move = None
    move_successful = False
    companion_moved = True
    next_move_successful = False
    if instruction == "^": # go up 
        intended_move = (-1, 0)
    elif instruction == ">": # go right
        intended_move = (0 , 1)
    elif instruction == "v": # go down
        intended_move = (1, 0)
    elif instruction == "<": # go left
        intended_move = (0, -1) 
    else:
        raise ValueError(f"Unknown orientation {instruction}")
    
    current_symbol = map_array[current_position[0]][current_position[1]]
    new_r = current_position[0] + intended_move[0]
    new_c = current_position[1] + intended_move[1]
    next_position = (new_r, new_c)

    next_symbol = map_array[new_r][new_c]
    
    #print(next_symbol)
    # not next the well 
    if next_symbol!= "#":
        # print(f"test {next_symbol}")
        # found a box need to move it

        if next_symbol in ["[", "]"]:
            #print_pretty(map_array)
            #print(f"instruction is{instruction}")
            #print(f"Next symbol is {next_symbol}")
            saved_map_before_box_is_moved = copy.deepcopy(map_array)
            if move_companion_also:
                companion_coordinate = find_companion_coordinate(next_symbol, next_position)
                companion_to_move = map_array[companion_coordinate[0]][companion_coordinate[1]]
                #print(f"Companion to move is {companion_to_move}")
                # try to move the companion box 
                #print("moving companion")
                companion_moved, _ = move_bigger(map_array, companion_coordinate, instruction)
                if companion_moved :
                    next_move_successful, _ = move_bigger(map_array, next_position, instruction)
            else:
                next_move_successful, _ = move_bigger(map_array, next_position, instruction)
            if companion_moved and next_move_successful:
                #print("advancing")
                advance(map_array, current_position, next_position)
                move_successful = True
            else:
                #print("Can't move")
                # We move nothing and we get back old map before move
                map_array = saved_map_before_box_is_moved
                move_successful = False
        # move directly
        else:
            advance(map_array, current_position, next_position)
            move_successful = True
    return move_successful, next_position


def find_companion_coordinate(symbol, symbol_coordinate):
    if symbol == "[":
        direction_to_check = (0, 1)
    elif symbol == "]":
        direction_to_check = (0, -1)

    companion_coordinate_r = symbol_coordinate[0] + direction_to_check[0]
    companion_coordinate_c = symbol_coordinate[1] + direction_to_check[1]

    return (companion_coordinate_r, companion_coordinate_c)


def companion(symbol):
    if symbol == "[":
        return "]"
    elif symbol == "]":
       return  "["
    else:
        return ""

def resise_map(initial_map):
    # twice as wide 
    new_columns = []
    for c in zip(*initial_map):
        new_columns += [c, c]
    new_map= [list(row) for row in zip(*new_columns)]

    # remove double @
    robot_position = find_position(new_map) 
    double_position_r = robot_position[0]
    double_position_c = robot_position[1] + 1
    new_map[double_position_r][double_position_c] = "."

    # replace box with double box 
    for i, row in enumerate(new_map):
        for j, col in enumerate(row):
            if col == "O":
                new_map[i][j] = "["
                new_map[i][j+1] = "]"
    return new_map


def simulate_part2(map_array):
    map_array = copy.deepcopy(map_array)
    initial_position = find_position(map_array)
    position = initial_position
    for instruction in instructions:
        intial_map = copy.deepcopy(map_array)
        changing_map = copy.deepcopy(intial_map)
        move_successful, next_position = move_bigger(changing_map, position, instruction)
        if move_successful:
            position = next_position
            map_array = changing_map
        else:
            map_array = intial_map
    return map_array

#print_pretty(map_array)
resized_map = resise_map(map_array)
#print_pretty(resized_map)

#resized_map, instructions = read_input("hard_example.txt")
#initial_position = find_position(resized_map)
#move_successful, next_position = move_bigger(resized_map, initial_position, "^")

#print_pretty(resized_map)

final_resized_map = simulate_part2(resized_map)
#print_pretty(final_resized_map)

def compute_gps_coordinate_bigger(map_array):
    total_sum = 0
    for i, r in enumerate(map_array):
        for j, col in enumerate(r):
            if col == "[":
                total_sum += i * 100 + j 

    return total_sum

total_sum_part2 = compute_gps_coordinate_bigger(final_resized_map)
print(f"Final size is {total_sum_part2}")

