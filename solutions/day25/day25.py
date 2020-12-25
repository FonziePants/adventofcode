def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []

    for line in file:
        if not line.rstrip():
            continue
        data.append(int(line.rstrip()))
    
    file.close()

    if debug:
        print(data)

    return data

def transform_subject_number(loop_size, subject_number):
    value = 1
    for loop in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value

def find_secret_loop_size(public_key, subject_number):
    value = 1
    loop = 0
    while value != public_key:
        loop += 1
        value *= subject_number
        value %= 20201227
    return loop

def calculate_encryption_key(device_1_public_key,device_2_loop_size):
    return transform_subject_number(device_2_loop_size,device_1_public_key)

def run_program(test=False, debug=False):
    file_path = "solutions\day25\day25.txt"
    if test:
        file_path = "solutions\day25\day25_test.txt"
    
    data = read_data(file_path, debug)

    pk1 = data[0]
    pk2 = data[1]

    ls2 = find_secret_loop_size(pk2,7)

    ek = calculate_encryption_key(pk1,ls2)

    print("Encryption Key: {0}\n\n".format(ek))

# run_program(True, True)
run_program()