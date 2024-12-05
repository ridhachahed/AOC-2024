from collections import defaultdict, deque

ordering = []
updates = []

with open("input.txt", "r") as file:
    for line in file:
        line = line.strip()
        if '|' in line:
            line = line.split('|')
            ordering.append((int(line[0]), int(line[1])))
        elif ',' in line:
            line = line.split(',')
            updates.append([int(x) for x in line if x!= ',' ])


def create_graph(tuples):
   graph = defaultdict(set) 
   in_degree = defaultdict(int)
   for a, b in tuples:
       graph[a].add(b)
       in_degree[b] += 1
       in_degree.setdefault(a, 0)
   return graph, in_degree


def topological_sort(graph, in_degree):
    # Initialize deque with nodes having in-degree = 0
    zero_in_degree = deque([node for node in in_degree if in_degree[node] == 0])
    sorted_order = []

    while zero_in_degree:
        # Get the next node with in-degree = 0
        node = zero_in_degree.popleft()
        sorted_order.append(node)

        # Reduce the in-degree of its neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            # If a neighbor now has in-degree = 0, add it to the deque
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)

    # If the sorted order doesn't include all nodes, the graph has a cycle
    if len(sorted_order) != len(in_degree):
        raise ValueError("The graph contains a cycle, so no valid topological order exists.")

    return sorted_order


def custom_sort(data, tuples):
    # Need to keep only the tuples I need for the rule 
    nodes_needed = set(data)
    filtered_tuples = list(filter(lambda x: x[0] in nodes_needed, tuples)) 
    graph, in_degree = create_graph(filtered_tuples)
    custom_order = topological_sort(graph, in_degree)
    rank_mapping = {value: rank for rank, value in enumerate(custom_order)}

    return sorted(data, key=lambda x: rank_mapping.get(x, float('inf')))

verifies_updates = []
ordered_updates = []
for u in updates:
    custom_sorted_updates = custom_sort(u, ordering)
    # if topological sort is keeping the same order 
    if (u == custom_sorted_updates):
        verifies_updates.append(u)
    else:
        ordered_updates.append(custom_sorted_updates)
        
sum = 0
for v in verifies_updates:
    middle = len(v) // 2
    sum += v[middle]
print(f"Updates sum to {sum}")

sum_updated = 0
for v in ordered_updates:
    middle = len(v) // 2
    sum_updated += v[middle]
print(f"Corrected updates sum to {sum_updated}")