def read_data(file_path,debug=True):
    file = open(file_path, "r")

    list = []

    for line in file:
        if not line.rstrip():
            continue
        list = line.rstrip().split(",")
    
    file.close()

    dict = {}
    for i in range(len(list)-1):
        num = int(list[i])
        if num not in dict:
            dict[num] = [i]
        else:
            dict[num].append(i)
        list[i] = num

    if debug:
        print(dict)

    return (int(list[len(list)-1]),dict)

def calculate_part1(data,stop,debug=False):  
    last = data[0] 
    dict = data[1]

    for idx in range(len(dict),stop-1):
        num = -1
        if last in dict:
            num = idx - dict[last][len(dict[last])-1]
            dict[last].append(idx)
        else:
            num = 0
            dict[last] = [idx]
        if debug:
            print("turn: {0}\nnum:  {1}\n".format(idx+2,num))
        last = num
        idx += 1

    print("Part 1: {0}\n\n".format(last))
    return

def calculate_part2(data,debug=False):

    print("Part 2: {0}\n\n".format("TODO"))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day15\day15.txt"
    stop = 2020
    if test:
        file_path = "solutions\day15\day15_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, stop, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()