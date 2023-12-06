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
    return data[0]

def is_marker(marker, marker_length):
    if len(marker) != marker_length:
        return False
    for i in range(0,marker_length-1):
        for j in range(i+1,marker_length):
            if marker[i] == marker[j]:
                return False
    return True

def find_first_marker(buffer, length):
    i = length
    while i <= len(buffer):
        if is_marker(buffer[i-length:i], length):
            break
        i+=1
    return i

def part1(buffer):
    return find_first_marker(buffer, 4)

def part2(buffer):
    return find_first_marker(buffer, 14)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day06.txt'
    
    buffer = read_data(file_path, debug)

    print(part1(buffer)) # 1093
    print(part2(buffer)) # 3534

run_program(False)