# [Day 2: Password Philosophy](https://adventofcode.com/2020/day/2)
> --- Day 2: Password Philosophy ---
>
> Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.
>
> The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers; we can't log in!" You ask if you can take a look.
>
> Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the Official Toboggan Corporate Policy that was in effect when they were chosen.
>
> To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted database) and the corporate policy when that password was set.
>
> For example, suppose you have the following list:
>
>- `1-3 a: abcde`
>- `1-3 b: cdefg`
>- `2-9 c: ccccccccc`
>
> Each line gives the password policy and then the password. The password policy indicates the lowest and highest number of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.
>
> In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of their respective policies.

So far, this whole "Advent of Code" thing seems like a great way to learn (or re-learn, in my case) a language. For day 2, I need to take a structured input and make sense of it, so this seemed like a great opportunity to learn [how to read lines from a file](https://www.w3schools.com/python/python_file_open.asp). Turns out, Python makes this easy (like everything else).

Because each line represented a password entry, and because each password entry had several characteristics (i.e. the password itself, a required character, and the minimum and maximum number of instances of said character), this seemed like a great opportunity to use a class. As always, [w3 schools is a wonderful resource](https://www.w3schools.com/python/python_classes.asp)!

Lastly, to convert this structured file input into the aforementioned class, I needed to also learn a little Python string manipulation to [split the lines into segments](https://www.tutorialspoint.com/python/string_split.htm), to [strip out unwanted characters](https://www.tutorialspoint.com/python/string_replace.htm), and [to count the number of instances of a specific substring](https://www.tutorialspoint.com/python/string_count.htm).

## Part 1
> How many passwords are valid according to their policies?
>
> Your puzzle answer was **447**.

My solution to part 1 was as follows:
1. Define a `PasswordEntry` class that takes a string and manipulates it into a few properties (i.e. `password`, `required_character`, `min_required_character`, and `max_required_character`) and has `print()` and `is_valid()` methods for testing and convenience
2. Define a `create_password_list(input_file)` method that opens a specified file and generates a list of `PasswordEtntry` instances from its contents
3. Define a `count_valid_passwords(input_file)` method that calls the aforementioned `create_password_list` method and then iterates through its elements, incrementing a `valid_password_count` counter for each element whose `is_valid()` returns `True`
4. 🥂 

## Part 2
> --- Part Two ---
>
> While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan Corporate Authentication System is expecting.
>
> The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job at the sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.
>
> Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy enforcement.
>
> Given the same example list from above:
>
>- `1-3 a: abcde` is valid: position 1 contains a and position 3 does not.
>- `1-3 b: cdefg` is invalid: neither position 1 nor position 3 contains b.
>- `2-9 c: ccccccccc` is invalid: both position 2 and position 9 contain c.
>
> How many passwords are valid according to the new interpretation of the policies?
>
> Your puzzle answer was **249**.

For part two, the logic of what makes a password valid changed, but I didn't want to redo my existing solution -- rather, I wanted to be able to easily switch between part 1 and part 2 logic without removing or rewriting code. Accordingly, I made the following changes:
- Created two new properties on my `PasswordEntry` class, `first_character_position` and `second_character_position`, which have the same values as the `min...` and `max...` properties, but with 1 subtracted so that they are properly zero-indexed
- Renamed the `is_valid()` method to be `is_valid_part1()`
- Created an `is_valid_part2()` method which first checks to make sure there are no out of bounds errors and then determines if position 1 and position 2 contain the desired character
- Lastly, the `is_valid_part2()` method returns an exclusive-or check (i.e. the first or second position have the required character, but not both)

Now, to toggle between part 1's logic and part 2's logic, all I need to do is change which `is_valid...()` method that I call, and _voila_! 

Worked on the first try 😎