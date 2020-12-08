# --- Day 8: Handheld Halting ---

def read_instructions(input_file):
    instructions = []

    file = open(input_file, "r")

    for line in file:
        if not line.rstrip():
            continue

        instructions.append(line.rstrip())
    
    file.close()

    return instructions

def parse_int(string_with_int):
    number = 0
    multiplier = 1
    for char in reversed(string_with_int):
        if char == "-":
            number *= -1
            break
        elif not char.isdigit():
            break
        number += int(char) * multiplier
        multiplier *= 10
    return number

def get_highest_instruction_count(instructions_read_map):
    highest_read_count = 0
    for key in instructions_read_map:
        if instructions_read_map[key] > highest_read_count:
            highest_read_count = instructions_read_map[key]
    return highest_read_count

def get_accumulator_value(instructions, terminate_on_last_line):
    instructions_read_map = {}
    accumulator = 0
    index = 0

    for instruction in instructions:
        instructions_read_map[index] = 0
        index += 1
    
    # reset index
    index = 0

    while (True):
        # Part 1: check to see if we're about to re-read an instruction
        if not terminate_on_last_line and instructions_read_map[index] == 1:
            print("PROGRAM TERMINATING: instruction [{0}] was already read.".format(instructions[index]))
            break

        # read instruction
        instructions_read_map[index] = instructions_read_map[index] + 1
        instruction = instructions[index]
        instruction_segments = instruction.split()
        command = instruction_segments[0]
        value = parse_int(instruction_segments[1])

        # execute instruction
        if command == "nop":
            index += 1
        elif command == "acc":
            accumulator += value
            index += 1
        elif command == "jmp":
            index += value
        
        # Part 2: check to see if we're about to read past the end of file
        if terminate_on_last_line and index >= len(instructions):
            print("PROGRAM TERMINATING: program has read to the end of file.")
            break

    print("Final accumulator value: {0}".format(accumulator))
    return accumulator

def create_all_instruction_versions(instructions):
    instruction_variants = []

    index = 0
    for instruction in instructions:
        if "jmp" in instruction:
            instructions_copy = instructions.copy()
            instructions_copy[index] = instruction.replace("jmp","nop")
            instruction_variants.append(instructions_copy)
        elif "nop" in instruction:
            if parse_int(instruction.split()[1]) != 0:
                instructions_copy = instructions.copy()
                instructions_copy[index] = instruction.replace("nop","jmp")
                instruction_variants.append(instructions_copy)
        index += 1
    
    return instruction_variants

def program_terminates_at_end_of_file(instructions, max_counter=20000):
    accumulator = 0
    index = 0
    counter = 0

    while (True):
        # check to see if we've run this program too long
        if counter > max_counter:
            print("PROGRAM TERMINATING: {0} instructions have been executed.".format(counter))
            break

        # read instruction
        counter += 1
        instruction = instructions[index]
        instruction_segments = instruction.split()
        command = instruction_segments[0]
        value = parse_int(instruction_segments[1])

        # execute instruction
        if command == "nop":
            index += 1
        elif command == "acc":
            accumulator += value
            index += 1
        elif command == "jmp":
            # don't bother with jmp +0
            if value == 0:
                break
            index += value
        
        # check to see if we're about to read past the end of file
        if index >= len(instructions):
            print("PROGRAM TERMINATING: program has read to the end of file.")
            return True

    return False

def run_correct_instructions(original_instructions):
    # get the list of possible instruction variations
    instruction_variants = create_all_instruction_versions(original_instructions)

    # run each of the instruction variations to find the correct one
    new_instructions = None
    for instructions in instruction_variants:
        if program_terminates_at_end_of_file(instructions):
            new_instructions = instructions

    # get the accumulator for the correct instruction set
    return get_accumulator_value(new_instructions,True)

instructions = read_instructions("solutions\day08\day08_real.txt")
# get_accumulator_value(instructions,False)
run_correct_instructions(instructions)

