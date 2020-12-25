# [Day 19: Monster Messages](https://adventofcode.com/2020/day/19)
>--- Day 19: Monster Messages ---
>
>You land in an airport surrounded by dense forest. As you walk to your high-speed train, the Elves at the Mythical Information Bureau contact you again. They think their satellite has collected an image of a sea monster! Unfortunately, the connection to the satellite is having problems, and many of the messages sent back from the satellite have been corrupted.
>
>They sent you a list of the rules valid messages should obey and a list of received messages they've collected so far (your puzzle input).
>
>The rules for valid messages (the top part of your puzzle input) are numbered and build upon each other. For example:
>```
>0: 1 2
>1: "a"
>2: 1 3 | 3 1
>3: "b"
>```
>Some rules, like 3: "b", simply match a single character (in this case, b).
>
>The remaining rules list the sub-rules that must be followed; for example, the rule 0: 1 2 means that to match rule 0, the text being checked must match rule 1, and the text after the part that matched rule 1 must then match rule 2.
>
>Some of the rules have multiple lists of sub-rules separated by a pipe (|). This means that at least one list of sub-rules must match. (The ones that match might be different each time the rule is encountered.) For example, the rule 2: 1 3 | 3 1 means that to match rule 2, the text being checked must match rule 1 followed by rule 3 or it must match rule 3 followed by rule 1.
>
>Fortunately, there are no loops in the rules, so the list of possible matches will be finite. Since rule 1 matches a and rule 3 matches b, rule 2 matches either ab or ba. Therefore, rule 0 matches aab or aba.
>
>Here's a more interesting example:
>```
>0: 4 1 5
>1: 2 3 | 3 2
>2: 4 4 | 5 5
>3: 4 5 | 5 4
>4: "a"
>5: "b"
>```
>Here, because rule 4 matches a and rule 5 matches b, rule 2 matches two letters that are the same (aa or bb), and rule 3 matches two letters that are different (ab or ba).
>
>Since rule 1 matches rules 2 and 3 once each in either order, it must match two pairs of letters, one pair with matching letters and one pair with different letters. This leaves eight possibilities: aaab, aaba, bbab, bbba, abaa, abbb, baaa, or babb.
>
>Rule 0, therefore, matches a (rule 4), then any of the eight options from rule 1, then b (rule 5): aaaabb, aaabab, abbabb, abbbab, aabaab, aabbbb, abaaab, or ababbb.

I breezed through Part 1 pretty quickly because I managed to make my recursive rule interpreter with little issue (✨ _miraculously_ ✨) and I brute-forced all the _possible_ messages and just checked my message list against _that_. However, this approach didn't quite work for loopy Part 2, and I spent a not-insignificant amount of time rewriting my solution for and then troubleshooting this second part. Oy vey.

## Part 1
>The received messages (the bottom part of your puzzle input) need to be checked against the rules so you can determine which are valid and which are corrupted. Including the rules and the messages together, this might look like:
>```
>0: 4 1 5
>1: 2 3 | 3 2
>2: 4 4 | 5 5
>3: 4 5 | 5 4
>4: "a"
>5: "b"
>
>ababbb
>bababa
>abbbab
>aaabbb
>aaaabbb
>```
>Your goal is to determine the number of messages that completely match rule 0. In the above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2. The whole message must match all of rule 0; there can't be extra unmatched characters in the message. (For example, aaaabbb might appear to match rule 0 above, but it has an extra unmatched b on the end.)
>
>How many messages completely match rule 0?
>
>Your puzzle answer was **122**.

As mentioned above, I brute-forced Part 1 by enumerating all possible valid messages and then checking my input messages against those. This was done in three steps:

1. **Condensing all of the rules**, thereby eliminating all line numbers and resulting in a rule filled with `a` and `b` and logic characters.
2. **Enumerating all of the possibilities** to create one, exhaustive list of valid messages.
3. **Checking my inputs against the valid message list**.

### Condensing all of the rules
I created a recursive `condense_rule` method that took in a dictionary of the numbered rules and the number of the rule to condense. In turn, this method ultimately returned an array with all of the numbers replaced with `a` and `b` characters as well as or-operators (`|`) and arrays for sequential values and options.
```
def condense_rule(rules,r):
    rule = rules[r]
```

First of all, the method will return a string if it has been simplified into `a`,`b`, or some combination of those two characters and the pipe `|`:
```
    if len(rule) == 1 and "\"" in rule[0]:
        value = rule[0]
        return value.replace("\"","")
```

If it hasn't returned yet, then it iterates through each _part_ of the rule, where it will build out a `simplified_rule` list and flip a couple booleans as necessary.
```
    simplified_rule = []
    is_flat = True
    has_option = False
    for part in rule:
```

If the part has the or-operator, `|`, then it adds it and flips the `has_option` flag, which will tell it to return the simplified rule as part of a list.
```
        if part == "|":
            simplified_rule.append(part)
            has_option = True
```

Otherwise, it calls itself recursively. If it receives a list back instead of a string, it flips the `is_flat` flag so that it can know to convert itself to a string and just return that instead of a list.
```
        else:
            condensed_rule = condense_rule(rules,int(part))
            simplified_rule.append(condensed_rule)
            if isinstance(condensed_rule,list):
                is_flat = False
```

Lastly, `simplified_rule` is converted to a string if it has no sub-parts and then it plugs itself into a list if it has an option (for example, `aa|bb`):
```
    if is_flat:
        simplified_rule = "".join(simplified_rule) 
        if has_option:
            simplified_rule = [simplified_rule]

    return simplified_rule
```

### Enumerating all of the possibilities
I made an `enumerate_options(rule)` method which, given a rule, returns all of the possible valid messages. It does this by iterating through each rule component and slowly building out a list of messages, doubling the number with every option (that is, `|`) that it hits.

Like the `condense_rule` method, this `enumerate_options` method is recursive, exits early if it hits a flat rule, and otherwise iterates through each of the rule's parts.
```
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
```

### Checking my inputs against the valid message list
Lastly, the easiest part: call the above two methods and then just check my input messages.

To condense rule0 and enumerate all of the options:
```
rule0 = condense_rule(data[0],0)
options = enumerate_options(rule0)
```

With these, all I needed to do was to iterate through each of my messages and check to see if it existed in the options. A `matches` counter kept track of every hit.
```
matches = 0
for message in data[1]:
    if message in options:
        matches += 1
```

## Part 2
>--- Part Two ---
>
>As you look over the list of messages, you realize your matching rules aren't quite right. To fix them, completely replace rules 8: 42 and 11: 42 31 with the following:
>```
>8: 42 | 42 8
>11: 42 31 | 42 11 31
>```
>This small change has a big impact: now, the rules do contain loops, and the list of messages they could hypothetically match is infinite. You'll need to determine how these changes affect which messages are valid.
>
>Fortunately, many of the rules are unaffected by this change; it might help to start by looking at which rules always match the same set of values and how those rules (especially rules 42 and 31) are used by the new versions of rules 8 and 11.
>
>(Remember, you only need to handle the rules you have; building a solution that could handle any hypothetical combination of rules would be significantly more difficult.)
>
>For example:
>```
>42: 9 14 | 10 1
>9: 14 27 | 1 26
>10: 23 14 | 28 1
>1: "a"
>11: 42 31
>5: 1 14 | 15 1
>19: 14 1 | 14 14
>12: 24 14 | 19 1
>16: 15 1 | 14 14
>31: 14 17 | 1 13
>6: 14 14 | 1 14
>2: 1 24 | 14 4
>0: 8 11
>13: 14 3 | 1 12
>15: 1 | 14
>17: 14 2 | 1 7
>23: 25 1 | 22 14
>28: 16 1
>4: 1 1
>20: 14 14 | 1 15
>3: 5 14 | 16 1
>27: 1 6 | 14 18
>14: "b"
>21: 14 1 | 1 14
>25: 1 1 | 1 14
>22: 14 14
>8: 42
>26: 14 22 | 1 20
>18: 15 15
>7: 14 5 | 1 21
>24: 14 1
>
>abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
>bbabbbbaabaabba
>babbbbaabbbbbabbbbbbaabaaabaaa
>aaabbbbbbaaaabaababaabababbabaaabbababababaaa
>bbbbbbbaaaabbbbaaabbabaaa
>bbbababbbbaaaaaaaabbababaaababaabab
>ababaaaaaabaaab
>ababaaaaabbbaba
>baabbaaaabbaaaababbaababb
>abbbbabbbbaaaababbbbbbaaaababb
>aaaaabbaabaaaaababaa
>aaaabbaaaabbaaa
>aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
>babaaabbbaaabaababbaabababaaab
>aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
>```
>Without updating rules 8 and 11, these rules only match three messages: bbabbbbaabaabba, ababaaaaaabaaab, and ababaaaaabbbaba.
>
>However, after updating rules 8 and 11, a total of 12 messages match:
>
>- bbabbbbaabaabba
>- babbbbaabbbbbabbbbbbaabaaabaaa
>- aaabbbbbbaaaabaababaabababbabaaabbababababaaa
>- bbbbbbbaaaabbbbaaabbabaaa
>- bbbababbbbaaaaaaaabbababaaababaabab
>- ababaaaaaabaaab
>- ababaaaaabbbaba
>- baabbaaaabbaaaababbaababb
>- abbbbabbbbaaaababbbbbbaaaababb
>- aaaaabbaabaaaaababaa
>- aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
>- aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
>
>After updating rules 8 and 11, how many messages completely match rule 0?
>
>Your puzzle answer was **287**.

For this part, I needed to rewrite my solution so that instead of **enumerating all possible messages** instead it could **check a given message against the rule logic itself**.

First, I updated my `condense_rule` method to handle loops more gracefully. In the section where each part of the rule was being assessed, I added the following check to know if a rule was calling itself. In this check, it increments a counter dictionary. Because I decided that 20 recursions would probably be sufficiently high, it terminates looping at that point with a garbage character:
```
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
```

Next, I replaced by enumeration method with an `evaluate_message(rule,message)` that likewise follows the same patterns:

- Exits early with "flat" conditions
- Calls itself **recursively**
- Iterates through each "part" of the rule

Whereas the enumeration method added an option to a aggregate list with every or-operator (`|`), this evaluation method instead evaluates the options right there and then and drops any of the options (both, if necessary) that don't match the `message`. Thus, this method will return the `message` itself if the message had been valid and otherwise an empty list.
```
def evaluate_message(rule,message):
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
            options += evaluate_message(new_rule[0:bar],message)

            if "|" in new_rule[bar+1:]:
                new_rule = new_rule[bar+1:]
            else:
                options += evaluate_message(new_rule[bar+1:],message)
                break
        return options

    idx = 0
    for part in rule:
        if idx > len(message):
            return []

        if "|" in part or isinstance(part,list):
            options = evaluate_message(part,message[idx:])
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
```

Lastly, I just needed to assemble these method calls. However, this is where I got a little too clever for my own good. At first, I attempted to be savvy by condensing my rule with all up-to-20 recursive loops with logic like the following:
```
rule8 = ['42', '|', '42', '8']
rule11 = ['42', '31', '|', '42', '11', '31']
data[0][8] = rule8
data[0][11] = rule11
```

This successfully brought the valid message count in the test data from 3 to 6, but I was still missing _half_ of the valid messages. What was going on?!

After carefully making tons of minor changes to my evaluate method (including making it handle multiple `|` per part), I realized that the problem was that it would always match on the first option but didn't know how to match on several options while still iterating through the characters to match. That is, if `*b*`,`*bb*`,`*bbb*`, and `*bbbb*` were all valid because of a loop, the evaluator wouldn't be able to accurately match the second star where the shorter options had invalid suffices but the longer options had valid ones.

Consider the following valid messages where the section in parentheses indicates a loop option:

- `a(b)bba`
- `a(bb)bba`
- `a(bbb)bba`
- `a(bbbb)bba`

The string `abbbbbba`, despite being valid, would match its first four characters against the first option and then fail as "invalid" because it wrongly matched part of its loop to the `bb` part of the suffix.

It took me _hours_ to figure this out, and luckily my personal bread baker had already solved the problem and mentioned to me that he _hadn't_ condensed the loop rules in the way I had. Thinking through this difference is what ultimately spurred me to replace my overwrites:
```
rule8 = ['42', '|', '42', '8']
rule11 = ['42', '31', '|', '42', '11', '31']

data[0][8] = rule8
data[0][11] = rule11
rule0 = condense_rule(data[0],0,{})
```

...with a nested for-loop:
```
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
```

This looked messier, but at least it worked. 🤷‍♀️

And so, by reducing my loop permissability to 5-per-loop (the two loops being rule8 and rule11) and by iterating through all 25 loop options, I was able to execute the following evaluation in each one:
```
u_messages = unknown_messages.copy()
for message in unknown_messages:
    result = evaluate_message(rule0, message)
    if len(result) > 0 and result[0] == message:
        print(message)
        matches += 1
        u_messages.remove(message)
unknown_messages = u_messages
```

And at last, I was done with this headache-inducing recursive mess. 😌