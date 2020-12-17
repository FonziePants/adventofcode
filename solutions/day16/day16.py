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

def print_valid_values(valid_values):
    print("VALID VALUES:")
    for value in valid_values:
        print("{0}: {1}".format(value, valid_values[value]))

def remove_field(valid_values, field):
    for value in valid_values:
        if field in valid_values[value]:
            valid_values[value].remove(field)
    return valid_values

def discard_invalid_tickets(data,debug=False):   
    fields = data[0]
    tickets = data[1]
    valid_values = {}
    valid_tickets = []
    
    for field in fields:
        for value in field.values:
            if value in valid_values:
                valid_values[value].append(field.name)
            else:
                valid_values[value] = [field.name]
    
    if debug:
        print_valid_values(valid_values)
    
    error_rate = 0
    for ticket in tickets:
        valid = True
        for value in ticket:
            if value not in valid_values:
                if debug:
                    print("{0} not found".format(value))
                error_rate += value
                valid = False
        if valid:
            valid_tickets.append(ticket)
    
    print("Part 1: {0}\n\n".format(error_rate))
    return (fields,valid_tickets,valid_values)

def determine_fields(data,debug=False):
    fields = data[0]
    tickets = data[1]
    valid_values = data[2]

    # create field indices array defaulted to false
    field_indices = []
    for i in range(len(fields)):
        field_indices.append(False)

    while False in field_indices:
        # go through each field position
        for i in range(len(field_indices)):
            # get that field position's value for each ticket
            values = []
            for ticket in tickets:
                if ticket[i] not in values:
                    values.append(ticket[i])
            # list out possible fields based on the value
            possible_fields = valid_values[values[0]].copy()
            # rule out fields by looking at all the other tickets
            for j in range(1,len(values)):
                for field in possible_fields:
                    if field not in valid_values[values[j]]:
                        possible_fields.remove(field)
            # if we found the field, remove it from options for other indices
            if len(possible_fields) == 1:
                field = possible_fields[0]
                field_indices[i] = field
                remove_field(valid_values,field)

    if debug:
        print(field_indices)

    # multiply values of departure fields
    answer = 1
    for i in range(len(field_indices)):
        if "departure" in field_indices[i]:
            answer *= tickets[0][i]

    print("Part 2: {0}\n\n".format(answer))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day16\day16.txt"
    if test:
        file_path = "solutions\day16\day16_test.txt"
    
    data = read_data(file_path, debug)

    # PART 1
    data2 = discard_invalid_tickets(data, debug)

    # PART 2
    determine_fields(data2, debug)

# run_program(True, True)
run_program(False, False)