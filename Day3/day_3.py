import re

with open("input.txt", "r") as file:
    text = file.readlines()

text = "".join(text)

pattern = r"mul\((\d+),(\d+)\)"

matches = re.findall(pattern, text)

total_sum = sum(map(lambda x: int(x[0]) * int(x[1]), matches))
print(f"The total sum is {total_sum}") 


pattern_2 = r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)"

matches = re.finditer(pattern_2, text)

total = 0 
stack = []
for match in matches:
    match = match.group()
    
    if match == "do()":
        can_multiply = True
        continue
    if match == "don't()":
        can_multiply = False
        continue
    
    if can_multiply:
        pattern = r"mul\((\d+),(\d+)\)"
        match = re.search(pattern, match)
        number_1 = int(match.group(1))
        number_2 = int(match.group(2))
        stack.append(number_1 * number_2)

taotal_sum_2 = sum(stack)

print(f"The total sum is {taotal_sum_2}") 
