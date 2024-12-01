
list_1 = []
list_2 = []
with open("input.txt", "r") as file:
    for line in file:
        line = line.strip().split()
        list_1.append(int(line[0]))
        list_2.append(int(line[1]))

sorted_list_1 = sorted(list_1)
sorted_list_2 = sorted(list_2)

total_distance = sum(abs(x[0] - x[1]) for x in zip(sorted_list_1, sorted_list_2))

print(f"The total distance is {total_distance}")

list_2_counter = {}

for i in list_2:
    old_count = list_2_counter.get(i, 0) 
    list_2_counter[i] = old_count + 1 

similarity_score = 0

for i in list_1:
    similarity_score += i * list_2_counter.get(i,0)

print(f"The total similarity score is {similarity_score}")
    