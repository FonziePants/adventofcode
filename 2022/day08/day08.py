def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        if not line.rstrip():
            continue
        sline = line.rstrip()
        data.append(sline)
        
    file.close()
    if debug: print(data)
    return data

def print_forest(forest):
    for row in forest: print(''.join([str(tree.height) for tree in row]))

def print_forest_visibility(forest):
    for row in forest: print(''.join(['V' if tree.is_visible() else ' ' for tree in row]))

def print_forest_scenery(forest):
    for row in forest: print(''.join(['{:02d} '.format(tree.scenic_score()) for tree in row]))

class Tree:
    def __init__(self, height, x, y) -> None:
        self.height = int(height)
        self.x = x
        self.y = y

        self.highest_t = None
        self.highest_b = None
        self.highest_l = None
        self.highest_r = None

        self.scenery_t = 0
        self.scenery_b = 0
        self.scenery_l = 0
        self.scenery_r = 0
    
    def __repr__(self) -> str:
        return '({x},{y})={h}'.format(x=self.x,y=self.y,h=self.height)
    
    def is_visible(self):
        return (
            self.highest_t is None or 
            self.height > self.highest_t.height or
            self.highest_b is None or 
            self.height > self.highest_b.height or
            self.highest_l is None or 
            self.height > self.highest_l.height or
            self.highest_r is None or 
            self.height > self.highest_r.height
        )
    
    def scenic_score(self):
        return self.scenery_t * self.scenery_b * self.scenery_l * self.scenery_r

def format_data(data):
    forest = []
    y = 0
    for row in data:
        tree_row = []
        x = 0
        for tree in row:
            tree_row.append(Tree(tree, x, y))
            x += 1
        forest.append(tree_row)
        y += 1
    
    h = len(forest)
    w = len(forest[0])
    
    for x in range(0, w):
        for y in range(0, h):
            if y == 0:
                forest[y][x].highest_t = None
                forest[h-y-1][w-x-1].highest_b = None
            else:
                if forest[y-1][x].highest_t is not None and forest[y-1][x].highest_t.height >= forest[y-1][x].height:
                    forest[y][x].highest_t = forest[y-1][x].highest_t
                else:
                    forest[y][x].highest_t = forest[y-1][x]
                if forest[h-y][w-x-1].highest_b is not None and forest[h-y][w-x-1].highest_b.height >= forest[h-y][w-x-1].height:
                    forest[h-y-1][w-x-1].highest_b = forest[h-y][w-x-1].highest_b
                else:
                    forest[h-y-1][w-x-1].highest_b = forest[h-y][w-x-1]
            if x == 0:
                forest[y][x].highest_l = None
                forest[h-y-1][w-x-1].highest_r
            else:
                if forest[y][x-1].highest_l is not None and forest[y][x-1].highest_l.height >= forest[y][x-1].height:
                    forest[y][x].highest_l = forest[y][x-1].highest_l
                else:
                    forest[y][x].highest_l = forest[y][x-1]
                if forest[h-y-1][w-x].highest_r is not None and forest[h-y-1][w-x].highest_r.height >= forest[h-y-1][w-x].height:
                    forest[h-y-1][w-x-1].highest_r = forest[h-y-1][w-x].highest_r
                else:
                    forest[h-y-1][w-x-1].highest_r = forest[h-y-1][w-x]

    for y in range(1, h-1):
        for x in range(1, w-1):
            tree = forest[y][x]
            # top
            t_tree = forest[y-1][x]
            while t_tree.y > 0:
                if t_tree.height >= tree.height:
                    break
                else:
                    t_tree = forest[t_tree.y-1][x]
            tree.scenery_t = y-t_tree.y

            # left
            l_tree = forest[y][x-1]
            while l_tree.x > 0:
                if l_tree.height >= tree.height:
                    break
                else:
                    l_tree = forest[y][l_tree.x-1]
            tree.scenery_l = x-l_tree.x

            # bottom
            b_tree = forest[y+1][x]
            while b_tree.y+1 < h:
                if b_tree.height >= tree.height:
                    break
                else:
                    b_tree = forest[b_tree.y+1][x]
            tree.scenery_b = b_tree.y-y

            # right
            r_tree = forest[y][x+1]
            while r_tree.x+1 < w:
                if r_tree.height >= tree.height:
                    break
                else:
                    r_tree = forest[y][r_tree.x+1]
            tree.scenery_r = r_tree.x-x

    return forest

def part1(forest):
    visible_trees = 0
    for row in forest:
        for tree in row:
            visible_trees += 1 if tree.is_visible() else 0
    return visible_trees

def part2(forest):
    max_scenic_score = 0
    for row in forest:
        max_scenic_score = max(max_scenic_score, max(tree.scenic_score() for tree in row))
    return max_scenic_score

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day08.txt'
    
    data = read_data(file_path, debug)
    forest = format_data(data)

    if debug: print_forest(forest)
    if debug: print_forest_visibility(forest)
    if debug: print_forest_scenery(forest)

    print(part1(forest)) # 1543
    print(part2(forest)) # 595080

run_program(False)