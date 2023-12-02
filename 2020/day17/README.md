# [Day 17: Conway Cubes](https://adventofcode.com/2020/day/17)
>--- Day 17: Conway Cubes ---
>
>As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact you. They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.
>
>The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket dimension! When you hear it's having problems, you can't help but agree to take a look.
>
>The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.
>
>In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small flat region of cubes (your puzzle input); the cubes in this region start in the specified active (#) or inactive (.) state.
>
>The energy source then proceeds to boot up by executing six cycles.
>
>Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.
>
>During a cycle, all cubes simultaneously change their state according to the following rules:
>
>If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
>If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
>The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and determine what the configuration of cubes should be at the end of the six-cycle boot process.
>
>For example, consider the following initial state:
>```
>.#.
>..#
>###
>```
>Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)
>
>Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):
>
>After the full six-cycle boot process completes, 112 cubes are left in the active state.

This problem felt an awful lot like the seating arrangement problem from [Day 11](https://adventofcode.com/2020/day/11), but with an extra dimension. Accordingly, I planned my solution to be very similar. The main creative difference I made was to store the underlying data as booleans arrays instead of peserving the print-friendly characters.

```
for line in file:
    if not line.rstrip():
        continue
    row = []
    for cube in line.rstrip():
        if cube == Constants.inactive:
            row.append(False)
        else:
            row.append(True)
    data.append(row)
```

## Part 1
>Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?
>
>Your puzzle answer was **289**.

For this, I created an `execute_cycle` method that would return the cube configuration after a single cycle. Then, I threw this in a for-loop to run it six times.

The `execute_cycle` method did the following:

1. **Expanded the data space** to accommodate the range of cubes increasing. I created an `expand_space` method that added 2 elements for each of the array's dimensions. All values defaulted to `False` and were then overwritten by the `old_data` values.
```
def expand_space(curr_data):
    next_data = []
    for i in range(len(curr_data)+2):
        next_data_zslice = []
        for j in range(len(curr_data[0])+2):
            next_data_row = [False for k in range(len(curr_data[0][0])+2)]
            next_data_zslice.append(next_data_row)
        next_data.append(next_data_zslice)

    # overwrite middle ones with curr_data
    for z in range(len(curr_data)):
        for y in range(len(curr_data[z])):
            for x in range(len(curr_data[z][y])):
                next_data[z+1][y+1][x+1] = curr_data[z][y][x]

    return next_data
```

2. **Copied the data into a `new_data` variable** so I could continue evaluating against the prior configuration without mutating it as I went.

```
def execute_cycle(curr_data,debug):
    old_data = expand_space(curr_data)
    new_data = expand_space(curr_data)
```

3. **Updated the cube state** for each cube by looking at its state and the state of its neighbors across all three dimensions.
```
for z in range(len(old_data)):
    for y in range(len(old_data[z])):
        for x in range(len(old_data[z][y])):
            cube = old_data[z][y][x]
            active_neighbors = count_active_neighbors(old_data, z, y, x)
            if ((cube and 
                (active_neighbors < 2 or 
                active_neighbors > 3)) 
                or 
                (not cube and 
                active_neighbors == 3)):
                new_data[z][y][x] = not cube
```

The `count_active_neighbors` method used similar logic to what I used on Day 11: first, it calculated the bounds where the max-bound were +/-1 from the current cube, and then it skipped checking itself:
```
def count_active_neighbors(data, z, y, x,debug=False):
    active_neighbors = 0
    z_lower = -1 if z > 0 else 0
    z_upper = 1 if z < len(data)-1 else 0
    y_lower = -1 if y > 0 else 0
    y_upper = 1 if y < len(data[z])-1 else 0
    x_lower = -1 if x > 0 else 0
    x_upper = 1 if x < len(data[z][y])-1 else 0

    for z_delta in range(z_lower,z_upper+1):
        for y_delta in range(y_lower, y_upper+1):
            for x_delta in range(x_lower,x_upper+1):
                x2 = x + x_delta
                y2 = y + y_delta
                z2 = z + z_delta
                if (x == x2 and y == y2 and z == z2):
                    continue
                if data[z2][y2][x2]:
                    active_neighbors += 1

    return active_neighbors
```
 4. **Lastly, summed up all the active cubes** after six cycles had executed. Again, this just involved iterating through a bunch of nested loops and incrementing a counter:
 ```
 def count_active(data):
    count = 0
    for z in range(len(data)):
        for y in range(len(data[z])):
            for x in range(len(data[z][y])):
                count += 1 if data[z][y][x] else 0
    return count
 ```

## Part 2
>--- Part Two ---
>
>For some reason, your simulated results don't match what the experimental energy source engineers expected. Apparently, the pocket dimension actually has four spatial dimensions, not three.
>
>The pocket dimension contains an infinite 4-dimensional grid. At every integer 4-dimensional coordinate (x,y,z,w), there exists a single cube (really, a hypercube) which is still either active or inactive.
>
>Each cube only ever considers its neighbors: any of the 80 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3,w=4, its neighbors include the cube at x=2,y=2,z=3,w=3, the cube at x=0,y=2,z=3,w=4, and so on.
>
>The initial state of the pocket dimension still consists of a small flat region of cubes. Furthermore, the same rules for cycle updating still apply: during each cycle, consider the number of active neighbors of each cube.
>
>For example, consider the same initial state as in the example above. Even though the pocket dimension is 4-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1x1 region of the 4-dimensional space.)
>
>Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z and w coordinate:
>
>Before any cycles:
>```
>z=0, w=0
>.#.
>..#
>###
>```
>After the full six-cycle boot process completes, 848 cubes are left in the active state.
>
>Starting with your given initial configuration, simulate six cycles in a 4-dimensional space. How many cubes are left in the active state after the sixth cycle?
>
>Your puzzle answer was **2084**.

I probably could have cleaned up my solution to reuse more of part 1 and part 2. However, as I'm visiting family and would rather spend time with my in-laws, I chose to cut corners and basically duplicate the code and add an extra nexted for-loop to all my methods.

Thus, code like this:
```
for z in range(len(data)):
    for y in range(len(data[z])):
        for x in range(len(data[z][y])):
            count += 1 if data[z][y][x] else 0
```
...became code like this:
```
for w in range(len(data)):
    for z in range(len(data[w])):
        for y in range(len(data[w][z])):
            for x in range(len(data[w][z][y])):
                count += 1 if data[w][z][y][x] else 0
```

Adjusting all of my methods like this all that was needed to adapt my solution from three dimensions to four dimensions.