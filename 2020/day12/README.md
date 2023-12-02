# [Day 12: Rain Risk](https://adventofcode.com/2020/day/12)
>--- Day 12: Rain Risk ---
>
>Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!
>
>Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.
>
>The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:
>
>- Action `N` means to move **north** by the given value.
>- Action `S` means to move **south** by the given value.
>- Action `E` means to move **east** by the given value.
>- Action `W` means to move **west** by the given value.
>- Action `L` means to turn **left** the given number of degrees.
>- Action `R` means to turn **right** the given number of degrees.
>- Action `F` means to move **forward** by the given value in the direction the ship is currently facing.
>
>The ship starts by facing **east**. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)
>
>For example:
>```
>F10
>N3
>F7
>R90
>F11
>```
>These instructions would be handled as follows:
>
>- `F10` would move the ship 10 units east (because the ship starts by facing east) to **east 10, north 0**.
>- `N3` would move the ship 3 units north to **east 10, north 3**.
>- `F7` would move the ship another 7 units east (because the ship is still facing east) to **east 17, north 3**.
>- `R90` would cause the ship to turn right by 90 degrees and face south; it remains at **east 17, north 3**.
>- `F11` would move the ship 11 units south to **east 17, south 8**.
>
>At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is `17 + 8` = **25**.

My first impression was that this problem would be mildly fun but not particularly challenging.

- _Mildly fun_ because there were a few types of inputs that would need to be treated differently, which I imagined would lend itself to various ways to solve the problem
- _Not particularly challenging_ because the commands themselves all seemed pretty straightforward

## Part 1
>Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
>
>Your puzzle answer was **590**.

There were no apparent tricks to this one. Basically, you'd have to:

1. **Read the file and store a list of "instructions."** Sure, you could make a custom instruction class, but the instructions themselves were so simple that I found **tuples** (in my case, a pair of character `action` and int `value`) to be sufficient.
1. **Iterate through each instruction.** A loop. Nothing special.
1. **Execute each instruction** by tracking the ship's current position (a tuple of **x** and **y** coordinates called `curr_coord` in my case) and the ship's current direction (a character of `E`, `N`, `W`, or `S`, which I called `curr_dir`), and modifying these variables in different ways depending on the specific action.
```
if action == Commands.FORWARD:
    action = curr_dir

if action in Directions.ALL:
    delta = Directions.calculate_change(action, value)
    curr_coord = (curr_coord[0] + delta[0],curr_coord[1] + delta[1])
else:
    curr_dir = calculate_new_direction(curr_dir, action, value)
```
Note in the above code, I change the `F` command to be the current direction (i.e. either `N`, `W`, `S`, or `E`) and let the code continue into the `if action in Directions.ALL:` condition.

The part I had the most fun with was the logic for calculating the new direction based on the ship's current heading and how many degrees it needed to rotate. For this, I created a `calculate_new_direction` method that took the two aforementioned pieces of data, and used index-modification to pull the correct cardinal direction out of an array:
```
class Directions:
    EAST = "E"
    WEST = "W"
    NORTH = "N"
    SOUTH = "S"
    ALL = [EAST, NORTH, WEST, SOUTH]
```
```
def calculate_new_direction(starting_direction, command, degrees):
    if command == Commands.FORWARD:
        return starting_direction

    dir_idx = Directions.ALL.index(starting_direction)
    idx_change = int(degrees / 90)

    if command == Commands.RIGHT:
        idx_change *= -1

    dir_idx += idx_change
    dir_idx %= len(Directions.ALL)

    return Directions.ALL[dir_idx]
```

## Part 2
>--- Part Two ---
>
>Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.
>
>Almost all of the actions indicate how to move a **waypoint** which is relative to the ship's position:
>
>Action N means to move the waypoint **north** by the given value.
>Action S means to move the waypoint **south** by the given value.
>Action E means to move the waypoint **east** by the given value.
>Action W means to move the waypoint **west** by the given value.
>Action L means to rotate the waypoint around the ship **left** (counter-clockwise) the given number of degrees.
>Action R means to rotate the waypoint around the ship **right** (clockwise) the given number of degrees.
>Action F means to move **forward** to the waypoint a number of times equal to the given value.
>The waypoint starts **10 units east and 1 unit north** relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.
>
>For example, using the same instructions as above:
>
>- `F10` moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
>- `N3` moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
>- `F7` moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
>- `R90` rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
>- `F11` moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
>
>After these operations, the ship's Manhattan distance from its starting position is `214 + 72` = **286**.
>
>Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?
>
>Your puzzle answer was **42013**.

I should start by mentioning that my husband completed the problem when it came out last night and told me that there wasn't much opportunity for reuse between parts 1 and 2. Obviously, I took this as a challenge.

I thought the addition of a waypoint was neat, and for my implementation, it necessitated the following changes:

1. **Update the `navigate` method to take an optional waypoint offset parameter**. For this to work, I needed to add a few `if curr_waypt:` checks in the logic to handle where the part 1 and part 2 logic deviated.
2. **Update the `if action == Commands.FORWARD:` condition to move the ship based on the waypoint** as opposed to the ship's current direction. For part 1, I had handled this by changing the `F` action to be the direction value of `curr_dir` and letting the program proceed to handle moving directions. Now, I had to write the code to actually move the ship right there and then:
```
if curr_waypt:
    delta = calculate_complex_change(curr_dir, curr_waypt)
    curr_coord = (curr_coord[0] + (value*delta[0]),curr_coord[1] + (value*delta[1]))
    continue
```
For `calculate_complex_change`, I simply modified my existing `calculate_change` method from something that only moved _one direction_ in the magnitude of _value_:
```
def calculate_change(dir,val):
    x_delta = 0
    y_delta = 0

    if dir == Directions.EAST:
        x_delta += val
    elif dir == Directions.WEST:
        x_delta -= val
    elif dir == Directions.NORTH:
        y_delta += val
    elif dir == Directions.SOUTH:
        y_delta -= val

    return (x_delta,y_delta)
```
To something that could move two directions (e.g. latitudinally and longitudinally) where `dir` represented the direction of the waypoint's coordinates relative to the normal X-Y orientation:
```
def calculate_complex_change(dir,waypoint):
    x_delta = 0
    y_delta = 0
    waypt_x = waypoint[0]
    waypt_y = waypoint[1]

    if dir == Directions.EAST:
        x_delta += waypt_y
        y_delta -= waypt_x
    elif dir == Directions.WEST:
        x_delta -= waypt_y
        y_delta += waypt_x
    elif dir == Directions.NORTH:
        x_delta += waypt_x
        y_delta += waypt_y
    elif dir == Directions.SOUTH:
        x_delta -= waypt_x
        y_delta -= waypt_y

    return (x_delta,y_delta)
```

And to make things backwards-compatible for part 1, I had `calculate_change` call `calculate_complex_code` instead of duplicating code:
```
def calculate_change(dir,val):        
    return calculate_complex_change(dir,(0,val))
```
Next, I had to...

3. **Update the N/W/S/E action-handling to move the waypoint coords instead of the ship coords.** Because my `curr_dir` variable was now storing the waypoint's orientation **_relative_ to north**, I needed to first "convert" the direction before applying the changes:
```
if curr_waypt:
    delta = calculate_change(convert_direction(curr_dir,action), value)
    curr_waypt = (curr_waypt[0] + delta[0],curr_waypt[1] + delta[1])
```
```
def convert_direction(ref_dir, target_dir):
    idx_change = (Directions.ALL.index(ref_dir) + 3)
    idx_adjusted = (Directions.ALL.index(target_dir) - idx_change) % len(Directions.ALL)
    return Directions.ALL[idx_adjusted]
```
Again, I used index-manipulation on my direction array to do these "conversions." Unfortunately, I initially used `(Directions.ALL.index(target_dir) + idx_change` instead of `(Directions.ALL.index(target_dir) - idx_change`, which led to some wasted time walking through test cases one by one to troubleshoot the mistake.

Why did I choose to use relative-orientation instead of just mutating the waypoint's coordinates on left and right turns, which would have been easier to troubleshoot?

The answer is simple: **Hubris**. 

Because of my husband's comments about little reuse and my innate contrarian personality, I wanted to minimize my code changes across parts 1 and 2, which meant I was able to leave the logic around the last action the same:

4. **Leave the `L` and `R` handling as-is**:
```
else:
    curr_dir = calculate_new_direction(curr_dir, action, value)
```

Besides a few extra print statements for debugging purposes, I had no other changes between parts 1 and 2. 😎