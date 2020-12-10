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
    
    if debug:
            print("Joltage differences: {0}".format(diff_count))

    return diff_count

def calculate_part1(diff_count):
    # product of 1-jolt diff count and 3-jolt diff count
    return diff_count[1] * diff_count[3]

def run_program(test=False, debug=False):
    file_path = "solutions\day10\day10_real.txt"
    if test:
        file_path = "solutions\day10\day10_test.txt"
    
    adapters = read_sorted_adapter_list(file_path,debug)
    jolt_diffs = count_jolt_differences(adapters,debug)
    print(calculate_part1(jolt_diffs))

run_program(False, True)