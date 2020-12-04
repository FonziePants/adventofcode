# adventofcode
## What is this?
This is a repository that contains code for solving the [Advent of Code 2020 challenges](https://adventofcode.com/2020/day/1).

## Setup
To set up Python in a Windows 10 VS Code environment, [follow these instructions](https://code.visualstudio.com/docs/python/python-tutorial).

## The challenges

### Day 1: Report Repair
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

### Day 2: Password Philosophy
So far, this whole "Advent of Code" thing seems like a great way to learn (or re-learn, in my case) a language. For day 2, I need to take a structured input and make sense of it, so this seemed like a great opportunity to learn [how to read lines from a file](https://www.w3schools.com/python/python_file_open.asp). Turns out, Python makes this easy (like everything else).

Because each line represented a password entry, and because each password entry had several characteristics (i.e. the password itself, a required character, and the minimum and maximum number of instances of said character), this seemed like a great opportunity to use a class. As always, [w3 schools is a wonderful resource](https://www.w3schools.com/python/python_classes.asp)!

Lastly, to convert this structured file input into the aforementioned class, I needed to also learn a little Python string manipulation to [split the lines into segments](https://www.tutorialspoint.com/python/string_split.htm), to [strip out unwanted characters](https://www.tutorialspoint.com/python/string_replace.htm), and [to count the number of instances of a specific substring](https://www.tutorialspoint.com/python/string_count.htm).

My solution to part 1 was as follows:
1. Define a `PasswordEntry` class that takes a string and manipulates it into a few properties (i.e. `password`, `required_character`, `min_required_character`, and `max_required_character`) and has `print()` and `is_valid()` methods for testing and convenience
2. Define a `create_password_list(input_file)` method that opens a specified file and generates a list of `PasswordEtntry` instances from its contents
3. Define a `count_valid_passwords(input_file)` method that calls the aforementioned `create_password_list` method and then iterates through its elements, incrementing a `valid_password_count` counter for each element whose `is_valid()` returns `True`
4. 🥂 

For part two, the logic of what makes a password valid changed, but I didn't want to redo my existing solution -- rather, I wanted to be able to easily switch between part 1 and part 2 logic without removing or rewriting code. Accordingly, I made the following changes:
- Created two new properties on my `PasswordEntry` class, `first_character_position` and `second_character_position`, which have the same values as the `min...` and `max...` properties, but with 1 subtracted so that they are properly zero-indexed
- Renamed the `is_valid()` method to be `is_valid_part1()`
- Created an `is_valid_part2()` method which first checks to make sure there are no out of bounds errors and then determines if position 1 and position 2 contain the desired character
- Lastly, the `is_valid_part2()` method returns an exclusive-or check (i.e. the first or second position have the required character, but not both)

Now, to toggle between part 1's logic and part 2's logic, all I need to do is change which `is_valid...()` method that I call, and _voila_! 

Worked on the first try 😎

### Day 3: Toboggan Trajectory
Today's was pretty straightforward. Before I even finished readng the problem, I figured it would make sense to write the code to ingest the map and store it as a 2D boolean array of tree-or-no-tree. I threw this in a class so that I could run convenience methods (like printing) without needing to pass in a 2d array everywhere.

The trickiest part of this is probably the map extension, but this was easy to solve with modulo math. Basically, store the original width, and then when either printing or calculating a tree hit, just use X modulo map-width.

By passing in the x-delta and y-delta programmatically, I was easily able to extend my answer to part 2 without making any major functional changes.

The main issue I ran into, for which I used pretty printing to debug, was that the newline character of the files being read in was wrongly adding to the map's width. A simple `str.rstrip()` call fixed this issue.

### Day 4: Passport Processing
This passport puzzle was a sad reminder that we can't travel during these pandemic times 😭 But the good news is that today was the first day that I completed the puzzle before the other two people on my friend's private leaderboard ✨ ...although this required me cutting some corners as my spouse typed furiously on his newly cleaned mechanical keyboard behind me.

For this puzzle, I decided my `solutions` directory was getting a little too messy and so I made a subdirectory for Day 04 specifically. I plan to continue this going forward.

Because the puzzle involved lists of arbitrarily ordered key-value pairs, I started off my work by defining a `Constants` class in which to store all of the keys. Then, I created a `Passport` class with the eight properties defaulting to values of `None`.

To ingest the test data, I created a method that reads the file line by line, storing what it reads into a temporary string variable. When it comes across an empty line, it knows it's at the end of a Passport definition and so it then splits the temporary string by its whitespace and pulls out the values one by one, matching them to a list of keys. It then creates a new `Passport` object, appends that to a list, and clears the temporary string. Rinse, wash, and repeat.

For part one, I just created an `is_valid` method on the `Passport` class that returns `False` if any of the properties are missing (i.e. `is None`) -- with the exception of `country_id`, which is allowed to be missing. This was all pretty straightforward and worked right away, despite my `passpord_id` typo (which I have since fixed).

Part two complicated things a little bit because each property suddenly had its own unique validation requirements. For this, I created a validation method for each individual property. 
- For **birth year**, **issue year**, and **expiration year**, I created a generic `validate_year(year, min_year, max_year)` with which I could pass in each of the three year property's unique year boundaries. 
- For **height**, I pulled out the unit and then checked the ranges by unit, returning `False` if any of the safety checks were not met (for example, a `None` value, too short a string length, or a missing unit).
- With **hair color** is where I cut corners for speed. By the sound of rushed typing coming from behind me, I knew my partner was catching up to me, so in lieu of [importing a regex module](https://www.w3schools.com/python/python_regex.asp) and figuring out the regex needed, I went with what I thought was quicker to implement quickly and correctly. Instead of an elegant regex check, I just made sure that the string was exactly 7 characters in length, that it's first character was `#`, and that the subsequent 6 characters were either a digit (i.e. `isdigit()`) or in the character-set of `a` through `f` (using `.lower()` to avoid needing to worry about casing).
- For **eye color**, I simply created a list of valid values and then checked to make sure the value was present in it. Easy peasy!
- With **passport ID**, again, I intentionally sidestepped using regex. Instead, I checked to make sure the string length was nine and that each character was a digit.

On the test data set, I only ran into one issue: I was accidentally returning the opposite boolean value in my year validtion. This fix was `not` very hard 😏

When I moved into the real data set (complete with 291 passports to check 🤯), I had my first experience entering the wrong answer!! 🙈 In addition to some subtle "don't cheat" messaging (a la "hey, your answer was right for _someone else_..."), the error messaging luckily gave me a clue that my answer was _too low_, which means I was wrongly marking some properties and thus passports as invalid. Obviously, 7 validated properties across 291 items is a lot to check, so I broke down my debugging process.

For each passport where **birth year** was marked as invalid (because there was no reason to check the valid ones as my answer was too low, not too high), I printed the allegedly invalid birth years and manually skimmed these to see if there were any anomalies. When my birth year validation checked out, I tried the same with **issue year**, **expiration year**, **height**, and then **hair color**. All were looking good.

Then, when I tested my **eye color** validation, I was in for a surprise: a bunch of `brn` and `gry` eye colors were being marked invalid! A quick scroll up to my validation method revealed a typo... 

I had used this:

<code>
valid_eye_colors = ["amb", "blu", <b>"brn,"</b> "gry", "grn", "hzl", "oth"]
</code>

...instead of:

<code>
valid_eye_colors = ["amb", "blu", <b>"brn",</b> "gry", "grn", "hzl", "oth"]
</code>

Naturally, there were no `brn,` eye colors. With this quick fix, my validation was working as expected and I was able to get the right answer about two minutes before my spouse could! 😎 Luckily for me, he forgot to include the start and end of line matches in his regex, which not only let me squeak past him on this Day 4 puzzle but also reinforced my decision to skip out on regex today 😂