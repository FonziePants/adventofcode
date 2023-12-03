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

def format_data(data):
    return data

def part1(commands):
    h = 0
    d = 0
    for command in commands:
        cparts = command.split(" ")
        instruction = cparts[0]
        value = int(cparts[1])

        match instruction:
            case 'forward':
                h += value
            case 'down':
                d += value
            case 'up':
                d -= value
    return h*d

def part2(commands):
    h = 0
    d = 0
    a = 0
    for command in commands:
        cparts = command.split(" ")
        instruction = cparts[0]
        value = int(cparts[1])

        match instruction:
            case 'forward':
                h += value
                d += a*value
            case 'down':
                a += value
            case 'up':
                a -= value
    return h*d

def run_program(debug=False):
    file_path = "day02.txt"
    
    data = read_data(file_path, debug)
    data = format_data(data)

    print(part1(data)) # 1693300
    print(part2(data)) # 1857958050

run_program(False)