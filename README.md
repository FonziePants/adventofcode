# adventofcode
## What is this?
This is a repository that contains code for solving the [Advent of Code 2020 challenges](https://adventofcode.com/2020/day/1).

## Setup
To set up Python in a Windows 10 VS Code environment, [follow these instructions](https://code.visualstudio.com/docs/python/python-tutorial).

## The challenges

### Day 1
I chose to use Python because I haven't used it in 16 years (2004!!) and everybody seems to love it these days. Turns out, I still dislike dynamically typed languages. Additionally, the fact that the built-in `sort()` method mutates the object it's used on instead of returning a copy also threw me for a loop. [Thank goodness for stackoverflow and the time and head-bangings it saves](https://stackoverflow.com/questions/7301110/why-does-return-list-sort-return-none-not-the-list).

I wavered between using a dictionary/hashmap data structure, where I could calculate the expected addend and do a lookup, versus iterating through loops and risking worst-case O(n<sup>2</sup>) performance. Ultimately, I opted for the loops if only because I was re-learning Python on the fly and I wanted to go to bed on time.

The general approach I took was as follows:
- Sort the inputs (as one should usually do in these kinds of problems...)
- Start a loop that increments from the front
- Nest a loop that decrements from the back
- Break the loop if we're already below 2020 (because all the decrementing-from-the-back is just a waste of time at that point)
- Return the product if we get two numbers that sum to 2020

The downside of this approach is obviously the runtime -- worst case scenario, the list is full of a bunch of close, high numbers. The upside of this approach revealed itself for part 2, where we were asked to find _three entries_ that sum up to 2020. It was easy to modify my approach to have a third nested loop (yikes @ performance) with a few checks to avoid going through the loops unnecessarily; for example:
- Skip the middle loop if the first two loops already sum above 2020
- Break out of both the second and third loops if the sums drop below 2020 (because in this case you'll need to increment the lowest value no matter what)
- Determine the range for the most-nested loop by always putting its range between the indices of the first and second loop so that we can prevent double-counting

There's probably a few edge cases I didn't account for (like the upper bound going below the lower bound), but _c'est la vie_.

**UPDATE:** My spouse guilted me into rewriting this for performance (or rather, he showed me his super fast C version which made me jealous). I improved the runtime by replacing the middle loop with a lookup. The changes were as follows:
- Create a dictionary ([super easy, it turns out -- thanks stackoverflow](https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary)) that includes keys for all the entries where their values are the number of times those entries appear in the list
- Replace the middle loop with a check to calculate the desired addend by adding the current lower and upper values and subtracting those from 2020
- Check to see if the desired addend is in the dictionary -- if so, return the product
- Remove superfluous checks

I think the lesson here is to be mildly competitive and to marry someone in the same field as you who will make you always strive to write better code. 

### Day 2
So far, this whole "Advent of Code" thing seems like a great way to learn (or re-learn, in my case) a language. For day 2, I need to take a structured input and make sense of it, so this seemed like a great opportunity to learn [how to read lines from a file](https://www.w3schools.com/python/python_file_open.asp). Turns out, Python makes this easy (like everything else).

Because each line represented a password entry, and because each password entry had several characteristics (i.e. the password itself, a required character, and the minimum and maximum number of instances of said character), this seemed like a great opportunity to use a class. As always, [w3 schools is a wonderful resource](https://www.w3schools.com/python/python_classes.asp)!

Lastly, to convert this structured file input into the aforementioned class, I needed to also learn a little Python string manipulation to [split the lines into segments](https://www.tutorialspoint.com/python/string_split.htm), to [strip out unwanted characters](https://www.tutorialspoint.com/python/string_replace.htm), and [to count the number of instances of a specific substring](https://www.tutorialspoint.com/python/string_count.htm).

My solution to part 1 was as follows:
1. Define a `PasswordEntry` class that takes a string and manipulates it into a few properties (i.e. `password`, `required_character`, `min_required_character`, and `max_required_character`) and has `print()` and `is_valid()` methods for testing and convenience
2. Define a `create_password_list(input_file)` method that opens a specified file and generates a list of `PasswordEtntry` instances from its contents
3. Define a `count_valid_passwords(input_file)` method that calls the aforementioned `create_password_list` method and then iterates through its elements, incrementing a `valid_password_count` counter for each element whose `is_valid()` returns `True`
4. 🥂 