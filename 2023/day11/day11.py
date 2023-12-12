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

class Galaxy:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return '{x},{y}'.format(x=self.x, y=self.y)

def format_data(data, distance):
    galaxies = []
    y_without = []
    x_without = []

    for y in range(0, len(data)):
        if '#' not in data[y]:
            y_without.append(y)
    
    for x in range(0, len(data[0])):
        has_galaxy = False
        for y in range(0, len(data)):
            if data[y][x] == '#':
                has_galaxy = True
                galaxies.append(Galaxy(x,y))
        if not has_galaxy:
            x_without.append(x)
    
    for galaxy in galaxies:
        y_inc = 0
        for y in y_without:
            if y < galaxy.y:
                y_inc += distance-1
        x_inc = 0
        for x in x_without:
            if x < galaxy.x:
                x_inc += distance-1
        galaxy.x += x_inc
        galaxy.y += y_inc

    return galaxies

def shortest_path(g1, g2):
    x = abs(g1.x - g2.x)
    y = abs(g1.y - g2.y)
    return x + y

def sum_paths(galaxies):
    shortest_paths = []
    for i in range(0, len(galaxies)):
        for j in range(i+1, len(galaxies)):
            shortest_paths.append(shortest_path(
                galaxies[i], 
                galaxies[j],
            ))
    return sum(shortest_paths)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day11.txt'
    
    data = read_data(file_path, debug)

    print(sum_paths(format_data(data, 2))) # 9681886
    print(sum_paths(format_data(data, 1000000))) # 791134099634

run_program(False)