class Field:
    def __init__(self, line):
        parts = line.split(": ")
        self.name = parts[0]
        self.values = []
        value_ranges = parts[1].split(" or ")
        for value_range in value_ranges:
            halves = value_range.split("-")
            for i in range(int(halves[0]),int(halves[1])+1):
                self.values.append(i)
    def print(self):
        print("Field '{0}' has possible values: {1}".format(self.name,self.values))

def read_data(file_path,debug=True):
    file = open(file_path, "r")

    fields = []
    tickets = []

    parsing_own_ticket = False
    parsing_tickets = False
    for line in file:
        if not line.rstrip():
            continue

        if parsing_tickets:
            if "," not in line:
                continue
            ticket = [int(val) for val in line.rstrip().split(",")]
            tickets.append(ticket)
        elif "ticket" in line:
            parsing_tickets = True
        else:
            field = Field(line)
            fields.append(field)
    
    file.close()

    if debug:
        for field in fields:
            field.print()
        print("\nTICKETS:")
        for ticket in tickets:
            print(ticket)
        print("\n")

    return (fields, tickets)

def calculate_part1(data,debug=False):   
    fields = data[0]
    tickets = data[1]
    valid_values = {}
    
    for field in fields:
        for value in field.values:
            if value in valid_values:
                valid_values[value].append(field.name)
            else:
                valid_values[value] = [field.name]
    
    if debug:
        print("VALID VALUES:")
        for value in valid_values:
            print("{0}: {1}".format(value, valid_values[value]))
    
    error_rate = 0
    for ticket in tickets:
        for value in ticket:
            if value not in valid_values:
                if debug:
                    print("{0} not found".format(value))
                error_rate += value
    
    print("Part 1: {0}\n\n".format(error_rate))
    return error_rate

def calculate_part2(data,debug=False):

    print("Part 2: {0}\n\n".format("TODO"))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day16\day16.txt"
    if test:
        file_path = "solutions\day16\day16_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()