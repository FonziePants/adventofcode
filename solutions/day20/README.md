# [Day 20: Jurassic Jigsaw](https://adventofcode.com/2020/day/20)
>--- Day 20: Jurassic Jigsaw ---
>
>The high-speed train leaves the forest and quickly carries you south. You can even see a desert in the distance! Since you have some spare time, you might as well see if there was anything interesting in the image the Mythical Information Bureau satellite captured.
>
>After decoding the satellite messages, you discover that the data actually contains many small images created by the satellite's camera array. The camera array consists of many cameras; rather than produce a single square image, they produce many smaller square image tiles that need to be reassembled back into a single image.
>
>Each camera in the camera array returns a single monochrome image tile with a random unique ID number. The tiles (your puzzle input) arrived in a random order.
>
>Worse yet, the camera array appears to be malfunctioning: each image tile has been rotated and flipped to a random orientation. Your first task is to reassemble the original image by orienting the tiles so they fit together.
>
>To show how the tiles should be reassembled, each tile's image data includes a border that should line up exactly with its adjacent tiles. All tiles have this border, and the border lines up exactly when the tiles are both oriented correctly. Tiles at the edge of the image also have this border, but the outermost edges won't line up with any other tiles.
>
>For example, suppose you have the following nine tiles:
>```
>Tile 2311:
>..##.#..#.
>##..#.....
>#...##..#.
>####.#...#
>##.##.###.
>##...#.###
>.#.#.#..##
>..#....#..
>###...#.#.
>..###..###
>
>Tile 1951:
>#.##...##.
>#.####...#
>.....#..##
>#...######
>.##.#....#
>.###.#####
>###.##.##.
>.###....#.
>..#.#..#.#
>#...##.#..
>
>Tile 1171:
>####...##.
>#..##.#..#
>##.#..#.#.
>.###.####.
>..###.####
>.##....##.
>.#...####.
>#.##.####.
>####..#...
>.....##...
>
>Tile 1427:
>###.##.#..
>.#..#.##..
>.#.##.#..#
>#.#.#.##.#
>....#...##
>...##..##.
>...#.#####
>.#.####.#.
>..#..###.#
>..##.#..#.
>
>Tile 1489:
>##.#.#....
>..##...#..
>.##..##...
>..#...#...
>#####...#.
>#..#.#.#.#
>...#.#.#..
>##.#...##.
>..##.##.##
>###.##.#..
>
>Tile 2473:
>#....####.
>#..#.##...
>#.##..#...
>######.#.#
>.#...#.#.#
>.#########
>.###.#..#.
>########.#
>##...##.#.
>..###.#.#.
>
>Tile 2971:
>..#.#....#
>#...###...
>#.#.###...
>##.##..#..
>.#####..##
>.#..####.#
>#..#.#..#.
>..####.###
>..#.#.###.
>...#.#.#.#
>
>Tile 2729:
>...#.#.#.#
>####.#....
>..#.#.....
>....#..#.#
>.##..##.#.
>.#.####...
>####.#.#..
>##.####...
>##..#.##..
>#.##...##.
>
>Tile 3079:
>#.#.#####.
>.#..######
>..#.......
>######....
>####.#..#.
>.#...#.##.
>#.#####.##
>..#.###...
>..#.......
>..#.###...
>```
>By rotating, flipping, and rearranging them, you can find a square arrangement that causes all adjacent borders to line up:
>```
>#...##.#.. ..###..### #.#.#####.
>..#.#..#.# ###...#.#. .#..######
>.###....#. ..#....#.. ..#.......
>###.##.##. .#.#.#..## ######....
>.###.##### ##...#.### ####.#..#.
>.##.#....# ##.##.###. .#...#.##.
>#...###### ####.#...# #.#####.##
>.....#..## #...##..#. ..#.###...
>#.####...# ##..#..... ..#.......
>#.##...##. ..##.#..#. ..#.###...
>
>#.##...##. ..##.#..#. ..#.###...
>##..#.##.. ..#..###.# ##.##....#
>##.####... .#.####.#. ..#.###..#
>####.#.#.. ...#.##### ###.#..###
>.#.####... ...##..##. .######.##
>.##..##.#. ....#...## #.#.#.#...
>....#..#.# #.#.#.##.# #.###.###.
>..#.#..... .#.##.#..# #.###.##..
>####.#.... .#..#.##.. .######...
>...#.#.#.# ###.##.#.. .##...####
>
>...#.#.#.# ###.##.#.. .##...####
>..#.#.###. ..##.##.## #..#.##..#
>..####.### ##.#...##. .#.#..#.##
>#..#.#..#. ...#.#.#.. .####.###.
>.#..####.# #..#.#.#.# ####.###..
>.#####..## #####...#. .##....##.
>##.##..#.. ..#...#... .####...#.
>#.#.###... .##..##... .####.##.#
>#...###... ..##...#.. ...#..####
>..#.#....# ##.#.#.... ...##.....
>```
>For reference, the IDs of the above tiles are:
>```
>1951    2311    3079
>2729    1427    2473
>2971    1489    1171
>```
>To check that you've assembled the image correctly, multiply the IDs of the four corner tiles together. If you do this with the assembled tiles from the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.

I like the kind of logic that this puzzle requires -- that is, going through a collection of things, keeping track of matches, and then using the matches as well as the number of matches to determine the configuration.

I created a `Tile` class to:

- Store the list of edges with which to match
- Store the matches as they were found
- Make grabbing the list of matches easier (because the corners would be tiles where there were only two matches)
- Make printing the 2D map with a label easier

```
class Tile:
    def __init__(self, id, data):
        self.id = id
        self.data = data

        self.edges = [data[0]]
        left_edge = []
        right_edge = []
        for i in range(len(data)):
            left_edge.append(data[i][0])
            right_edge.append(data[i][len(data)-1])
        self.edges.append("".join(right_edge))
        self.edges.append(data[len(data)-1])
        self.edges.append("".join(left_edge))

        self.matches = [None, None, None, None]

    def get_exposed_edge_count(self):
        exposed_edge_count = 4
        for match in self.matches:
            if match:
                exposed_edge_count -= 1
        return exposed_edge_count

    def print(self):
        print("TILE {0}".format(self.id))
        for row in self.data:
            print(row)
        print()
```

In the constructor, note that the orientation of the bottom edge is right to left and the left edge is bottom to top.

Little did I know the headache that keeping track of all of these orientations, the rotations, and the flipping would cause... 

😵

## Part 1
>Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?
>
>Your puzzle answer was **83775126454273**.

Thankfully, Part 1 was easy. I brute-forced matching tiles together, not bothering to optimize against superfluous double-checks because it all required quick computations anyway.

I used a nested for loop to iterate through each pair of tiles, skipping any iterations where I would otherwise be checking a tile against itself:
```
for t1 in tiles:
    for t2 in tiles:
        if t1 == t2:
            continue
        tile1 = tiles[t1]
        tile2 = tiles[t2]
```

Then, I used another nested loop to check each tile's edge against each edge of the other tile:
```
        for e1 in range(len(tile1.edges)):
            for e2 in range(len(tile2.edges)):
```

If the edges matched (or their inverses matched), I created a "match" entry for each of the tiles. Each match was a tuple with the following data:

1. The `id` of the tile that matched the edge at the specified index
2. The index of the other tile's edge that matched
3. `True` if the edge matched exactly (which would mean one needs to be flipped) or `False` otherwise

```
                if (tile1.edges[e1] == tile2.edges[e2][::-1]):
                    tile1.matches[e1] = (t2,e2,False)
                    tile2.matches[e2] = (t1,e1,False)
                elif (tile1.edges[e1] == tile2.edges[e2]):
                    tile1.matches[e1] = (t2,e2,True)
                    tile2.matches[e2] = (t1,e1,True) 
```

Lastly, to get the product of all of the corners' IDs, I iterated through all of the tiles, multiplying IDs only if they only had two matches.

```
corners_product = 1
for t in tiles:
    edge_count = tiles[t].get_exposed_edge_count()
    if edge_count == 2:
        corners_product *= t
```

## Part 2
>--- Part Two ---
>
>Now, you're ready to check the image for sea monsters.
>
>The borders of each tile are not part of the actual image; start by removing them.
>
>In the example above, the tiles become:
>```
>.#.#..#. ##...#.# #..#####
>###....# .#....#. .#......
>##.##.## #.#.#..# #####...
>###.#### #...#.## ###.#..#
>##.#.... #.##.### #...#.##
>...##### ###.#... .#####.#
>....#..# ...##..# .#.###..
>.####... #..#.... .#......
>
>#..#.##. .#..###. #.##....
>#.####.. #.####.# .#.###..
>###.#.#. ..#.#### ##.#..##
>#.####.. ..##..## ######.#
>##..##.# ...#...# .#.#.#..
>...#..#. .#.#.##. .###.###
>.#.#.... #.##.#.. .###.##.
>###.#... #..#.##. ######..
>
>.#.#.### .##.##.# ..#.##..
>.####.## #.#...## #.#..#.#
>..#.#..# ..#.#.#. ####.###
>#..####. ..#.#.#. ###.###.
>#####..# ####...# ##....##
>#.##..#. .#...#.. ####...#
>.#.###.. ##..##.. ####.##.
>...###.. .##...#. ..#..###
>```
>Remove the gaps to form the actual image:
>```
>.#.#..#.##...#.##..#####
>###....#.#....#..#......
>##.##.###.#.#..######...
>###.#####...#.#####.#..#
>##.#....#.##.####...#.##
>...########.#....#####.#
>....#..#...##..#.#.###..
>.####...#..#.....#......
>#..#.##..#..###.#.##....
>#.####..#.####.#.#.###..
>###.#.#...#.######.#..##
>#.####....##..########.#
>##..##.#...#...#.#.#.#..
>...#..#..#.#.##..###.###
>.#.#....#.##.#...###.##.
>###.#...#..#.##.######..
>.#.#.###.##.##.#..#.##..
>.####.###.#...###.#..#.#
>..#.#..#..#.#.#.####.###
>#..####...#.#.#.###.###.
>#####..#####...###....##
>#.##..#..#...#..####...#
>.#.###..##..##..####.##.
>...###...##...#...#..###
>```
>Now, you're ready to search for sea monsters! Because your image is monochrome, a sea monster will look like this:
>```
>                  # 
>#    ##    ##    ###
> #  #  #  #  #  #   
>```
>When looking for this pattern in the image, the spaces can be anything; only the # need to match. Also, you might need to rotate or flip your image before it's oriented correctly to find sea monsters. In the above image, after flipping and rotating it to the appropriate orientation, there are two sea monsters (marked with O):
>```
>.####...#####..#...###..
>#####..#..#.#.####..#.#.
>.#.#...#.###...#.##.O#..
>#.O.##.OO#.#.OO.##.OOO##
>..#O.#O#.O##O..O.#O##.##
>...#.#..##.##...#..#..##
>#.##.#..#.#..#..##.#.#..
>.###.##.....#...###.#...
>#.####.#.#....##.#..#.#.
>##...#..#....#..#...####
>..#.##...###..#.#####..#
>....#.##.#.#####....#...
>..##.##.###.....#.##..#.
>#...#...###..####....##.
>.#.##...#.##.#.#.###...#
>#.###.#..####...##..#...
>#.###...#.##...#.##O###.
>.O##.#OO.###OO##..OOO##.
>..O#.O..O..O.#O##O##.###
>#.#..##.########..#..##.
>#.#####..#.#...##..#....
>#....##..#.#########..##
>#...#.....#..##...###.##
>#..###....##.#...##.##.#
>```
>Determine how rough the waters are in the sea monsters' habitat by counting the number of # that are not part of a sea monster. In the above example, the habitat's water roughness is 273.
>
>How many # are not part of a sea monster?
>
>Your puzzle answer was **1993**.

This part was a PITA because all of the transformations and looping required led to a lot of room for typos and bugs. 

Unfortunately, I made a lot of tiny mistakes, from forgetting to swap indices in my `matches` arrays on flipping to not accouonting for horizontal flip and vertical flips together, and much much more.

Fortunately, my landlord had already solved the problem, so I had him run his solution on my data so that I could have an accurate version of the final map against which to compare my own. Then, I committed the versions to my repo and used Github's split compare view to see which tiles were incorrectly oriented. (In hindsight, instead of committing so many garbage commits, I should have just used a branch to compare, but live and learn.) 

As I don't want to relive the hours of frustration I spent tracking down silly transformation and iteration bugs, I'll just recap the final solution here...

### Drawing and orienting a tile
Before I could build any maps, I needed to update my `Tile` class to handle:

#### Trimming the edges
```
self.data = self.data[1:len(self.data)-1]
for r in range(len(self.data)):
    self.data[r] = self.data[r][1:-1]
```

#### Orienting and finding neighbors

...in the constructor:
```
self.top_index = -1
    self.flip_h = False
    self.flip_v = False
```

...in the convenience methods:
```
def get_right_neighbor(self):
    if self.top_index < 0:
        return None
    
    index = self.top_index + 3 if self.flip_h else self.top_index + 1
    return self.matches[index%4]

def get_bottom_neighbor(self):
    if self.top_index < 0:
        return None
    
    index = self.top_index if self.flip_v else self.top_index + 2
    return self.matches[index%4]

def get_top_neighbor(self):
    if self.top_index < 0:
        return None
    
    index = self.top_index + 2 if self.flip_v else self.top_index
    return self.matches[index%4]
```

#### Flipping and rotating the map itself
```
def get_modified_data(self):
    modified_data = self.data.copy()

    rotate = (4 - self.top_index) % 4

    flip_h = self.flip_h
    flip_v = self.flip_v

    for i in range(rotate):
        modified_data = rotate_map(modified_data)

    if flip_h:
        for r in range(len(modified_data)):
            modified_data[r] = modified_data[r][::-1]
    
    if flip_v:
        modified_data = flip_map(modified_data)
    
    return modified_data
```

...where the `rotate_map` and `flip_map` were pulled into general convenience methods to also eventually be used for the constructed map in its entirety:
```
def rotate_map(map):
    new_map = []
    for c in range(0,len(map[0])):
        row = ""
        for r in reversed(range(0,len(map))):
            row += map[r][c]
        new_map.append(row)

    return new_map

def flip_map(map):
    return list(reversed(map))
```

### Assembling the map
This was the hard part.

First, for debugging purposes, I created a 2D print utility:
```
def print_2d(title,data):
    print(title)
    for row in data:
        print(row)
    print()
```

Then, I created a method that tracked the following:

- The `map` to be constructed (a 2D array of characters, or more accurately, a 1D array of strings)
- A list of `unused_tile_ids` initialized with _all_ of the tile IDs (i.e. `list(tiles.keys())`) that would be used to determine when to _stop_ constructing the map
- A list of `used_tile_ids` which was really only used for troubleshooting
- The `first_tile_in_row` which was used to retain position and orientation information when needing to begin a _new_ row
- The `current_tile` being constructed and used for map iteration

This method took in a starting corner (basically, any of the four two-matched tiles from Part 1), declared it the top-left corner, and used the indices of the two null (`None` in Python) elements in its `matches` array to determine which index corresponded to the _top_. I then stored this orientation on the instance itself. Likewise, I stored its flip state to `False` so that every other tile would be positioned and flipped _relative_ to this starting tile.
```
# get starting tile's orientation
for i in range(4):
    if not current_tile.matches[i] and not current_tile.matches[(i+3)%4]:
        current_tile.top_index = i
        current_tile.flip = False
        break
```

Then, I performed housekeeping which involved:

- Storing the initial tile in a row _section_: `row_section = current_tile.get_modified_data()`
- Removing the tile from the unused list: `unused_tile_ids.remove(current_tile.id)`
- Adding the tile to the used list: `used_tile_ids.append(current_tile.id)`

Next, I created a while loop that would run so long as there were unused tiles remaining to be added:
```
while len(unused_tile_ids) > 0:
```

Functionally, it constructed the map row by row, only pausing to create a new row when the `current_tile` at hand had no right neighbor, at which point it referred to the `first_tile_in_row` instead to find the first tile of the _next_ row:
```
    new_row = False
    flip_h = current_tile.flip_h
    flip_v = current_tile.flip_v
    match_info = current_tile.get_right_neighbor()
    if (not match_info):
        # add the row section
        for row in row_section:
            map.append(row)
        row_section = []
        flip_h = first_tile_in_row.flip_h
        flip_v = first_tile_in_row.flip_v
        # get the tile below the first tile in the row
        new_row = True
        match_info = first_tile_in_row.get_bottom_neighbor()
    
    previous_tile = current_tile
    current_tile = tiles[match_info[0]]
```

The following is where I had a number of bugs. Before _drawing_ the tile into the big map, I needed to make sure the tile was rotated and flipped _relative_ to the `previous_tile`, which involved different logic for moving right versus downward:
```
    if new_row:
        top_index = match_info[1]
        if match_info[2]:
            flip_h = not flip_h
        current_tile.flip_h = flip_h
        current_tile.top_index = (top_index)%4
    else:
        left_index = match_info[1]
        if (match_info[2] and not previous_tile.flip_h) or (not match_info[2] and previous_tile.flip_h):
            flip_v = not flip_v
        current_tile.flip_v = flip_v
        current_tile.top_index = (left_index + 1)%4

    tile_data = current_tile.get_modified_data()
```

Lastly, each while-loop's iteration drew the tile into the map at large using the `row_section` variable, and then it updated the used and unused lists accordingly:
```
    if new_row:
        row_section = tile_data
        first_tile_in_row = current_tile
    else:
        for r in range(len(row_section)):
            row_section[r] += tile_data[r]

    unused_tile_ids.remove(current_tile.id)
    used_tile_ids.append(current_tile.id)
```

After the loop completed, it added the last row and then returned the map.
```
for row in row_section:
        map.append(row)

return map
```

### Identifying the monsters
I didn't want to hard-code the monster array, so I copied the data into its own `seamonster.txt` file and created a `read_sea_monster()` utility method to read it into its own 2D array.

Then, I created a `match_monster(map, monster)` method that took a `map` and a `monster` array. This method kept a `monster_count` variable and incremented it every time a monster was found.

The logic was as follows:

1. **Iterate through each `map` character**, using the differences of the `map` and `monster` sizes as bounds:
```
for map_row in range(0,len(map)-len(monster)):
    for map_col in range(0,len(map[0])-len(monster[0])):
```

2. **Create a _copy_ of the map** so that any modifications could be reverted in the event a monster was _not_ found. Also, **default _found_monster_ to `True`** and look to _disprove_ it.
```
        new_map = map.copy()
        found_monster = True
```

3. **Iterate through each `monster` character`**:
```
        for monster_row in range(0,len(monster)):
            for monster_col in range(0,len(monster[0])):
```

4. **Only check the `#` characters**, and if the monster has one but the map does not, abort this map position check.
```
                if monster[monster_row][monster_col] != "#":
                    continue
                elif map[map_row+monster_row][map_col+monster_col] != "#":
                    found_monster = False
                    break
```
```
            if not found_monster:
                break
```
5. **Overwrite the `map` if part of the monster _was_ found**.
```
                row = map_row+monster_row
                col = map_col+monster_col
                map_string = new_map[row]
                new_map[row] = map_string[0:col] + "🐉" + map_string[col+1:]
```
6. **If `found_monster` is _still_ `True` after completion the check for that map's position, overwrite the map and increment the monster count**.
```
        if found_monster:
            map = new_map
            monster_count += 1
```

That concludes the `match_monster` check, but that isn't enough -- this method only checks for the monster at _one_ orientation, but there are _eight_ possible map orientations if you consider the four rotations and the two flip states.

Thus, to wrap up Part 2, I plugged all of the aforementioned utility methods together into the following logic:
```
map = assemble_map(tiles, data[1], debug)
monster = read_sea_monster()
monster_count = 0

for j in range(0,2):
    for i in range(0,4):
        round = match_monster(map,monster)
        map = round[0]
        monster_count += round[1]
        if debug:
            print_2d("MAP {0}".format((i+1)+(4*j)),map)
        map = rotate_map(map)
    map = flip_map(map)
```

And finally, the wave count could be calculated with a simple for-loop:
```
water_count = 0
for row in map:
    water_count += row.count("#")
```