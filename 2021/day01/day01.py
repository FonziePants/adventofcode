def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        if not line.rstrip():
            continue
        sline = line.rstrip()
        data.append(int(sline))
        
    file.close()
    if debug: print(data)
    return data

def format_data(data):
    return data

def part1(readings):
    larger_readings = 0
    past_depth = None
    for depth in readings:
        if past_depth is not None and past_depth < depth:
            larger_readings += 1
        past_depth = depth
    return larger_readings

def part2(readings):
    larger_readings = 0
    for i in range(3, len(readings)):
        if readings[i] > readings[i-3]:
            larger_readings += 1
    return larger_readings

def run_program(debug=False):
    file_path = "day01.txt"
    
    data = read_data(file_path, debug)
    data = format_data(data)

    print(part1(data)) # 1215
    print(part2(data)) # 1150

run_program(False)