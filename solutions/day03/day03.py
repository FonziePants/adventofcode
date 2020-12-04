# --- Day 3: Toboggan Trajectory ---
# With the toboggan login problems resolved, you set off toward the airport. While travel by toboggan might be easy, it's certainly not safe: there's very minimal steering and the area is covered in trees. You'll need to see which angles will take you near the fewest trees.

# Due to the local geology, trees in this area only grow on exact integer coordinates in a grid. You make a map (your puzzle input) of the open squares (.) and trees (#) you can see. For example:

# ..##.......
# #...#...#..
# .#....#..#.
# ..#.#...#.#
# .#...##..#.
# ..#.##.....
# .#.#.#....#
# .#........#
# #.##...#...
# #...##....#
# .#..#...#.#
# These aren't the only trees, though; due to something you read about once involving arboreal genetics and biome stability, the same pattern repeats to the right many times:

# ..##.........##.........##.........##.........##.........##.......  --->
# #...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
# .#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
# ..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
# .#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
# ..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
# .#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
# .#........#.#........#.#........#.#........#.#........#.#........#
# #.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
# #...##....##...##....##...##....##...##....##...##....##...##....#
# .#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on your map).

# The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers); start by counting all the trees you would encounter for the slope right 3, down 1:

# From your starting position at the top-left, check the position that is right 3 and down 1. Then, check the position that is right 3 and down 1 from there, and so on until you go past the bottom of the map.

# The locations you'd check in the above example are marked here with O where there was an open square and X where there was a tree:

# ..##.........##.........##.........##.........##.........##.......  --->
# #..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
# .#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
# ..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
# .#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
# ..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
# .#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
# .#........#.#........X.#........#.#........#.#........#.#........#
# #.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
# #...##....##...##....##...#X....##...##....##...##....##...##....#
# .#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# In this example, traversing the map using this slope would cause you to encounter 7 trees.

# Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?

class Constants:
    C_TREE = "#"
    C_OPEN = "."
    C_HIT = "X"
    C_MISS = "O"
    TEST_FILE = "solutions\day03\day03_test.txt"
    REAL_FILE = "solutions\day03\day03.txt"


class TreeMap:
    def __init__(self, tree_map, width, height):
        # default values
        self.map = tree_map
        self.width = width
        self.height = height
    
    def print(self):
        for index in range(len(self.map)):
            print(self.map[index])
    
    def pretty_print(self, desired_width):
        if desired_width < self.width:
            desired_width = self.width

        for row in range(len(self.map)):
            strip = ""
            for col in range(desired_width):
                strip += Constants.C_TREE if self.map[row][col%self.width] else Constants.C_OPEN
            print(strip)
    
    def count_trees(self, x_delta, y_delta):
        tree_count = 0
        x = 0
        y = 0
        
        while (y < len(self.map)):
            # make sure we don't go out of bounds
            x = x % self.width
            
            if self.map[y][x]:
                tree_count += 1
            
            x += x_delta
            y += y_delta
        
        return tree_count
    
    def count_trees_debug(self, x_delta, y_delta, desired_width):
        tree_count = 0
        x = 0
        y = 0

        if desired_width < self.width:
            desired_width = self.width

        for row in range(len(self.map)):
            strip = ""
            for col in range(desired_width):
                if y == row and x == col%self.width:
                    strip += Constants.C_HIT if self.map[row][col%(self.width)] else Constants.C_MISS

                    x += x_delta
                    x %= self.width
                    y += y_delta

                    if self.map[row][col%self.width]:
                        tree_count += 1
                else:
                    strip += Constants.C_TREE if self.map[row][col%self.width] else Constants.C_OPEN
            print(strip)
        
        print(str(tree_count))
    
    def print_tree_count(self, x_delta, y_delta):
        trees_hit = self.count_trees(x_delta, y_delta)
        print(trees_hit)
        return trees_hit

def create_2d_map(input_file):
    # open file
    file = open(input_file, "r")

    # create password list line by line
    tree_map = []
    max_width = 0
    row = 0

    for line in file:
        line = line.rstrip()
        line_length = len(line)

        # assumption: all lines will have the same line length,
        # so this will only enter once
        if line_length > max_width:
            max_width = line_length

        map_row = [False for i in range(max_width)]
        for index in range(line_length):
            c = line[index]
            if c == Constants.C_TREE:
                map_row[index] = True
        
        tree_map.append(map_row)
        row += 1
    
    file.close()
    
    return TreeMap(tree_map, max_width, row)

# tree_map = create_2d_map(Constants.TEST_FILE)
tree_map = create_2d_map(Constants.REAL_FILE)
# tree_map.count_trees_debug(3,1,0)
opt1 = tree_map.print_tree_count(1,1)
opt2 = tree_map.print_tree_count(3,1)
opt3 = tree_map.print_tree_count(5,1)
opt4 = tree_map.print_tree_count(7,1)
opt5 = tree_map.print_tree_count(1,2)

print("product of trees hit on all slopes: " + str(opt1*opt2*opt3*opt4*opt5))