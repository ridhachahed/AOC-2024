
def read_file(file_name):
    towels_available = []
    towels_desired = []
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            if line:
                if "," in line:
                    line = line.split(",")
                    towels_available += [c.strip() for c in line]
                else:
                    towels_desired.append(line)
    return towels_available, towels_desired

towels_available, towels_desired = read_file("input.txt")
towels_available_set = set(towels_available)

def find_maximum_pattern(towels_available):
    maximum_towel_size = 0 
    for towel in towels_available:
        length_ = len(towel)
        if length_ > maximum_towel_size:
            maximum_towel_size = length_
    return maximum_towel_size

maximum_towel_size = find_maximum_pattern(towels_available)

def recursive_towels(towels_available_set, towel_desired, maximum_towel_size, memory):
    if len(towel_desired) == 0:
        return True
    elif towel_desired in memory:
        return memory[towel_desired]
    else:
        element_to_check = min(maximum_towel_size, len(towel_desired))
        for i in range(1, element_to_check + 1):
            element = towel_desired[:i]
            element_string = "".join(element)
            if element_string in towels_available_set:
                recursive_call = recursive_towels(towels_available_set, towel_desired[i:], maximum_towel_size, memory)
                memory[towel_desired] = recursive_call
                if recursive_call:
                    return recursive_call
        return False

# Example
#result = recursive_towels(towels_available_set, towels_desired[4], maximum_towel_size, {})
#print(result)

def general(towels_available_set, towels_desired, maximum_towel_size):
    result = 0
    for towel_desired in towels_desired:
        memory = {}
        towel_result = recursive_towels(towels_available_set, towel_desired, maximum_towel_size, memory)
        if towel_result:
            result += 1
    return result

available_towel_result = general(towels_available_set, towels_desired, maximum_towel_size)
print(available_towel_result)


# Part2
def recursive_towels_counter(towels_available_set, towel_desired, maximum_towel_size, memory):
    if len(towel_desired) == 0:
        return 1
    elif towel_desired in memory:
        return memory[towel_desired]
    else:
        element_to_check = min(maximum_towel_size, len(towel_desired))
        total_ways = 0
        for i in range(1, element_to_check + 1):
            element = towel_desired[:i]
            element_string = "".join(element)
            if element_string in towels_available_set:
                recursive_call = recursive_towels_counter(towels_available_set, towel_desired[i:], maximum_towel_size, memory)
                total_ways += recursive_call

        memory[towel_desired] = total_ways
        return total_ways
    
def general_counter(towels_available_set, towels_desired, maximum_towel_size):
    result = 0
    for towel_desired in towels_desired:
        memory = {}
        towel_result = recursive_towels_counter(towels_available_set, towel_desired, maximum_towel_size, memory)
        result += towel_result
    return result

#memory_example = {}
#counter = recursive_towels_counter(towels_available_set, towels_desired[2], maximum_towel_size, memory_example)
#print(memory_example)
#print(counter)

available_towel_counter_result = general_counter(towels_available_set, towels_desired, maximum_towel_size)
print(available_towel_counter_result)