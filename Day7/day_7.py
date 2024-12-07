


def parse_input(file_path):
    total_list = []
    numbers_list = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.split(":")
            total_list.append(int(line[0]))
            numbers = [int(n) for n in line[1].strip().split()]
            numbers_list.append(numbers)
    
    return total_list, numbers_list


total_list, numbers_list = parse_input('input.txt')

# given a list of numbers and a total return if path exists
def validate_sum(numbers, total):
    def helper(current_sum, index):
        if index == len(numbers):
            return current_sum == total
        else:
            if current_sum <= total:
                next_item = numbers[index]

                return helper(current_sum + next_item, index + 1) or helper(current_sum * next_item, index + 1)

    found_nice_total = helper(numbers[0],1)

    return found_nice_total

def generate_sum_of_valid(numbers_list, total_list, function_to_validate):
    total_sum = 0
    for numbers, total in zip(numbers_list, total_list):
        if function_to_validate(numbers, total):
            total_sum += total
    return total_sum

total_sum=generate_sum_of_valid(numbers_list, total_list, validate_sum)

print(f"Total sum of valid sums is {total_sum}")



def validate_sum_with_concatenation(numbers, total):
    def helper(current_sum, index):
        if index == len(numbers):
            return current_sum == total
        else:
            if current_sum <= total:
                next_item = numbers[index]
                concatenated_sum = int(str(current_sum) + str(next_item))
                return helper(current_sum + next_item, index + 1) \
                    or helper(current_sum * next_item, index + 1) \
                    or helper(concatenated_sum, index + 1)

    found_nice_total = helper(numbers[0],1)

    return found_nice_total


total_sum_with_concatenated=generate_sum_of_valid(numbers_list, total_list, validate_sum_with_concatenation)

print(f"Total sum of valid sums with concatenation is {total_sum_with_concatenated}")
