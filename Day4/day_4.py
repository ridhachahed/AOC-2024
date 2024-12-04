

def file_to_2d_array(file_path):
    with open(file_path, 'r') as file:
        # Read lines, strip the newline character, and convert each line to a list of characters
        array_2d = [list(line.strip()) for line in file]
    return array_2d

input_array = file_to_2d_array("input.txt")


normal_directions = [
        (0, 1),  # Horizontal right
        (0, -1),  # Horizontal left
        (1, 0),  # Vertical down
        (-1, 0),  # Vertical up
        (1, 1),  # Diagonal down-right
        (-1, -1),  # Diagonal up-left
        (1, -1),  # Diagonal down-left
        (-1, 1)  # Diagonal up-right
]

def find_word(grid, word, directions):
    rows, cols = len(grid), len(grid[0])
    word_len = len(word)
    
    def is_valid(x, y):
        """Check if coordinates are within the grid."""
        return 0 <= x < rows and 0 <= y < cols
    
    def search_from(x, y, dx, dy):
        """Search for the word starting at (x, y) in direction (dx, dy)."""
        for i in range(word_len):
            nx, ny = x + i * dx, y + i * dy
            if not is_valid(nx, ny) or grid[nx][ny] != word[i]:
                return False
        return True
    
    found_positions = []  # Store starting positions of found words
    
    # Iterate through each cell in the grid
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == word[0]:  # Potential start of the word
                for dx, dy in directions:
                    if search_from(x, y, dx, dy):
                        found_positions.append(((x, y), (dx, dy)))  # Append start and direction
    
    return found_positions

xmas_occurences = find_word(input_array, 'XMAS', normal_directions)
print(f"There is {len(xmas_occurences)} occurences of XMAS")

mas_word = "MAS"
right_directions = [(1, 1), (-1, -1)]  # either up down-right or up-left
left_dicrections = [(-1, 1), (1, -1)]  # either up right or down left


mas_1 = find_word(input_array, mas_word, right_directions)
mas_2 = find_word(input_array, mas_word, left_dicrections)

# ok new new to find the common As

def find_comom_center(list_1, list_2):
    centers_1 = map(lambda x: (x[0][0] + x[1][0], x[0][1] + x[1][1]), list_1)
    centers_2 = map(lambda x: (x[0][0] + x[1][0], x[0][1] + x[1][1]), list_2)
    common = set(centers_1).intersection(set(centers_2))
    return list(common)

number_of_x = find_comom_center(mas_1, mas_2)
print(f"There is {len(number_of_x)} occurences of X-MAS")
