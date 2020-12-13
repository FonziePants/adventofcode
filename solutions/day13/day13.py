def read_data(file_path,debug=True):
    file = open(file_path, "r")

    line0 = ""
    line1 = ""

    idx = 0
    for line in file:
        if not line.rstrip():
            continue
        if idx == 0:
            line0 = line.rstrip()
        else:
            line1 = line.rstrip()
        idx += 1
    
    file.close()
    
    data = (line0,line1)

    if debug:
        print(data)

    return data

def calculate_part1(data,debug=False):   
    earliest_departure_time = int(data[0])
    raw_bus_list = data[1] 

    # extract the bus list
    bus_list_str = raw_bus_list.split(",")
    bus_list = []
    for bus_str in bus_list_str:
        if bus_str == "x":
            continue
        bus_list.append(int(bus_str))
    
    time = earliest_departure_time - 1 
    next_bus = -1
    while next_bus < 0:
        time += 1
        for bus in bus_list:
            if debug:
                print("Time: {0}\nBus:  {1}\nMod:  {2}\n".format(time,bus,time % bus))
            if time % bus == 0:
                next_bus = bus
                break
    
    if debug:
        print("Time: {0}\nBus:  {1}\nWait: {2}\n".format(time,next_bus,(time - earliest_departure_time)))

    answer = bus * (time - earliest_departure_time)
    print("Part 1: {0}\n\n".format(answer))
    return answer

def calculate_part2(data,debug=False):
    print("Part 2: {0}\n\n".format("TODO"))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day13\day13.txt"
    if test:
        file_path = "solutions\day13\day13_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()