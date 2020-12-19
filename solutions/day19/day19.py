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

def condense_rule(rules,r):
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
        else:
            condensed_rule = condense_rule(rules,int(part))
            simplified_rule.append(condensed_rule)
            if isinstance(condensed_rule,list):
                is_flat = False

    if is_flat:
        simplified_rule = "".join(simplified_rule) 
        if has_option:
            simplified_rule = [simplified_rule]
    
    return simplified_rule

def enumerate_options(rule):
    if len(rule) == 1 and isinstance(rule[0],str):
        if "|" in rule[0]:
            return rule[0].split("|")
        return rule
    
    if "|" in rule:
        bar = rule.index("|")
        options = enumerate_options(rule[0:bar])
        options += enumerate_options(rule[bar+1:])
        return options

    options = [""]

    for part in rule:
        if "|" in part or isinstance(part,list):
            suboptions = enumerate_options(part)
            new_options = []
            for option in options:
                for suboption in suboptions:
                    new_options.append(option + suboption)
            options = new_options
        else:
            new_options = []
            for option in options:
                new_options.append(option + part)
            options = new_options
    return options

def calculate_part1(data,debug=False):   
    rule0 = condense_rule(data[0],0)
    options = enumerate_options(rule0)

    if debug:
        print("Rule 0: {0}".format(rule0))
        print("Options:")
        for option in options:
            print("  {0}".format(option))

    matches = 0
    round = 0
    for message in data[1]:
        round += 1
        print("Round {0}".format(round))
        if message in options:
            matches += 1

    print("Part 1: {0}\n\n".format(matches))
    return

def calculate_part2(data,debug=False):

    print("Part 2: {0}\n\n".format("TODO"))
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