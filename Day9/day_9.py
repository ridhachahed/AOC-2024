import copy

def read_file(file_path):
    result = []
    with open(file_path, 'r') as file:
        for line in file:
            for c in line:
                result.append(int(c))
    return result

input_numbers = read_file("input.txt")
#print(input_numbers)

def get_memory_representation(input_numbers):
    result = []
    memory_numbers = [number for i, number in enumerate(input_numbers) if i%2 == 0]
    free_space_numbers = [number for i, number in enumerate(input_numbers) if not(i%2 == 0)]
    for i, (number, memory) in enumerate(zip(memory_numbers, free_space_numbers)):
        result += [i]  * number
        result += ["."] * memory
    if len(memory_numbers) != len(free_space_numbers):
        memory_map = len(memory_numbers) - 1 
        result += [memory_map] * memory_numbers[-1]
    return result, memory_numbers, free_space_numbers

def print_list(memory_representation):
    print("".join(str(m) for m in memory_representation))

memory_representation, memory_numbers, free_space_numbers = get_memory_representation(input_numbers)
#print_list(free_space_numbers)
#print(memory_numbers)

def find_first_occurence(list_, element):
    for i, l in enumerate(list_):
        if l == element:
            return i
    return -1

def reorder_memory_representation(memory_representation):
    result = copy.copy(memory_representation)
    condititon_to_end = lambda l: any(x =="." for x in l)
    while condititon_to_end(result):
        element_to_swap = result.pop()
        index_to_modify = find_first_occurence(result, ".")
        result[index_to_modify] = element_to_swap
    
    return result

#reordered_memory = reorder_memory_representation(memory_representation)
#print_list(reordered_memory)

def compute_check_sum(memory_representation):
    checksum = 0
    for i, x in enumerate(memory_representation):
        checksum +=i *x
    return checksum

#checksum = compute_check_sum(reordered_memory)
#print(f"Checksum is {checksum}")


# input_numbers
# 2333133121414131402
def reorder_memory_representation_by_block(input_numbers, memory_numbers):

    result = [] 
    index = 0 
    look_for_replacement = False
    replacement_budget = 0
    swapped_block = set()
    # index to block_size 
    memory_dict = { i: memory_number for i, memory_number in enumerate(memory_numbers)}

    for i in input_numbers:
        if look_for_replacement:
            replacement_budget = i
            while replacement_budget != 0:
                found_replacement = False
                # look for candidates 
                # if no candidate we break and move on 
                for key in reversed(memory_dict):
                    budget = memory_dict[key]
                    if budget <= replacement_budget:
                        result += [key] * budget
                        replacement_budget -= budget
                        del memory_dict[key]
                        found_replacement = True
                        swapped_block.add(key)
                        break
                if not found_replacement:
                    result += ["."] * replacement_budget    
                    break
            look_for_replacement = False
        else:
            if index in swapped_block:
                result += ["."] * i
            else:
                result += [index] * i
            # update memory dict to consider only free blocks above index
            memory_dict = {k: v for k, v in memory_dict.items() if k > index}
            index += 1
            look_for_replacement = True

    return result

result_blocked = reorder_memory_representation_by_block(input_numbers, memory_numbers)

def compute_check_sum_with_dots(memory_representation):
    checksum = 0
    for i, x in enumerate(memory_representation):
        if x != ".":
            checksum +=i *x
    return checksum

#print_list(result_blocked)

checksum_block = compute_check_sum_with_dots(result_blocked)
print(f"Checksum by block is {checksum_block}")
