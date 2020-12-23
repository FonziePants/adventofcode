def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []

    for line in file:
        if not line.rstrip():
            continue
        data.append(line.rstrip())
    
    file.close()

    if debug:
        print(data)

    return data

def round(data,lowest, highest):
    pickup = data[1:4]
    data = data[0] + data[4:]
    destination = int(data[0])-1

    while str(destination) not in data:
        destination -= 1
        if destination < lowest:
            destination = highest
    
    index = data.index(str(destination)) + 1
    if index >= len(data):
        data += pickup
    else:
        data = data[0:index] + pickup + data[index:]
    
    data = data[1:] + data[0]
    
    return data


def calculate_part1(data,debug=False):  
    highest = -1
    lowest = 100
    for c in data:
        n = int(c)
        if n > highest:
            highest = n
        elif n < lowest:
            lowest = n

    for i in range(100):
        print("{0}: {1}\n\n".format(i+1,data))
        data = round(data,lowest,highest)
    
    for i in range(100):
        data = data[-1:] + data[0:-1]

    print("Part 1: {0}\n\n".format(data))
    return

def calculate_part2(data,debug=False):

    print("Part 2: {0}\n\n".format("TODO"))
    return 

def run_program(test=False, debug=False):
    # file_path = "solutions\day23\day23.txt"
    # if test:
    #     file_path = "solutions\day23\day23_test.txt"
    
    # data = read_data(file_path, debug)

    data = "215694783"
    if test:
        data = "389125467"

    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()