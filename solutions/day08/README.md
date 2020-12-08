# [Day 8: Handheld Halting](https://adventofcode.com/2020/day/8)
>--- Day 8: Handheld Halting ---
>
>Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to you.
>
>Their handheld game console won't turn on! They ask if you can take a look.
>
>You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should be able to fix it, but first you need to be able to run the code in isolation.
>
>The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).
>
>- acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
>- jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
>- nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
>
>For example, consider the following program:
>```
>nop +0
>acc +1
>jmp +4
>acc +3
>jmp -3
>acc -99
>acc +1
>jmp -4
>acc +6
>```
>These instructions are visited in this order:
>```
>nop +0  | 1
>acc +1  | 2, 8(!)
>jmp +4  | 3
>acc +3  | 6
>jmp -3  | 7
>acc -99 |
>acc +1  | 4
>jmp -4  | 5
>acc +6  |
>```
>First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.
>
>This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to run any instruction a second time, you know it will never terminate.
>
>Immediately before the program would run an instruction a second time, the value in the accumulator is 5.

I finally gave up on my "write a class first" approach as this problem didn't seem to necessitate any convenience methods. I relied instead on the following two data structures:
- An **array of strings** where each item represents an instruction (this was super easy to parse from the file, line by line)
- A **dictionary with integers for its keys and values**.
  - The **key** represented the instruction's line number (i.e. its index in the array of strings)
  - The **value** represented the number of times it appeared (in reality, I could have just gave it a Boolean value, but I wasn't thinking things through...)

Reading instructions only involved:
1. **Splitting the instruction** (by a space character) into two segments
2. Saving the first string segment as the **command** (i.e. `nop`, `jmp`, `acc`)
3. Converting the second string segment to an int and saving it as the **value** (i.e. how far to jump or by how much to accumulate)

## Part 1
>Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?
>
>Your puzzle answer was **1941**.

To run the instructions, all that was needed was the following:
1. Infinite while loop
2. Break if an instruction is about to be read a second time (i.e. check to see if the instruction is already in our dictionary of already-read-instructions)
3. Otherwise, add the instruction to the dictionary of already-read-instructions and proceed
4. If the instruction is `nop` then increment the line count by 1
5. If the instruction is `jmp` then increment the line count by the instruction's value (unless the value equals `0`, in which case this is an infinite loop so we might as well stop processing the instructions)
6. If the instruction is `acc` then increment the line count by 1 and the accumulator by the instruction's value
```
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
```
7. If the line count is beyond the file size, return that accumulator value
8. If the while loop exits without returning anything, then that instruction set hit an infinite loop, so print the accumulator value but return `None`

Part 1 only required that last condition because the input file was bound to hit an infinite loop.

## Part 2
>--- Part Two ---
>
>After some careful analysis, you believe that exactly one instruction is corrupted.
>
>Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)
>
>The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.
>
>For example, consider the same program from above:
>```
>nop +0
>acc +1
>jmp +4
>acc +3
>jmp -3
>acc -99
>acc +1
>jmp -4
>acc +6
>```
>If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.
>
>However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:
>```
>nop +0  | 1
>acc +1  | 2
>jmp +4  | 3
>acc +3  |
>jmp -3  |
>acc -99 |
>acc +1  | 4
>nop -4  | 5
>acc +6  | 6
>```
>After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).
>
>Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
>
>Your puzzle answer was **2096**.

During my first implementation, I foolishly removed my check-for-infinite-loop logic (oops!) and added an is-this-running-too-long? counter instead. This was dumb, so I later went back and fixed it. The final logic for my Part 2 solution is as follows:
1. Create an empty array `instruction_variants` in which I will store all possible instruction set variations
2. For each instruction in the original instruction set, check to see if I should add a new variation to the aforementioned array:
    - For `jmp` commands, make a copy of the original instruction set, change that specific `jmp` instruction to `nop`, and add it to my `instruction_variants` list
    - For `nop` commands whose value is not 0 (becauase this will result in an infinite loop), make a copy of the original instruction set, change that specific `nop` instruction to `jmp`, and add it to my `instruction_variants` list
```
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
```

3. Then, for each instruction variant, run the original program
4. If a specific instruction set makes it to the end of the file successfully, then break! That's the correct instruction set, so that program will have the desired accumulator value

That's all, folks.