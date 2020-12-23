
def read_data(file_path,debug=True):
    file = open(file_path, "r")

    rules = {}
    messages = []

    for line in file:
        if not line.rstrip():
            continue

        if ":" in line:
            halves = line.rstrip().split(": ")
            rules[int(halves[0])] = halves[1].split(" ")
        else:
            messages.append(line.rstrip())
    
    file.close()

    data = (rules, messages)

    if debug:
        print(data)

    return data

def condense_rule(rules,r,counters):
    rule = rules[r]

    if len(rule) == 1 and "\"" in rule[0]:
        value = rule[0]
        return value.replace("\"","")

    simplified_rule = []
    is_flat = True
    has_option = False
    for part in rule:
        if part == "|":
            simplified_rule.append(part)
            has_option = True
            continue

        # check for loops
        if r == int(part):
            if r not in counters: 
                counters[r] = 1
            else:
                counters[r] += 1

            # skip it if we're already deep
            if counters[r] > 20:
                simplified_rule.append("⛔")
                continue
                
        condensed_rule = condense_rule(rules,int(part),counters)
        simplified_rule.append(condensed_rule)
        if isinstance(condensed_rule,list):
            is_flat = False

    if is_flat:
        simplified_rule = "".join(simplified_rule) 
        if has_option:
            simplified_rule = [simplified_rule]
    
    return simplified_rule

def evaluate_message(rule,message,full):
    if len(rule) == 1 and isinstance(rule[0],str) and "|" in rule[0]:
        parts = rule[0].split("|")
        options = []
        for part in parts:
            if len(part) <= len(message) and part == message[:len(part)]:
                if len(options) > 0:
                    options.append("|")
                    options.append(part)
                else:
                    options.append(part)
        return options
    
    if "|" in rule:
        options = []
        new_rule = rule.copy()
        while True:
            bar = new_rule.index("|")
            options += evaluate_message(new_rule[0:bar],message,message)

            if "|" in new_rule[bar+1:]:
                new_rule = new_rule[bar+1:]
            else:
                options += evaluate_message(new_rule[bar+1:],message,message)
                break
        return options

    idx = 0
    for part in rule:
        if idx > len(message):
            return []

        if "|" in part or isinstance(part,list):
            options = evaluate_message(part,message[idx:],message)
            if len(options) == 0:
                return options
            else:
                part = options[0]

        if len(part) <= len(message[idx:]):
            if part != message[idx:idx+len(part)]:
                return []
            idx += len(part)
        else:
            return []

    return [message[:idx]]

def calculate_part1(data,debug=False):   
    rule0 = condense_rule(data[0],0,{})

    matches = 0
    for message in data[1]:
        result = evaluate_message(rule0, message, message)
        if len(result) > 0 and result[0] == message:
            print(message)
            matches += 1

    print("Part 1: {0}\n\n".format(matches))

def calculate_part2(data,debug=False):
    matches = 0
    unknown_messages = data[1].copy()
    for i8 in range(5):
        for i11 in range(5):
            rule8 = ['42']
            rule11 = ['42', '31']
            for j8 in range(i8):
                rule8.append('42')
            for j11 in range(i11):
                rule11 = ['42'] + rule11 + ['31']
            data[0][8] = rule8
            data[0][11] = rule11

            rule0 = condense_rule(data[0],0,{})
            u_messages = unknown_messages.copy()
            for message in unknown_messages:
                result = evaluate_message(rule0, message, message)
                if len(result) > 0 and result[0] == message:
                    print(message)
                    matches += 1
                    u_messages.remove(message)
            unknown_messages = u_messages
    
    print("Part 2: {0}\n\n".format(matches))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day19\day19.txt"
    if test:
        file_path = "solutions\day19\day19_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()