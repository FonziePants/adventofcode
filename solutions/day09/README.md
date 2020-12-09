# [Day 9: Encoding Error](https://adventofcode.com/2020/day/9)
>With your neighbor happily enjoying their video game, you turn your attention to an open data port on the little screen in the seat in front of you.
>
>Though the port is non-standard, you manage to connect it to your computer through the clever use of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).
>
>The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, conveniently for you, is an old cypher with an important weakness.
>
>XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one such pair.
>
>For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be valid, the next number must be the sum of two of those numbers:
>
>- 26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
>- 49 would be a valid next number, as it is the sum of 24 and 25.
>- 100 would not be valid; no two of the previous 25 numbers sum to 100.
>- 50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.
>
>Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 numbers ago) was 20. Now, for the next number to be valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to it:
>
>- 26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
>- 65 would not be valid, as no two of the available numbers sum to it.
>- 64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.

I'm not a huge fan of these kinds of problems because there's always a pretty straightforward approach involving looping through collections, carefully choosing iterators, and performing simple equality checks. It's not that I mind when problems are easy, but I don't like that the most frustrating parts of these problems are typically minor errors in choosing iterators and indices. I'd rather work on problems that involve thoughtful data representation and interesting data manipulation and mutation.

This problem might be more interesting if the challenge was making it performant -- avoiding nested loops, etc, but Advent of Code incentivizes speed over performance, so that's the direction I've been taking.

## Part 1
>Here is a larger example which only considers the previous 5 numbers (and has a preamble of length 5):
>```
>35
>20
>15
>25
>47
>40
>62
>55
>65
>95
>102
>117
>150
>182
>127
>219
>299
>277
>309
>576
>```
>In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only number that does not follow this rule is 127.
>
>The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?
>
>Your puzzle answer was **393911906**.

The only real snafu I ran into here was when I forgot to cast the lines I was reading into my array as `int` and so my arithmetic clearly didn't work as planned. Luckily, that was a quick and obvious fix (because by no means should `35` + `20` have a value of `3525`).

My approach was really simple:
- Loop through the array starting after the preamble
- For each number, try adding all possible combinations of 2 entries together
- If you find a valid pair, flip the `valid` flag, abort from the inner loop, and move onto the next number to check

```
def find_first_invalid_number(full_num_array, preamble):
    if len(full_num_array) < preamble:
        return None
    
    for i in range(preamble,len(full_num_array)):
        num = full_num_array[i]

        valid = False
        for j in range(i-preamble,i):
            for k in range(j+1,i):
                prev1 = full_num_array[j]
                prev2 = full_num_array[k]

                if num == (prev1 + prev2):
                    valid = True
                    break
            if valid:
                break
        
        if not valid:
            print("Number {0} at index {1} is NOT valid. Stop processing.".format(num, i))
            return i #index of num
```

## Part 2
>--- Part Two ---
>
>The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.
>
>Again consider the above example:
>```
>35
>20
>15
>25
>47
>40
>62
>55
>65
>95
>102
>117
>150
>182
>127
>219
>299
>277
>309
>576
>```
>In this list, adding up all of the numbers from 15 through 40 produces the invalid number from step 1, 127. (Of course, the contiguous set of numbers in your actual list might be much longer.)
>
>To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example, these are 15 and 47, producing 62.
>
>What is the encryption weakness in your XMAS-encrypted list of numbers?
>
>Your puzzle answer was **59341885**.

For this, I just brute-forced it. I took the subset of the num array between its start and the first invalid number...
```
def find_contiguous_set_of_addends(full_num_array,index_of_num,debug=False):
    num_array_subset = full_num_array[:index_of_num]
    sum_target = full_num_array[index_of_num]
```
...and I iterated through every possible contiguous sum within that range. There were probably heuristics I could have applied to the range I was looking at to avoid some checks, but because Advent of Code incentivizes speed over performance (and because I wanted to beat my spouse today), I didn't bother with those kinds of optimizations.
```
    # iterate through all the possible starting numbers
    for start in range(len(num_array_subset)):

        # iterate through all the possible sequence lengths
        for stop in range(start+1,len(num_array_subset)):

            sum = 0
            highest_num = 0
            lowest_num = sum_target * 10000
            for i in range(start,stop+1): #stop+1 makes it inclusive
                num = num_array_subset[i]
                sum += num

                if num > highest_num:
                    highest_num = num
                
                if num < lowest_num:
                    lowest_num = num
            
            if debug:
                print("Sum of values between index {0} (value = {1}) and index {2} (value = {3}) is {4}.".format(start,num_array_subset[start],stop,num_array_subset[stop],sum))
            
            if sum == sum_target:
                encryption_weakness = highest_num + lowest_num
                print("Sequence found! Terminate program. Encryption weakness = {0}".format(encryption_weakness))
                return encryption_weakness
```

The debug print took awhile to run (over a minute 😅), but if I toggled that off, I got the answer in a matter of seconds. 