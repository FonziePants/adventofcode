# [Day 14: Shuttle Search](https://adventofcode.com/2020/day/14)
>--- Day 14: Docking Data ---
>
>As your ferry approaches the sea port, the captain asks for your help again. The computer system that runs this port isn't compatible with the docking program on the ferry, so the docking parameters aren't being correctly initialized in the docking program's memory.
>
>After a brief inspection, you discover that the sea port's computer system uses a strange bitmask system in its initialization program. Although you don't have the correct decoder chip handy, you can emulate it in software!
>
>The initialization program (your puzzle input) can either update the bitmask or write a value to memory. Values and memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.
>
>The bitmask is always given as a string of 36 bits, written with the most significant bit (representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right. The current bitmask is applied to values immediately before they are written to memory: a 0 or 1 overwrites the corresponding bit in the value, while an X leaves the bit in the value unchanged.
>
>For example, consider the following program:
>```
>mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
>mem[8] = 11
>mem[7] = 101
>mem[8] = 0
>```
>This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite two bits in every written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten with 1.
>
>The program then attempts to write the value 11 to memory address 8. By expanding everything out to individual bits, the mask is applied as follows:
>```
>value:  000000000000000000000000000000001011  (decimal 11)
>mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
>result: 000000000000000000000000000001001001  (decimal 73)
>```
>So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program tries to write 101 to address 7:
>```
>value:  000000000000000000000000000001100101  (decimal 101)
>mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
>result: 000000000000000000000000000001100101  (decimal 101)
>```
>This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to set. Finally, the program tries to write 0 to address 8:
>```
>value:  000000000000000000000000000000000000  (decimal 0)
>mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
>result: 000000000000000000000000000001000000  (decimal 64)
>```
>64 is written to address 8 instead, overwriting the value that was there previously.

Binary math and manipulation are pretty fun, so I was hopeful about this problem.

## Part 1
>To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.) In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.
>
>Execute the initialization program. What is the sum of all values left in memory after it completes?
>
>Your puzzle answer was **5875750429995**.

For this problem, I reused a `convert_to_binary` method from a previous problem and also created a `convert_to_decimal` one. 

The approach was pretty simple:

1. Create a for-loop to iterate through each line in the file
2. If the line is a mask definition line, pull the data and overwrite the `mask` variable
```
mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
for line in data:
    if "mask" in line:
        mask = line[6:]
```

3. Otherwise, parse the memory address and value out of the line, convert the value to binary so that a mask can be applied, and then store the data in a dictionary `memory` where the `address` is the key
```
else:
    parts = line.split("] = ") 
    address = parts[0][4:]
    dec_val = int(parts[1])
    bin_val = convert_to_binary(dec_val)
    bin_val = apply_mask(mask, bin_val)
    dec_val = convert_to_decimal(bin_val)
    memory[address] = dec_val
```

4. For the `apply_mask` method...
- Add leading zeroes to the number-to-be-modified as necessary
```
while len(bin_num) < len(mask):
    bin_num = "0" + bin_num
```
- Iterate through each character of the mask and if the character _isn't_ `X`, then overwrite the corresponding character in the number-to-be-modified

```
for i in range(len(mask_list)):
    if mask_list[i] == "X":
        continue
    bin_list[i] = mask_list[i]
```
5. Lastly, once all of the lines have been read, all the masks have been applied, and all the values have been written to memory, iterate through each memory address to increment a sum variable. 
```
for address in memory:
    sum += memory[address]
```

## Part 2
>--- Part Two ---
>
>For some reason, the sea port's computer system still can't communicate with your ferry's docking program. It must be using version 2 of the decoder chip!
>
>A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts as a memory address decoder. Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address in the following way:
>
>- If the bitmask bit is 0, the corresponding memory address bit is unchanged.
>- If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
>- If the bitmask bit is X, the corresponding memory address bit is floating.
>
>A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, this means the floating bits will take on all possible values, potentially causing many memory addresses to be written all at once!
>
>For example, consider the following program:
>```
>mask = 000000000000000000000000000000X1001X
>mem[42] = 100
>mask = 00000000000000000000000000000000X0XX
>mem[26] = 1
>```
>When this program goes to write to memory address 42, it first applies the bitmask:
>```
>address: 000000000000000000000000000000101010  (decimal 42)
>mask:    000000000000000000000000000000X1001X
>result:  000000000000000000000000000000X1101X
>```
>After applying the mask, four bits are overwritten, three of which are different, and two of which are floating. Floating bits take on every possible combination of values; with two floating bits, four actual memory addresses are written:
>```
>000000000000000000000000000000011010  (decimal 26)
>000000000000000000000000000000011011  (decimal 27)
>000000000000000000000000000000111010  (decimal 58)
>000000000000000000000000000000111011  (decimal 59)
>```
>Next, the program is about to write to memory address 26 with a different bitmask:
>```
>address: 000000000000000000000000000000011010  (decimal 26)
>mask:    00000000000000000000000000000000X0XX
>result:  00000000000000000000000000000001X0XX
>```
>This results in an address with three floating bits, causing writes to eight memory addresses:
>```
>000000000000000000000000000000010000  (decimal 16)
>000000000000000000000000000000010001  (decimal 17)
>000000000000000000000000000000010010  (decimal 18)
>000000000000000000000000000000010011  (decimal 19)
>000000000000000000000000000000011000  (decimal 24)
>000000000000000000000000000000011001  (decimal 25)
>000000000000000000000000000000011010  (decimal 26)
>000000000000000000000000000000011011  (decimal 27)
>```
>The entire 36-bit address space still begins initialized to the value 0 at every address, and you still need the sum of all values left in memory at the end of the program. In this example, the sum is 208.
>
>Execute the initialization program using an emulator for a version 2 decoder chip. What is the sum of all values left in memory after it completes?
>
>Your puzzle answer was **5272149590143**.

I _thought_ this should be easy (despite my rival's warnings), and my approach was as follows:

1. Reuse the same logic for:
    - Pulling the data from the file
    - Detecting a mask and a memory line
    - Parsing the memory line information
    - Converting binary and decimal numbers
2. Modify the `apply_mask` method to handle part 2 differently: whereas `X` was ignored and `0` would overwrite in part 1, now `X` would overwrite and `0` would be ignored in part 2
```
for i in range(len(mask_list)):
    if mask_list[i] == "X" and not pt2:
        continue
    elif mask_list[i] == "0" and pt2:
        continue
    bin_list[i] = mask_list[i]
```
3. Apply the mask to the _address_ instead of the value, and consider this a "base address" from which we will generate a full list of addresses of all permutations where `X` must be replaced with `0` and `1`
```
dec_address = int(parts[0][4:])
bin_address = convert_to_binary(dec_address)
bin_address = apply_mask(mask, bin_address, True)
addresses = generate_addresses(bin_address)
for address in addresses:
    memory[address] = value
```
4. Generate all possible addresses by:
  - Initiate an `addresses` list with a single item: the `base_address`
  - Create a for-loop that increments an index variable for each character in the `base_address` size
  - For each iteration where the character in the `base_address` is `X`, create a _new_ list for addresses (`new_addresses`) and for each address in the original `addresses` list, add two items to the new list:
    - One where the `X` at `idx` is replaced with `0`
    - One where the `X` at `idx` is replaced with `1`
  - Then replace `addresses` with `new_addresses`
```
if base_address[idx] != "X":
    continue
new_addresses = []
for address in addresses:
    add_list = list(address)
    for b in range(0,2):
        add_list[idx] = str(b)
        new_addresses.append("".join(add_list))
addresses = new_addresses
```
5. Then, update the values at all of the newly-generated addresses.
```
for address in addresses:
    memory[address] = value
```
6. Lastly, use the existing summing method to get the final answer.

I thought this was pretty clear and I didn't foresee any meaningful optimizations, so I asked my rival what he thought was the issue with Part 2. He had approached this problem by instantiating _all_ of the possible memory addresses -- whether or not they were used -- which led to unreasonable amounts of memory being allocated. 

I was reassured by this because my dictionary approach would only store memory addresses that are actually used, thus reaffirming my belief that dictionaries (or hashmaps) are pretty much the most versatile data structure ever (with both their iterability and instant lookups).

I had a mild panic when I tried to run my program against the original test data from Part 1 -- I observed that my `generate_addresses` method was pretty fast until hitting the 22nd or so `X`, in which case it slowed to an exponentially-increasing crawl. For a moment, I thought, maybe my rival was right?!

Luckily, I rechecked the problem statement and realized two things:
1. _Different_ test data was provided for Part 2
2. The _real_ data never had more than 20 `X`s

Cautiously, I ran the program against the actual Part 2 test data and was relieved to see it generated an answer very quickly. Then, moving onto the real data, I received my answer in less than a second. CRISIS AVERTED!