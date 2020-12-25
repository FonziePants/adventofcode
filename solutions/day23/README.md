# [Day 23: Crab Cups](https://adventofcode.com/2020/day/23)
>--- Day 23: Crab Cups ---
>
>The small crab challenges you to a game! The crab is going to mix up some cups, and you have to predict where they'll end up.
>
>The cups will be arranged in a circle and labeled clockwise (your puzzle input). For example, if your labeling were 32415, there would be five cups in the circle; going clockwise around the circle from the first cup, the cups would be labeled 3, 2, 4, 1, 5, and then back to 3 again.
>
>Before the crab starts, it will designate the first cup in your list as the current cup. The crab is then going to do 100 moves.
>
>Each move, the crab does the following actions:
>
>- The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
>- The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
>- The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
>- The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
>
>For example, suppose your cup labeling were 389125467. If the crab were to do merely 10 moves, the following changes would occur:
>```
>-- move 1 --
>cups: (3) 8  9  1  2  5  4  6  7 
>pick up: 8, 9, 1
>destination: 2
>
>-- move 2 --
>cups:  3 (2) 8  9  1  5  4  6  7 
>pick up: 8, 9, 1
>destination: 7
>
>-- move 3 --
>cups:  3  2 (5) 4  6  7  8  9  1 
>pick up: 4, 6, 7
>destination: 3
>
>-- move 4 --
>cups:  7  2  5 (8) 9  1  3  4  6 
>pick up: 9, 1, 3
>destination: 7
>
>-- move 5 --
>cups:  3  2  5  8 (4) 6  7  9  1 
>pick up: 6, 7, 9
>destination: 3
>
>-- move 6 --
>cups:  9  2  5  8  4 (1) 3  6  7 
>pick up: 3, 6, 7
>destination: 9
>
>-- move 7 --
>cups:  7  2  5  8  4  1 (9) 3  6 
>pick up: 3, 6, 7
>destination: 8
>
>-- move 8 --
>cups:  8  3  6  7  4  1  9 (2) 5 
>pick up: 5, 8, 3
>destination: 1
>
>-- move 9 --
>cups:  7  4  1  5  8  3  9  2 (6)
>pick up: 7, 4, 1
>destination: 5
>
>-- move 10 --
>cups: (5) 7  4  1  8  3  9  2  6 
>pick up: 7, 4, 1
>destination: 3
>
>-- final --
>cups:  5 (8) 3  7  4  1  9  2  6 
>```
>In the above example, the cups' values are the labels as they appear moving clockwise around the circle; the current cup is marked with ( ).
>
>After the crab is done, what order will the cups be in? Starting after the cup labeled 1, collect the other cups' labels clockwise into a single string with no extra characters; each number except 1 should appear exactly once. In the above example, after 10 moves, the cups clockwise from 1 are labeled 9, 2, 6, 5, and so on, producing 92658374. If the crab were to complete all 100 moves, the order after cup 1 would be 67384529.

I was going to wait until tomorrow, but I discovered that my roommate had skipped yesterday's puzzle and was trying to edge me out on this one for the extra stars! I jumped into action and managed to knock out Part 1 in about ten minutes. Luckily for me, Part 1 was doable with simple python string manipulation, of which I had learned the syntax over the past couple weeks.

🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀

## Part 1
>Using your labeling, simulate 100 moves. What are the labels on the cups after cup 1?
>
>Your puzzle input was `215694783`.
>
>Your puzzle answer was **46978532**.

I can't say I'm proud of my solution for this one. I hard-coded random things, used opaque variable names, and left the data a string in an attempt to beat my rival to the answer.

Here is my quick and dirty logic to calculate the high and low bounds of the problem:
```
rounds = 100 
highest = -1
lowest = 100
for c in data:
    n = int(c)
    if n > highest:
        highest = n
    elif n < lowest:
        lowest = n
```

I used a for-loop to execute each round:
```
for i in range(rounds):
    print("{0}: {1}\n\n".format(i+1,data))
    data = round(data,lowest,highest)
```

...where each round was just a bunch of hacky string manipulations:
```
def round(data,lowest, highest):
    pickup = data[1:4]
    data = data[0] + data[4:]
    destination = int(data[0])-1

    while str(destination) not in data:
        destination -= 1
        if destination < lowest:
            destination = highest
    
    index = data.index(str(destination)) + 1
    if index >= len(data):
        data += pickup
    else:
        data = data[0:index] + pickup + data[index:]
    
    data = data[1:] + data[0]
    
    return data
```

...and because I moved the first character to the back instead of actually iterating through the character array, I had to reverse my modifications for the same number of rounds (and yes, I could have used modulo to make the string correction exactly once, but I was racing and the for-loop was quicker):
```
for i in range(rounds):
    data = data[-1:] + data[0:-1]
```

## Part 2
>--- Part Two ---
>
>Due to what you can only assume is a mistranslation (you're not exactly fluent in Crab), you are quite surprised when the crab starts arranging many cups in a circle on your raft - one million (1000000) in total.
>
>Your labeling is still correct for the first few cups; after that, the remaining cups are just numbered in an increasing fashion starting from the number after the highest number in your list and proceeding one by one until one million is reached. (For example, if your labeling were 54321, the cups would be numbered 5, 4, 3, 2, 1, and then start counting up from 6 until one million is reached.) In this way, every number from one through one million is used exactly once.
>
>After discovering where you made the mistake in translating Crab Numbers, you realize the small crab isn't going to do merely 100 moves; the crab is going to do ten million (10000000) moves!
>
>The crab is going to hide your stars - one each - under the two cups that will end up immediately clockwise of cup 1. You can have them if you predict what the labels on those cups will be when the crab is finished.
>
>In the above example (389125467), this would be 934001 and then 159792; multiplying these together produces 149245887792.
>
>Determine which two cups will end up immediately clockwise of cup 1. What do you get if you multiply their labels together?
>
>Your puzzle answer was **163035127721**.

Once I realized that the numbers now extended beyond `9`, I realized I'd need to use an array instead of a string. I hurriedly copied and pasted my `round` method into a `round2` method and made the appropriate changes to:

- Convert the string into an integer array
- Extend the integer array to `1000000`
- Change the number of rounds to `10000000`

This failed. Miserably.

Turns out, my array (or `list` as they call them in Python) manipulations were _expensive_, and it would take hours and hours to run. Oy vey.

I naively hoped that Python lists would someone have the benefits of both arrays (with instant lookups afforded by preallocated, sequential memory) and linked lists (with efficient element additions and removals). I quickly realized that short of learning how to find and load a third-party python library (which yes, is _absolutely_ something I should learn to do), I would need to implement my own linked list.

Things of which I am proud:

- I was able to implement a doubly linked list rather quickly despite not having done so for about 12 years
- I had the foresight to include a dictionary property called `nodes` in my `LinkedList` class where the key was the numeric value of the node and the value was the node itself (typing that out is confusing...)

Things that should embarrass me:

- My poor extensibility (my `LinkedList` constructor is tightly coupled to this problem, and my insertion and pop methods are likewise so)
- My arbitrary use of methods versus class methods (I should really read up on overloading constructors and all that jazz)

But again, I was racing.

My `Node` class looked as follows:
```
class Node:
    def __init__(self,value,prev,next):
        self.value = value
        self.prev = prev
        self.next = next
```

Nothing special, clearly.

Then, my `LinkedList` class had a convoluted constructor that initialized the data and had absolutely _zero_ convenience methods:
```
class LinkedList:
    def __init__(self,starting,max):
        self.nodes = {}
        self.start = None
        highest = -1
        prev = None
        for character in starting:
            num = int(character)
            if num > highest:
                highest = num
            node = Node(num,prev,None)
            if self.start == None:
                self.start = node
            if prev:
                prev.next = node
            self.nodes[num] = node
            prev = node
        
        for i in range(highest,max):
            node = Node(i+1,prev,None)
            if prev:
                prev.next = node
            self.nodes[node.value] = node
            prev = node
        
        prev.next = self.start
        self.start.prev = prev
```

In lieu of class methods, I created global methods that worked by modifying node relationships and didn't actually need access to the `LinkedList`. It's all a messy violation of data access privileges and best practices, but so is life, amirite?
```
def pop_three(prev):
    first = prev.next
    third = first.next.next
    fourth = third.next
    prev.next = fourth
    fourth.prev = prev
    third.next = None
    return first

def insert_three(prev,first):
    third = first.next.next
    fourth = prev.next
    third.next = fourth
    fourth.prev = third
    prev.next = first
    first.prev = prev
```

The plus side of all this mess is that my actual Part 2 procedures looked... simpler? I guess?
```
def calculate_part2(data,debug=False):
    rounds = 10000000
    max = 1000000
    
    data = LinkedList(data,max)
    
    node = data.start
    for i in range(rounds):
        popped = pop_three(node)
        dest = node.value-1

        if dest == 0:
            dest = max

        values = [popped.value, popped.next.value, popped.next.next.value]
        while dest in values:
            dest -= 1

            if dest < 1:
                dest = max
        
        prev = data.nodes[dest]
        insert_three(prev,popped)

        node = node.next
    
    one = data.nodes[1]
    answer = one.next.value * one.next.next.value
    print("{0} x {1} = {2}".format(one.next.value,one.next.next.value,answer))

    print("Part 2: {0}\n\n".format(answer))
```

The good news for this trainwreck of a solution? I finished first on my private leaderboard, putting me in a solid second place with a possibility of winning overall if I can sabotage my husband over the next two days...

Stay tuned 😎

🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀