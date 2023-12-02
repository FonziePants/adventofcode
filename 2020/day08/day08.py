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

def get_accumulator(instructions):
    instructions_read_map = {}
    accumulator = 0
    index = 0

    for instruction in instructions:
        instructions_read_map[index] = 0
        index += 1
    
    # reset index
    index = 0

    while (True):
        # check to see if we're about to re-read an instruction
        if instructions_read_map[index] == 1:
            print("PROGRAM TERMINATING: instruction [{0}] was already read.  Final accumulator value: {1}".format(instructions[index], accumulator))
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
            # don't bother with jmp +0
            if value == 0:
                break
            index += value
        
        # check to see if we're about to read past the end of file
        if index >= len(instructions):
            print("PROGRAM TERMINATING: program has read to the end of file. Final accumulator value: {0}".format(accumulator))
            return accumulator

    return None

def run_correct_instructions(original_instructions):
    # get the list of possible instruction variations
    instruction_variants = create_all_instruction_versions(original_instructions)

    # run each of the instruction variations to find the correct one
    new_instructions = None
    for instructions in instruction_variants:
        accumulator = get_accumulator(instructions)
        if accumulator:
            return accumulator

instructions = read_instructions("day08_real.txt")
get_accumulator(instructions)
run_correct_instructions(instructions)