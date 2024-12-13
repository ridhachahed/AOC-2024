from functools import cache

def read_file(file_path):
    result = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip().split()
            result += line
    return result

input_ = read_file("input.txt")

def remmove_left_zeros(number):
    digits = [digit for digit in number]
    index_to_keep = 0
    while digits[index_to_keep] == "0" and index_to_keep < len(digits) - 1 and len(digits) != 1:
        index_to_keep += 1
    new_digits = digits[index_to_keep:]
    return "".join(new_digits)

def split(number):
    results = []
    digits = [digit for digit in number]
    if all(map(lambda x: x == "0", digits)):
        results.append("1")
    elif len(digits) % 2 == 0:
        middle_index = len(digits) // 2
        left_part = remmove_left_zeros(digits[:middle_index])
        right_part = remmove_left_zeros(digits[middle_index:])
        results += [left_part, right_part]
    else:
        new_number = str(int(number) * 2024)
        results.append(new_number)
    return results

def blink(line, nbr_step):
    result = line
    new_line = []
    for i in range(nbr_step):
        for number in result:
            new_line += split(number)
        result = new_line
        #print(result)
        new_line = []
    return result

new_stones = blink(input_, 10)
print(f"We have {len(new_stones)} stones")


memory = {}

def split_with_memoization(number, step):
    digits = [digit for digit in number]
    key  = (number, step) 
    if step == 0: 
        return 1
    elif key in memory:
        return memory[key]
    elif all(map(lambda x: x == "0", digits)):
        memory[key] = split_with_memoization("1",  step - 1 )
    elif len(digits) % 2 == 0:
        middle_index = len(digits) // 2
        left_part = remmove_left_zeros(digits[:middle_index])
        right_part = remmove_left_zeros(digits[middle_index:])
        memory[key] = split_with_memoization(left_part, step - 1) + split_with_memoization(right_part, step - 1)
    else:
        new_number = str(int(number) * 2024)
        memory[key] =  split_with_memoization(new_number, step - 1)
    return memory[key]


def blink_smartly(line, nbr_step):
    result = 0
    for number in line: 
        answer = split_with_memoization(number, nbr_step)
        result += answer
        print(f"Number {number} done")
    return result
#print(split_with_memoization("8791", 4))

new_stones_part2 = blink_smartly(input_, 75)
print(f"We have {new_stones_part2} stones")




