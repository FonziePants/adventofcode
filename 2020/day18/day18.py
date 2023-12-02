def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []

    for line in file:
        if not line.rstrip():
            continue
        data.append(line.rstrip().replace(" ",""))
    
    file.close()

    if debug:
        print(data)

    return data

def evaluate_expression(problem, debug):
    if debug:
        print("Solving: {0}".format(problem))

    term = None
    operator = None
    answer = 0
    i = 0
    while i < len(problem):
        c = problem[i]
        if c.isdigit():
            term = int(c)
        
        elif c == "+":
            operator = "+"

        elif c == "*":
            operator = "*"

        elif c == "(":
            p_count = 1
            j = i+1
            while j < len(problem):
                c2 = problem[j]
                if c2 == "(":
                    p_count += 1
                elif c2 == ")":
                    p_count -= 1
                if p_count == 0:
                    term = evaluate_expression(problem[i+1:j],debug)
                    i = j
                    break
                j += 1

        if term:
            if not operator:
                answer = term
            elif operator == "+":
                answer += term
            else:
                answer *= term
            term = None
            operator = None

        i += 1

    return answer

def add_parentheses(problem, debug):
    plus_location = problem.find("x")
    if plus_location < 0:
        return problem

    if debug:
        print("BEFORE:  " + problem)

    # add open parenthesis
    i = plus_location
    idx = None
    while i >= 0 and not idx:
        c = problem[i]
        if c.isdigit():
            idx = i
        elif c == ")":
            p_count = 1
            j = i-1
            while j >= 0:
                c2 = problem[j]
                if c2 == ")":
                    p_count += 1
                elif c2 == "(":
                    p_count -= 1
                if p_count == 0:
                    idx = j
                    break
                j -= 1
        i -= 1
    if not idx:
        problem = "(" + problem
    else:
        problem = problem[0:idx] + "(" + problem[idx:]
    plus_location += 1
    
    # add close parenthesis
    i = plus_location
    idx = None
    while i < len(problem) and not idx:
        c = problem[i]
        if c.isdigit():
            idx = i
        elif c == "(":
            p_count = 1
            j = i+1
            while j < len(problem):
                c2 = problem[j]
                if c2 == "(":
                    p_count += 1
                elif c2 == ")":
                    p_count -= 1
                if p_count == 0:
                    idx = j
                    break
                j += 1
        i += 1
    if not idx:
        problem = problem + ")"
    else:
        problem = problem[0:idx+1] + ")" + problem[idx+1:]

    problem = problem[0:plus_location] + "+" + problem[plus_location+1:]

    if debug:
        print("AFTER:  " + problem)

    return add_parentheses(problem,debug)

def calculate_part1(data,debug=False):   
    answer = 0
    for problem in data:
        partial_answer = evaluate_expression(problem, debug)
        print(partial_answer)
        answer += partial_answer
    print("Part 1: {0}\n\n".format(answer))
    return

def calculate_part2(data,debug=False):
    answer = 0
    for problem in data:
        problem = add_parentheses(problem.replace("+","x"),debug)
        partial_answer = evaluate_expression(problem, debug)
        print(partial_answer)
        answer += partial_answer
    print("Part 2: {0}\n\n".format(answer))
    return 

def run_program(test=False, debug=False):
    file_path = "day18.txt"
    if test:
        file_path = "day18_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, debug)
    calculate_part2(data, debug)

run_program(True, True)
run_program()