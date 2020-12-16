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
        dict[num] = i
        list[i] = num
    list[len(list)-1] = int(list[len(list)-1])

    if debug:
        print(dict)

    return (list,dict)

def calculate(data,stop,part,debug=False):  
    list = data[0] 
    last = list[len(list)-1]
    dict = data[1]

    for idx in range(len(dict),stop-1):
        num = -1
        if last in dict:
            num = idx - dict[last]
        else:
            num = 0
        dict[last] = idx
        list.append(last)
        if debug:
            print("turn: {0}\nnum:  {1}\n".format(idx+2,num))
        last = num
        idx += 1

    print(list[len(list)-10:])
    print("Part {0}: {1}\n\n".format(part,last))
    return

def run_program(part2,test=False, debug=False):
    file_path = "solutions\day15\day15.txt"
    stop = 2020
    part = 1
    if test:
        file_path = "solutions\day15\day15_test.txt"
    if part2:
        stop = 30000000
        part = 2
    
    data = read_data(file_path, debug)

    calculate(data, stop, part, debug)

run_program(True)