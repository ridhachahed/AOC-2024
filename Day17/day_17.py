def read_input(file_name):
    register_a = None
    register_b = None
    register_c = None
    program = []
    with open(file_name) as f:
        for line in f:
            if "Register A:" in line:
                register_a = int(line.strip().split(":")[1])
            elif "Register B:" in line:
                register_b = int(line.strip().split(":")[1])
            elif "Register C:" in line:
                register_c = int(line.strip().split(":")[1])
            elif "Program:" in line:
                line = line.strip().split(":")[1]
                program = [int(c) for c in line.split(",")]
    return register_a, register_b, register_c, program

def get_combo(number, register_a, register_b, register_c):
    if 0 <= number <= 3:
        return number
    if number == 4: 
        return register_a
    elif number == 5: 
        return register_b
    elif number == 6: 
        return register_c
    else:
        return number # not allowed

def do_operation(instruction_pointer, register_a, register_b, register_c, opcode, operand):
    
    combo = get_combo(operand, register_a, register_b, register_c)
    output = None
    if opcode == 0:
        numerator = register_a
        denominator = 2 ** combo
        register_a = numerator // denominator
        instruction_pointer += 2
    elif opcode == 1:
        register_b = register_b ^ operand
        instruction_pointer += 2
    elif opcode == 2:
        register_b = combo % 8 
        instruction_pointer += 2
    elif opcode == 3:
        if register_a != 0:
            # Jumps
            instruction_pointer = operand
        else:
            instruction_pointer += 2
    elif opcode == 4:
        register_b = register_b ^ register_c
        instruction_pointer += 2
    elif opcode == 5:
        # only output
        output = combo % 8
        instruction_pointer += 2
    elif opcode == 6: 
        numerator = register_a
        denominator = 2 ** combo
        register_b = numerator // denominator
        instruction_pointer += 2
    elif opcode == 7: 
        numerator = register_a
        denominator = 2 ** combo
        register_c = numerator // denominator
        instruction_pointer += 2
    return output, instruction_pointer, register_a, register_b, register_c


def simulate(register_a, register_b, register_c, program):
    results = []
    instruction_pointer = 0
    while instruction_pointer < len(program) - 1:
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        output, instruction_pointer, register_a, register_b, register_c = do_operation(instruction_pointer, register_a, register_b, register_c, opcode, operand)
        if output is not None:
            results.append(str(output))
    return ",".join(results)


def demo(register_a, register_b, register_c, program):
    output = simulate(register_a, register_b, register_c, program)
    return output

register_a, register_b, register_c, program = read_input("input.txt")
result = demo(register_a, register_b, register_c, program)
print(result)

# Part 2
def simulate_aux(current_register_a, register_b, register_c, reversed_program):
    if len(reversed_program) == 0:
        return current_register_a
    else:
        element_to_guess = reversed_program[0]
        current_register_a = current_register_a << 3
        for ending in range(8):
            trial = current_register_a
            trial += ending
            output = demo(trial, register_b, register_c, program)
            #print(f"Objective is {element_to_guess}")
            #print(f"Output is {output[0]}")
            if str(output[0]) == str(element_to_guess):
                print(f"{output}")
                recursive_call = simulate_aux(trial, register_b, register_c, reversed_program[1:])
                if recursive_call:
                    return recursive_call
    
reversed_program = program[::-1]
current_register_a = 0
result = simulate_aux(0, register_b, register_c, reversed_program)
print(result)

register_a, register_b, register_c, program = read_input("input.txt")
result = demo(result, register_b, register_c, program)
print(result)
