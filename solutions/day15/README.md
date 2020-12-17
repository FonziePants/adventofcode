# [Day 15: Rambunctious Recitation](https://adventofcode.com/2020/day/15)
>--- Day 15: Rambunctious Recitation ---
>
>You catch the airport shuttle and try to book a new flight to your vacation island. Due to the storm, all direct flights have been cancelled, but a route is available to get around the storm. You take it.
>
>While you wait for your flight, you decide to check in with the Elves back at the North Pole. They're playing a memory game and are ever so excited to explain the rules!
>
>In this game, the players take turns saying numbers. They begin by taking turns reading from a list of starting numbers (your puzzle input). Then, each turn consists of considering the most recently spoken number:
>
>- If that was the first time the number has been spoken, the current player says 0.
>- Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.
>
>So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or an age (if the last number is a repeat).
>
>For example, suppose the starting numbers are 0,3,6:
>
>- Turn 1: The 1st number spoken is a starting number, 0.
>- Turn 2: The 2nd number spoken is a starting number, 3.
>- Turn 3: The 3rd number spoken is a starting number, 6.
>- Turn 4: Now, consider the last number spoken, 6. Since that was the first time the number had been spoken, the 4th number spoken is 0.
>- Turn 5: Next, again consider the last number spoken, 0. Since it had been spoken before, the next number to speak is the difference between the turn number when it was last spoken (the previous turn, 4) and the turn number of the time it was most recently spoken before then (turn 1). Thus, the 5th number spoken is 4 - 1, 3.
>- Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5 and 2. So, the 6th number spoken is 5 - 2, 3.
>- Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart, the 7th number spoken is 1.
>- Turn 8: Since 1 is new, the 8th number spoken is 0.
>- Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference between them, 4.
>- Turn 10: 4 is new, so the 10th number spoken is 0.
>
>(The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)

I thought this problem would be very easy. On one hand, I was right because my solution for Part 1 could be reused without any changes for Part 2. However, I ended up hitting a bunch of python snags that a more experienced python developer probably wouldn't have hit.

## Part 1
>Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be 436.
>
>Here are a few more examples:
>
>- Given the starting numbers `1,3,2`, the 2020th number spoken is 1.
>- Given the starting numbers `2,1,3`, the 2020th number spoken is 10.
>- Given the starting numbers `1,2,3`, the 2020th number spoken is 27.
>- Given the starting numbers `2,3,1`, the 2020th number spoken is 78.
>- Given the starting numbers `3,2,1`, the 2020th number spoken is 438.
>- Given the starting numbers `3,1,2`, the 2020th number spoken is 1836.
>
>Given your starting numbers, what will be the 2020th number spoken?
>
>Your puzzle answer was **206**.

In my zeal for dictionaries, I decided to store each unique number as a key in a `dict` dictionary where its values were the indices in the list where it appeared. 

I used an array as the value instead of just storing the last time the number appeared because I thought for Part 2 it might have been needed. However, when Part 2 showed this wasn't the case, I rewrote the dictionary to only store the last time the value appeared.

### Snag 1
While reading the data from the file, I was keen enough to cast the comma-separated values as `int`. 

```
for i in range(len(list)-1):
    num = int(list[i])
    dict[num] = i
    list[i] = num
```

However, as I wanted to keep the last number out of dict for the sake of easier processing, I made the mistake of excluding it from this conversion function and thus not casting it correctly.

After a lot of frustration, I finally noticed the `6` in my test data amidst a collection of integers. This was just a good reminder that I hate the combination of dynamic typing and strict typing.

## Part 2
>--- Part Two ---
>
>Impressed, the Elves issue you a challenge: determine the 30000000th number spoken. For example, given the same starting numbers as above:
>
>- Given `0,3,6`, the 30000000th number spoken is 175594.
>- Given `1,3,2`, the 30000000th number spoken is 2578.
>- Given `2,1,3`, the 30000000th number spoken is 3544142.
>- Given `1,2,3`, the 30000000th number spoken is 261214.
>- Given `2,3,1`, the 30000000th number spoken is 6895259.
>- Given `3,2,1`, the 30000000th number spoken is 18.
>- Given `3,1,2`, the 30000000th number spoken is 362.
>
>Given your starting numbers, what will be the 30000000th number spoken?
>
>Your puzzle answer was **955**.

The solution:

1. Create a for-loop to iterate from the last element of the starting list through the desired stop

```'
for idx in range(len(dict),stop-1):
```

2. If the `last` number is already in the dictionary, calculate the next number with the number of turns since it has last appeared; otherwise, set it to zero

```
if last in dict:
    num = idx - dict[last]
else:
    num = 0
```

3. Add the `last` number to the dictionary and repeat the loop, using the calculated `num` as your new `last` number

```
dict[last] = idx
last = num
```

## Snag 2
I forgot that when you pass data into a python method, collections like lists and dictionaries are passed by reference and not by value. Thus, I was utterly bewildered when part 1 worked perfectly with `2020` iterations but part 2 failed despite using the same underlying method.

Largely because I performed my method cleanup before trying to run the program, thus changing too many variables at once, it took me awhile to realize that the data was being mutated in part 1 in a way that would cause part 2 to break. The solution was simple: either copy the data, or only run one part at a time. Oy vey.

