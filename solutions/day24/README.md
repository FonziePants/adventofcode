# [Day 24: Lobby Layout](https://adventofcode.com/2020/day/24)
>--- Day 24: Lobby Layout ---
>
>Your raft makes it to the tropical island; it turns out that the small crab was an excellent navigator. You make your way to the resort.
>
>As you enter the lobby, you discover a small problem: the floor is being renovated. You can't even reach the check-in desk until they've finished installing the new tile floor.
>
>The tiles are all hexagonal; they need to be arranged in a hex grid with a very specific color pattern. Not in the mood to wait, you offer to help figure out the pattern.
>
>The tiles are all white on one side and black on the other. They start with the white side facing up. The lobby is large enough to fit whatever pattern might need to appear there.
>
>A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input). Each line in the list identifies a single tile that needs to be flipped by giving a series of steps starting from a reference tile in the very center of the room. (Every line starts from the same reference tile.)
>
>Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest, and northeast. These directions are given in your list, respectively, as e, se, sw, w, nw, and ne. A tile is identified by a series of these directions with no delimiters; for example, esenee identifies the tile you land on if you start at the reference tile and then move one tile east, one tile southeast, one tile northeast, and one tile east.
>
>Each time a tile is identified, it flips from white to black or from black to white. Tiles might be flipped more than once. For example, a line like esew flips a tile immediately adjacent to the reference tile, and a line like nwwswee flips the reference tile itself.
>
>Here is a larger example:
>```
>sesenwnenenewseeswwswswwnenewsewsw
>neeenesenwnwwswnenewnwwsewnenwseswesw
>seswneswswsenwwnwse
>nwnwneseeswswnenewneswwnewseswneseene
>swweswneswnenwsewnwneneseenw
>eesenwseswswnenwswnwnwsewwnwsene
>sewnenenenesenwsewnenwwwse
>wenwwweseeeweswwwnwwe
>wsweesenenewnwwnwsenewsenwwsesesenwne
>neeswseenwwswnwswswnw
>nenwswwsewswnenenewsenwsenwnesesenew
>enewnwewneswsewnwswenweswnenwsenwsw
>sweneswneswneneenwnewenewwneswswnese
>swwesenesewenwneswnwwneseswwne
>enesenwswwswneneswsenwnewswseenwsese
>wnwnesenesenenwwnenwsewesewsesesew
>nenewswnwewswnenesenwnesewesw
>eneswnwswnwsenenwnwnwwseeswneewsenese
>neswnwewnwnwseenwseesewsenwsweewe
>wseweeenwnesenwwwswnew
>```
>In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back to white). After all of these instructions have been followed, a total of 10 tiles are black.

Fr today's problem, I started down the wrong approach. At first, I tried to do without an exhaustive list of all tiles by defining a `HexTile` class with references to all of its adjacent tiles. Unfortunately, I had completed the constructor and business logic for this approach before realizing the error of my ways: without absolute positioning or a way to keep track of already-instantiated tiles, I would inevitably create duplicates and be unable to track flipping correctly.

So, I threw all that away and ended up with a simple `HexTile` class, a `dictionary` to track instantiated tiles (aptly called `tiles`), and a few convenience methods.

### The `HexTile` class
Just an id property that encodes it location (to guarantee uniqueness by location) and a boolean to store its color. For convenience methods, just a `flip()` method for readability and a `print()` method for debugging.

```
class HexTile:
    def __init__(self,x,y):
        self.id = get_id(x,y)
        self.white_side_up = True
    
    def flip(self):
        self.white_side_up = not self.white_side_up
    
    def print(self):
        print("TILE AT ({0}): {1}".format(self.id,"WHITE" if self.white_side_up else "BLACK"))
```

### Convenience methods
First, the coordinate methods:

- A method to convert `x,y` coordinates to a string (for use in `id`s)
    ```
    def get_id(x,y):
        return "{0},{1}".format(x,y)
    ```

- A method to convert an id string to `x,y` coordinates for iteration and neighbor-calculating purposes.
    ```
    def get_x_y(id):
        x = int(id.split(",")[0])
        y = int(id.split(",")[1])
        return (x,y)
    ```

- Next, a method to find the coordinate change for the neighbor in a specific direction. The coordinate system I used assumed that there is _never_ a tile where the x-value is even but the y-value is odd. That is, the sum of `x` and `y` for all of a tile's neighbors _always_ add up to `2`. These assumptions all me to use tiles with six neighbors in a 2-axis coordinate system.
    ```
    def get_coordinates(dir):
        x=0
        y=0

        if "e" in dir:
            x += 1
        elif "w" in dir:
            x -= 1
        
        if len(dir) == 1:
            x *= 2
        
        if "n" in dir:
            y += 1
        elif "s" in dir:
            y -= 1
        
        return (x,y)
    ```

## Part 1
>Go through the renovation crew's list and determine which tiles they need to flip. After all of the instructions have been followed, how many tiles are left with the black side up?
>
>Your puzzle answer was **459**.

### Reading the instructions

To be honest, at first I didn't bother changing the input data from a string. Rather, I navigated each partial instruction (e.g. going from `n` to `ne` on a single line) using a for-loop, a `dir` variable, and a conditional statement. If the character was `s` or `n`, I added it to `dir` and went to the next character; otherwise, I added the current character to `dir` and then executed the navigation that `dir` as a whole required.

However, because I hit a bug and separating the sub-instructions made things easier to debug, I ended up splitting the instruction lines into arrays. I knew that every direction ended in either an `e` or a `w` and so I simply split the string on these characters.

This didn't really buy me anything besides ease in debugging when trying to determine if I was reading the directions wrong (spoilers: this didn't end up being my problem). The logic is as follows:

```
def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []

    for line in file:
        if not line.rstrip():
            continue
        data.append(line.replace("e","e ").replace("w","w ").rstrip().split(" "))
    
    file.close()

    if debug:
        print(data)

    return data
```

### Reading the instructions
For each instruction, I performed the following logic:
1. Default the starting coordinate to `(0,0)`:
    ```
    for instruction in data:
        x = 0
        y = 0
    ```
2. For each direction `dir` (e.g. one of `e`, `ne`, `nw`, `w`, `sw`, or `se`) in the instruction line, I calculated the delta from my current `x,y` values and incremented accordingly:
    ```
        for dir in instruction:
            delta = get_coordinates(dir)
            x += delta[0]
            y += delta[1]
    ```
3. I calculated an `id` from the ultimate `x,y` coordinate that resulted from the above loop, added it to my `tiles` dictionary if it wasn't already there, and then flipped the tile:
    ```
        id = get_id(x,y)
        if id not in tiles:
            tiles[id] = HexTile(x,y)
        tiles[id].flip()
    ```

### Counting black tiles
To count the number of black tiles, I simply looped through each tile in my `tiles` dictionary and incremented a counter on the tile-isn't-white condition. When I saw that Part 2 likewise required the number of black tiles, I moved this logic to its own convenience method:
```
def count_black_tiles(tiles):
    black_count = 0
    for t_id in tiles:
        if not tiles[t_id].white_side_up:
            black_count += 1
    return black_count
```

Finally, calling this method resulted in the final answer:
```
black_count = count_black_tiles(tiles)
```

## Part 2
>--- Part Two ---
>
>The tile floor in the lobby is meant to be a living art exhibit. Every day, the tiles are all flipped according to the following rules:
>
>- Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
>- Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
>
>Here, tiles immediately adjacent means the six tiles directly touching the tile in question.
>
>The rules are applied simultaneously to every tile; put another way, it is first determined which tiles need to be flipped, then they are all flipped at the same time.
>
>In the above example, the number of black tiles that are facing up after the given number of days has passed is as follows:
>```
>Day 1: 15
>Day 2: 12
>Day 3: 25
>Day 4: 14
>Day 5: 23
>Day 6: 28
>Day 7: 41
>Day 8: 37
>Day 9: 49
>Day 10: 37
>
>Day 20: 132
>Day 30: 259
>Day 40: 406
>Day 50: 566
>Day 60: 788
>Day 70: 1106
>Day 80: 1373
>Day 90: 1844
>Day 100: 2208
>```
>After executing this process a total of 100 times, there would be 2208 black tiles facing up.
>
>How many tiles will be black after 100 days?
>
>Your puzzle answer was **4150**.

I thought this would be easy, but I wasted time with a couple of mistakes:
1. Instead of considering that there were neighboring white tiles not yet in my `tiles` dictionary, I first only flipped the tiles I had run across in Part 1. Obviously, this gave me the wrong result. It took creating a `print_tiles(tiles)` method (which required a `get_bounds(tiles)` method) to see the error of my ways:
    ```
    def print_tiles(tiles):
        bounds = get_bounds(tiles)
        map = []
        
        for y in list(reversed(bounds[1])):
            row = " "
            for x in bounds[0]:
                id = get_id(x,y)
                if (x+y)%2 == 1:
                    row += "  "
                elif id in tiles:
                    if tiles[id].white_side_up:
                        row += "o "
                    else:
                        row += "# "
                else:
                    row += "_ "
            map.append(row)
        
        for row in map:
            print(row)
        
        return  
    ```
    ```
    def get_bounds(tiles):
        upper_bound = 0
        lower_bound = 0
        left_bound = 0
        right_bound = 0

        map = []

        for t_id in tiles:
            coord = get_x_y(t_id)
            if coord[0] < left_bound:
                left_bound = coord[0]
            if coord[0] > right_bound:
                right_bound = coord[0]
            if coord[1] < lower_bound:
                lower_bound = coord[1]
            if coord[1] > upper_bound:
                upper_bound = coord[1]
        
        return (range(left_bound-2,right_bound+2),range(lower_bound-2,upper_bound+2))
    ```

2. When I realized I should consider _all_ of the tiles in the relevant area, I changed my iteration to go from iterating through each tile in my `tiles` dictionary to instead look at each tile in some calculated `bounds`. However, I didn't pad my bounds sufficiently (because `range()` is not inclusive on the upper bound), and found my black tile counts coming up short.

Once I fixed these two issues, my code worked as expected.

### Getting the neighbors
To calculate neighbors, I created the following method which iterates through each of the six directions and uses my `get_coordinates(dir)` method from before to calculate appropriate `x,y` deltas:
```
def get_adjacent_ids(id):
    neighbors = []

    coord = get_x_y(id)
    for dir in ["e", "ne", "nw", "w", "sw", "se"]:
        delta = get_coordinates(dir)
        neighbors.append(get_id(coord[0]+delta[0],coord[1]+delta[1]))

    return neighbors
```

### Flipping the tiles, round by round
I used a for-loop to execute the changes for each day.
```
for day in range(0,100):
```

The logic for each iteration was as follows:

1. Create a list to store the tiles which will need to be flipped:
    ```
    tiles_to_flip = []
    ```
2. After calculating the bounds of the tiles which could be flipped, iterate through each possible tile, skipping the coordinates which won't map to a tile:
    ```
    bounds = get_bounds(tiles)
    for x in bounds[0]:
        for y in bounds[1]:
            if (x+y)%2 != 0:
                continue
    ```
    In this inner loop...

    1. Get the neighbors for the tile at this position:
        ```
            t_id = get_id(x,y)
            neighbors = get_adjacent_ids(t_id)
        ```

    2. For each of these neighbors, increment the black neighbor counter (`bnc`) if the tile is in the `tiles` dictionary and does not have its white side up:
        ```
            bnc = 0
            for n_id in neighbors:
                if n_id not in tiles:
                    n_xy = get_x_y(n_id)
                elif not tiles[n_id].white_side_up:
                    bnc += 1
        ```
    3. If the tile isn't already in the dictionary, add it now, and then add it to the `tiles_to_flip` list if the right conditions are met:
        ```
            if t_id not in tiles:
                tiles[t_id] = HexTile(x,y)
            tile = tiles[t_id]
            if (    (tile.white_side_up     and bnc == 2)
                or  (not tile.white_side_up and bnc == 0)
                or  (not tile.white_side_up and bnc > 2)):
                tiles_to_flip.append(t_id)
        ```

At this point, a day is "complete" and we can actually perform the flipping. To do this, I iterated through each element in the `tiles_to_flip` array and flipped it:
```
for t_id in tiles_to_flip:
    tiles[t_id].flip()
```

The last step was to call `count_black_tiles(tiles)` one last time, and that was it!
```
black_count = count_black_tiles(tiles)
```