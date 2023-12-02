# --- Day 10: Adapter Array ---

def read_sorted_adapter_list(file_path,debug=True):
    file = open(file_path, "r")

    adapter_list = []

    # add in the airplane output
    adapter_list.append(0)

    for line in file:
        if not line.rstrip():
            continue
        adapter_list.append(int(line.rstrip()))
    
    file.close()

    adapter_list.sort()

    # add in your device, which will have +3 of the final adapter
    adapter_list.append(adapter_list[len(adapter_list)-1]+3)
    
    if debug:
        print("Adapters: {0}".format(adapter_list))

    return adapter_list

def count_jolt_differences(adapters,debug=False):
    diff_count = {}

    for i in range(1,len(adapters)):
        diff = adapters[i] - adapters[i-1]

        if diff in diff_count:
            diff_count[diff] = diff_count[diff] + 1
        else:
            diff_count[diff] = 1
        
        if debug:
            print("Adapters {0} (jolt-rating={1}) and {2} (jolt-rating={3}) have difference of {4}".format(i-1,adapters[i-1],i,adapters[i],adapters[i]-adapters[i-1]))

    return diff_count

def calculate_part1(diff_count,debug=False):
    if debug:
        print("Joltage differences: {0}".format(diff_count))

    #print answer
    print("Part 1: {0}".format(diff_count[1] * diff_count[3]))

    # product of 1-jolt diff count and 3-jolt diff count
    return diff_count[1] * diff_count[3]

def calculate_part2(adapters,debug=False):
    # create a map that shows from any one adapter, which possible combos there are
    # key = jolt value
    # value = jolt values of the options
    options_map = {}

    for i in range(0,len(adapters)):
        options = []

        for j in range(1,4):
            if adapters_can_connect(adapters,i,i+j):
                options.append(adapters[i+j])

        options_map[adapters[i]] = options
    
    if debug:
        print("Options map: {0}".format(options_map))
    
    # create a map that shows from any one adapter, what the downstream decision tree size is
    # key = jolt value
    # value = decision tree size
    decisions_map = {}

    decisions_map[adapters[len(adapters)-1]] = 1
    for i in reversed(range(len(adapters)-1)):
        option_sum = 0
        for option in options_map[adapters[i]]:
            option_sum += decisions_map[option]
        decisions_map[adapters[i]] = option_sum
    
    if debug:
        print("Decisions map: {0}".format(decisions_map))
    
    #print answer
    print("Part 2: {0}".format(decisions_map[adapters[0]]))

    return decisions_map[adapters[0]]

def adapters_can_connect(adapters,index1,index2):
    if index1 >= len(adapters) or index2 >= len(adapters):
        return False
    
    return (adapters[index2] - adapters[index1]) <= 3

def run_program(test=False, debug=False):
    file_path = "day10_real.txt"
    if test:
        file_path = "day10_test.txt"
    
    adapters = read_sorted_adapter_list(file_path,debug)
    jolt_diffs = count_jolt_differences(adapters,debug)
    calculate_part1(jolt_diffs,debug)
    calculate_part2(adapters,debug)

run_program(True, True)