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

def get_accumulator_value_on_first_run(input_file):
    instructions = read_instructions(input_file)

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
            print("Instruction [{0}] was already read.".format(instructions[index]))
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

    print("Final accumulator value: {0}".format(accumulator))
    return accumulator

get_accumulator_value_on_first_run("solutions\day08\day08_real.txt")
