
reports = []

with open("input.txt", "r") as file:
    for line in file:
        line = line.strip().split()
        levels = [int(i) for i in line]
        reports.append(levels)

def verify_safe(l):
    if len(l) <= 1:
        return True
    else:
        differences = [ l[i] - l[i-1] for i in range(1, len(l))]
        positif_differences = [ int(x > 0) for x in differences]

        if any(x == 0 for x in differences):
            return False
    
        if l[1] > l[0]:
            if sum(positif_differences) == len(positif_differences):
                return max(differences) <= 3
            else:
                return False   
        else:
            if sum(positif_differences) == 0:
                return min(differences) >= -3
            else: 
                return False

def verify_reports(reports):
    safe_report_counter = 0 
    for r in reports:
        if verify_safe(r):
            safe_report_counter +=1
    return safe_report_counter


print(f"There are {verify_reports(reports)} reports safe")
    

def verify_reports_with_tolerance(reports):
    safe_report_counter = 0 
    for r in reports:
        safeness = verify_safe(r)

        if safeness:
            safe_report_counter += 1
            continue
        else:
            for i in range(len(r)):
                modified_list = r[:i] + r[i+1:]
                if verify_safe(modified_list):
                    safe_report_counter +=1
                    break
   
    return safe_report_counter 

print(f"There are {verify_reports_with_tolerance(reports)} reports safe with tolerance")
