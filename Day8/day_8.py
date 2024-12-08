
import re 
import copy
from collections import defaultdict

def file_to_2d_array(file_path):
    with open(file_path, 'r') as file:
        array_2d = [list(line.strip()) for line in file]
    return array_2d


file_path = "input.txt"
grid = file_to_2d_array(file_path)

#print(grid)

rows = len(grid)
print(rows)
columns = len(grid[0])
print(columns)

def is_valid(x, y):
    return 0 <= x < rows and 0<= y < columns


def detect_antennas(grid):
    antennas_dict = defaultdict(list)
    pattern = r'^[a-zA-Z0-9]$'

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if re.match(pattern, col):
                antennas_dict[col].append((i,j))
    return antennas_dict

antennas_dict = detect_antennas(grid)
#print(antennas_dict)


def add_antinodes(point_a, point_b):
    x_a, y_a = point_a
    x_b, y_b = point_b

    x_diff = x_b - x_a
    y_diff = y_b - y_a
    
    # check in the grid 
    anti_nodes = []
    candidate_1 = (x_b + x_diff, y_b + y_diff)
    candidate_2 = (x_a - x_diff, y_a - y_diff)
    if is_valid(*candidate_1):
        anti_nodes.append(candidate_1)
    if is_valid(*candidate_2):
        anti_nodes.append(candidate_2)
    return anti_nodes

point_a = (5, 6)
point_b = (8, 8)
print(add_antinodes(point_a, point_b))

def compute_antinodes(grid, antenna_dict, antinode_function):
    grid_output = copy.copy(grid)
    antinodes_list = set()
    for antenna in antenna_dict:
        points = antenna_dict[antenna]
        if len(points) > 1:
            for point_a in points[0:-1]:
                for point_b in points[1:]:
                    if point_a != point_b:
                        antinodes = antinode_function(point_a, point_b)
                        # print(f"Point a=({point_a}) and b=({point_b}) give antinodes : {antinodes}")
                        antinodes_list.update(antinodes)
                    for p in antinodes:
                        if grid[p[0]][p[1]] == ".":
                            grid_output[p[0]][p[1]] = "#"
    return antinodes_list, grid_output

def write_output(fn, grid_output):
    with open(fn, "w") as file:
        for row in grid_output:
            file.write(" ".join(map(str, row)) + "\n")


antinodes_list, grid_output = compute_antinodes(grid, antennas_dict, add_antinodes)
print(antinodes_list)

print(f"There are {len(antinodes_list)} antinodes")      
write_output("output_part1.txt", grid_output)

def add_harmonic_antinodes(point_a, point_b):
    x_a, y_a = point_a
    x_b, y_b = point_b

    x_diff = x_b - x_a
    y_diff = y_b - y_a
    
    # check in the grid 
    anti_nodes = [point_a, point_b]
    candidate_1 = (x_b + x_diff, y_b + y_diff)
    candidate_2 = (x_a - x_diff, y_a - y_diff)
    while is_valid(*candidate_1):
        anti_nodes.append(candidate_1)
        candidate_1 = (candidate_1[0] + x_diff, candidate_1[1] + y_diff)
    while is_valid(*candidate_2):
        anti_nodes.append(candidate_2)
        candidate_2 = (candidate_2[0] - x_diff, candidate_2[1] - y_diff)
    return anti_nodes


antinodes_list_harmonic, grid_output_harmonic = compute_antinodes(grid, antennas_dict, add_harmonic_antinodes)
#print(antinodes_list_harmonic)

print(f"There are {len(antinodes_list_harmonic)} harmonic antinodes")
write_output("output_part2.txt", grid_output_harmonic)

