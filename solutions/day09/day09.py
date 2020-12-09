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

def find_first_invalid_number(full_num_array, preamble):
    if len(full_num_array) < preamble:
        return None
    
    for i in range(preamble,len(full_num_array)):
        num = full_num_array[i]

        valid = False
        for j in range(i-preamble,i):
            for k in range(j+1,i):
                prev1 = full_num_array[j]
                prev2 = full_num_array[k]

                print("Checking to see if {0} is the sum of {1} and {2}".format(num,prev1,prev2))

                if num == (prev1 + prev2):
                    valid = True
                    break
            if valid:
                break
        
        if not valid:
            print("Number {0} at index {1} is NOT valid. Stop processing.".format(num, i))
            return num

        print("Number {0} at index {1} is valid. Proceed to next entry.".format(num, i))

# num_array = read_num_array("solutions\day09\day09_test.txt")
# find_first_invalid_number(num_array,5)

num_array = read_num_array("solutions\day09\day09_real.txt")
find_first_invalid_number(num_array,25)