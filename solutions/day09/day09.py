# --- Day 9: Encoding Error ---
def read_num_array(file_path):
    file = open(file_path, "r")

    num_array = []

    for line in file:
        if not line.rstrip():
            continue

        num_array.append(int(line.rstrip()))
    
    file.close()

    return num_array

def find_first_invalid_number(full_num_array, preamble, debug=False):
    if len(full_num_array) < preamble:
        return None
    
    for i in range(preamble,len(full_num_array)):
        num = full_num_array[i]

        valid = False
        for j in range(i-preamble,i):
            for k in range(j+1,i):
                prev1 = full_num_array[j]
                prev2 = full_num_array[k]

                if debug:
                    print("Checking to see if {0} is the sum of {1} and {2}".format(num,prev1,prev2))

                if num == (prev1 + prev2):
                    valid = True
                    break
            if valid:
                break
        
        if not valid:
            print("Number {0} at index {1} is NOT valid. Stop processing.".format(num, i))
            return i #index of num

        if debug:
            print("Number {0} at index {1} is valid. Proceed to next entry.".format(num, i))

def find_contiguous_set_of_addends(full_num_array,index_of_num,debug=False):
    num_array_subset = full_num_array[:index_of_num]
    sum_target = full_num_array[index_of_num]

    # iterate through all the possible starting numbers
    for start in range(len(num_array_subset)):

        # iterate through all the possible sequence lengths
        for stop in range(start+1,len(num_array_subset)):

            sum = 0
            highest_num = 0
            lowest_num = sum_target * 10000
            for i in range(start,stop+1): #stop+1 makes it inclusive
                num = num_array_subset[i]
                sum += num

                if num > highest_num:
                    highest_num = num
                
                if num < lowest_num:
                    lowest_num = num
            
            if debug:
                print("Sum of values between index {0} (value = {1}) and index {2} (value = {3}) is {4}.".format(start,num_array_subset[start],stop,num_array_subset[stop],sum))
            
            if sum == sum_target:
                encryption_weakness = highest_num + lowest_num
                print("Sequence found! Terminate program. Encryption weakness = {0}".format(encryption_weakness))
                return encryption_weakness
    
    return -1

def run_program(test_data=False,debug=False):
    file_path = "solutions\day09\day09_real.txt"
    preamble = 25

    if test_data:
        file_path = "solutions\day09\day09_test.txt"
        preamble = 5
    
    num_array = read_num_array(file_path)
    index_of_invalid_num = find_first_invalid_number(num_array,preamble,debug)
    find_contiguous_set_of_addends(num_array, index_of_invalid_num,debug)

run_program()