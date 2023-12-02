# [Day 6: Custom Customs](https://adventofcode.com/2020/day/6)
>--- Day 6: Custom Customs ---
>
>As your flight approaches the regional airport where you'll switch to a much larger plane, customs declaration forms are distributed to the passengers.
>
>The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.
>
>However, the person sitting next to you seems to be experiencing a language barrier and asks if you can help. For each of the people in their group, you write down the questions for which they answer "yes", one per line. For example:
>```
>abcx
>abcy
>abcz
>```
>In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the same question don't count extra; each question counts at most once.)
>Another group asks for your help, then another, and eventually you've collected answers from every group on the plane (your puzzle input). Each group's answers are separated by a blank line, and within each group, each person's answers are on a single line. For example:
>```
>abc
>
>a
>b
>c
>
>ab
>ac
>
>a
>a
>a
>a
>
>b
>```
>This list represents answers from five groups:
>
>- The first group contains one person who answered "yes" to 3 questions: a, b, and c.
>- The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
>- The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
>- The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
>- The last group contains one person who answered "yes" to only 1 question, b.

The approach I've started to take is to begin implementation before fully reading the question. Specifically, I read enough of the problem to understand **what kind of data structure I would need to be able to store and extensibly manipulate the input data** and then I create a class (or group of classes) with a constructor and a print statement.

While this approach has slowed me down for Part 1 because I am sometimes storing more information (and therefore writing more code) than the question requires, it has helped me breeze through Part 2 on a few occasions, including today. For today's problem, my husband edged me out on Part 1 by a couple minutes and then I returned the favor for Part 2. 😈

Today, I chose to create a class to represent a single group's set of answers, which turned out to just be a glorified wrapper on a dictionary where letter characters were the keys and integer yes-counts were the values. However, the benefit of wrapping this native data structure in a class is that it makes it easier for me to write helper methods on it. To instantiate this class, I did the following:

- Took in a list of strings, where each string represented an individual's answers in the group
- Instantiated an empty dictionary
- Iterated through each string in the list, and for each character, I added it to the dictionary if it wasn't already present or otherwise incremented the value already in the dictionary

Thus, I ended up with a dictionary that only had keys present if someone in the group had answered yes on it and where the value was the number of yes responses for that specific question in the group. Additionally, in the event I would later want to examine specific sets of answers, I also stored the original string list as a property on the class.

My rationale for using the dictionary data structure was as follows:
- Quick lookup (yay, performance!)
- No need to sort answers -- uniqueness and matching are built-in
- Flexible value types -- had I just made a list of keys for which there was a yes answer, I'd lose data (i.e. how many yeses), and I (rightfully) anticipated needing this data later.

```
def __init__(self, answer_list=[]):
    self.answer_list = answer_list
    self.response_dict = {}

    # for each group member's answer, update the response dict
    for answer in answer_list:
        # for each specific answer, increment the question's yes count
        for question in answer:
            yes_count = 0
            if question in self.response_dict.keys():
                yes_count = self.response_dict[question] + 1
            self.response_dict[question] = yes_count
```

## Part 1
>In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.
>
>For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
>
>Your puzzle answer was **6930**.

My intuition paid off here -- summing the number of questions for which any group member answered "yes" was as simple as counting the unique keys in my underlying dictionary and adding those together later. 

```
def get_any_yes_count(self):
    return len(self.response_dict)
```

## Part 2
>--- Part Two ---
>
>As you finish the last group's customs declaration, you notice that you misread one word in the instructions:
>
>You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!
>
>Using the same example as above:
>```
>abc
>
>a
>b
>c
>
>ab
>ac
>
>a
>a
>a
>a
>
>b
>```
>This list represents answers from five groups:
>
>- In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
>- In the second group, there is no question to which everyone answered "yes".
>- In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
>- In the fourth group, everyone answered yes to only 1 question, a.
>- In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
>
>In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.
>
>For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
>
>Your puzzle answer was **3585**.

Again, my intuition paid off! I only needed to add a couple lines to my constructor:
1. A `self.num_respondents` property (instantiated at `0`) that I could use as a counter
2. A `self.num_respondents += 1` line to increment my counter for each answer in the answer list

Then, to determine how many questions _every_ group member answered yes for, all I had to do was count the number of dictionary items where the value equaled the number of respondents. To check this:
1. I renamed the `get_yes_count()` method to be `get_any_yes_count()`
2. I created a `get_all_yes_count()` method with the following logic: 
```
def get_all_yes_count(self):
    all_yes_count = 0
    for key in self.response_dict:
        if self.response_dict[key] == self.num_respondents:
            all_yes_count += 1
    return all_yes_count
```

Lastly, I updated my summing method (which previously summed up the `get_yes_count()` results for each group) to take a boolean so that I could easily toggle which "yes type" (i.e. any or all) to use:
```
def sum_yes_answers(answers, require_all):
    yes_sum = 0
    for answer in all_answers:
        if require_all:
            yes_sum += answer.get_all_yes_count()
        else:
            yes_sum += answer.get_any_yes_count()
```

But, things rarely work on the first time. Turns out that while I successfully anticipated needing to know how many group members answered yes on each question, I did not correctly store that value (and because Part 1 didn't need that information, I didn't notice the bug until Part 2). In my original constructor, I was improperly incrementing my yes count, but the fix was as easy as changing this:
```
for question in answer:
    yes_count = 0
    if question in self.response_dict.keys():
        yes_count = self.response_dict[question] + 1
    self.response_dict[question] = yes_count
```
to start the yes count at `1` and to remove the `1` increment in the case that the key already existed:
```
for question in answer:
    yes_count = 1
    if question in self.response_dict.keys():
        yes_count += self.response_dict[question]
    self.response_dict[question] = yes_count
```

And then it worked as expected 😌