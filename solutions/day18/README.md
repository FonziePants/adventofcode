# [Day 18: Ticket Translation](https://adventofcode.com/2020/day/18)
>-- Day 18: Operation Order ---
>
>As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.
>
>Unfortunately, it seems like this "math" follows different rules than you remember.
>
>The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.
>
>However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.
>
>For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:
>```
>1 + 2 * 3 + 4 * 5 + 6
>  3   * 3 + 4 * 5 + 6
>      9   + 4 * 5 + 6
>         13   * 5 + 6
>             65   + 6
>                 71
>```
>Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):
>```
>1 + (2 * 3) + (4 * (5 + 6))
>1 +    6    + (4 * (5 + 6))
>     7      + (4 * (5 + 6))
>     7      + (4 *   11   )
>     7      +     44
>            51
>```
>Here are a few more examples:
>```
>2 * 3 + (4 * 5) becomes 26.
>5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
>5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
>((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
>```

I love math, so today's problem got me excited.

To read in the data, I simply read each line as a `string` and stored it in an array. 

## Part 1
>Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?
>
>Your puzzle answer was **202553439706**.

For each problem string in my problem array, I simple executed a recursive `evaluate_expression` method which does the following:

1. Starts with the following variables:
  - A `term` variable, defaulted to `None`, in which to temporarily store a numeric value
  - An `operator` variable, defaulted to `None`, in which to temporarily store a character that represents either addition or multiplication
  - An `answer` variable, initialized at `0`, in which I will keep track of the answer as I evaluation sub-expressions
  - An `i` variable, initialized at `0`, which I will use to iterate through each character in the problem
2. Iterates through each character in the problem string using a while-loop:
```
while i < len(problem):
    c = problem[i]
```
3. If the character is a digit, stores it in the `term` variable
4. Else, if the character is an operator, stores it in the `operator` variable
```
if c.isdigit():
    term = int(c)

elif c == "+":
    operator = "+"

elif c == "*":
    operator = "*"
```
5. However, if the character is an opening parenthesis, it uses an inner-loop to find the corresponding closing parenthesis, using a `p_count` variable to determine which one is "corresponding." Once it finds this closing parenthesis, it calls itself (_recursion!_) and passes the inner text in as the `problem` parameter to be evaluated, storing the value returned as the `term` and jumping the value of `i` ahead to be at the end of the closing parenthesis.
```
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
```
6. At the end of the while loop, before incrementing `i`, it checks to see if the `term` value is present. If so, it looks at the `operator` variable to see how to update `answer` accordingly, and then it resets the `term` and `operator` variables.
```
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
```

To calculate Part 1, all that's needed is to call this method on each of the problems and to sum up their returned values:
```
answer = 0
for problem in data:
    partial_answer = evaluate_expression(problem, debug)
    print(partial_answer)
    answer += partial_answer
print("Part 1: {0}\n\n".format(answer))
```

## Part 2
>--- Part Two ---
>
>You manage to answer the child's questions and they finish part 1 of their homework, but get stuck when they reach the next section: advanced math.
>
>Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.
>
>For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:
>```
>1 + 2 * 3 + 4 * 5 + 6
>  3   * 3 + 4 * 5 + 6
>  3   *   7   * 5 + 6
>  3   *   7   *  11
>     21       *  11
>         231
>```
>Here are the other examples from above:
>```
>1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
>2 * 3 + (4 * 5) becomes 46.
>5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
>5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
>((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
>```
>What do you get if you add up the results of evaluating the homework problems using these new rules?
>
>Your puzzle answer was **88534268715686**.

I decided the cleanest thing to do would be to keep my `evaluate_expression` method exactly as-is and to just add parentheses into the problem so that additions would _need_ to be executed first.

To do this, I created a recursive `add_parentheses` method that replaces all `x` characters with `+`characters once that addition sign's terms have been enclosed in parentheses. Other than that, my logic was the same as in Part 1:
```
answer = 0
for problem in data:
    problem = add_parentheses(problem.replace("+","x"),debug)
    partial_answer = evaluate_expression(problem, debug)
    print(partial_answer)
    answer += partial_answer
print("Part 2: {0}\n\n".format(answer))
```

The `add_parentheses` method, because it's recursive, begins by returning if there is no `x` to replace:
```
def add_parentheses(problem, debug):
    plus_location = problem.find("x")
    if plus_location < 0:
        return problem
```

Otherwise, it replaces the first `x` it sees in three steps:

1. **Adds an open parenthesis.** It uses an `idx` variable to track whether the index of where to place the `(` has been identified. Then, starting at the location of the `+`, it iterates through each preceding character until it finds the first term (either a number of a parentheses-pair) to which the `+` corresponds. It uses similar logic as the earlier parenthesis-matching loop to do this.
```
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
```
2. **Adds a closed parenthesis.** This does the same thing as above, but in reverse. Again, it uses an `idx` variable and a while-loop. However, this time it starts at the `+` sign and iterates through following characters until it finds the second term or it reaches the end of the problem.
```
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
```

3. **It makes this `+` as found and then recursively calls itself** to add parentheses for any remaining plus signs.
```
problem = problem[0:plus_location] + "+" + problem[plus_location+1:]

return add_parentheses(problem,debug)
```