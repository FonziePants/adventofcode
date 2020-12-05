# [Day 4: Passport Processing](https://adventofcode.com/2020/day/4)
>--- Day 4: Passport Processing ---
>
>You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually valid documentation for travel in most of the world.
>
>It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport scanners, and the delay could upset your travel itinerary.
>
>Due to some questionable network security, you realize you might be able to solve both of these problems at the same time.
>
>The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:
>
>- byr (Birth Year)
>- iyr (Issue Year)
>- eyr (Expiration Year)
>- hgt (Height)
>- hcl (Hair Color)
>- ecl (Eye Color)
>- pid (Passport ID)
>- cid (Country ID)
>Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.
>
>Here is an example batch file containing four passports:
>```
>ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
>byr:1937 iyr:2017 cid:147 hgt:183cm
>
>iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
>hcl:#cfa07d byr:1929
>
>hcl:#ae17e1 iyr:2013
>eyr:2024
>ecl:brn pid:760753108 byr:1931
>hgt:179cm
>
>hcl:#cfa07d eyr:2025 pid:166559648
>iyr:2011 ecl:brn hgt:59in
>```
>The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).
>
>The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.
>
>The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.
>
>According to the above rules, your improved system would report 2 valid passports.

This passport puzzle was a sad reminder that we can't travel during these pandemic times 😭 But the good news is that today was the first day that I completed the puzzle before the other two people on my friend's private leaderboard ✨ ...although this required me cutting some corners as my spouse typed furiously on his newly cleaned mechanical keyboard behind me.

For this puzzle, I decided my `solutions` directory was getting a little too messy and so I made a subdirectory for Day 04 specifically. I plan to continue this going forward.

Because the puzzle involved lists of arbitrarily ordered key-value pairs, I started off my work by defining a `Constants` class in which to store all of the keys. Then, I created a `Passport` class with the eight properties defaulting to values of `None`.

To ingest the test data, I created a method that reads the file line by line, storing what it reads into a temporary string variable. When it comes across an empty line, it knows it's at the end of a Passport definition and so it then splits the temporary string by its whitespace and pulls out the values one by one, matching them to a list of keys. It then creates a new `Passport` object, appends that to a list, and clears the temporary string. Rinse, wash, and repeat.

## Part 1
>Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?
>
>Your puzzle answer was **260**.

For part one, I just created an `is_valid` method on the `Passport` class that returns `False` if any of the properties are missing (i.e. `is None`) -- with the exception of `country_id`, which is allowed to be missing. This was all pretty straightforward and worked right away, despite my `passpord_id` typo (which I have since fixed).

## Part 2
>--- Part Two ---
>
>The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data are getting through. Better add some data validation, quick!
>
>You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:
>
>byr (Birth Year) - four digits; at least 1920 and at most 2002.
>iyr (Issue Year) - four digits; at least 2010 and at most 2020.
>eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
>hgt (Height) - a number followed by either cm or in:
>If cm, the number must be at least 150 and at most 193.
>If in, the number must be at least 59 and at most 76.
>hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
>ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
>pid (Passport ID) - a nine-digit number, including leading zeroes.
>cid (Country ID) - ignored, missing or not.
>Your job is to count the passports where all required fields are both present and valid according to the above rules. Here are some example values:
>
>byr valid:   2002
>byr invalid: 2003
>
>hgt valid:   60in
>hgt valid:   190cm
>hgt invalid: 190in
>hgt invalid: 190
>
>hcl valid:   #123abc
>hcl invalid: #123abz
>hcl invalid: 123abc
>
>ecl valid:   brn
>ecl invalid: wat
>
>pid valid:   000000001
>pid invalid: 0123456789
>Here are some invalid passports:
>```
>eyr:1972 cid:100
>hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
>
>iyr:2019
>hcl:#602927 eyr:1967 hgt:170cm
>ecl:grn pid:012533040 byr:1946
>
>hcl:dab227 iyr:2012
>ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
>
>hgt:59cm ecl:zzz
>eyr:2038 hcl:74454a iyr:2023
>pid:3556412378 byr:2007
>```
>Here are some valid passports:
>```
>pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
>hcl:#623a2f
>
>eyr:2029 ecl:blu cid:129 byr:1989
>iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
>
>hcl:#888785
>hgt:164cm byr:2001 iyr:2015 cid:88
>pid:545766238 ecl:hzl
>eyr:2022
>
>iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
>```
>Count the number of valid passports - those that have all required fields and valid values. Continue to treat cid as optional. In your batch file, how many passports are valid?
>
>Your puzzle answer was **153**.

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
```
valid_eye_colors = ["amb", "blu", <b>"brn,"</b> "gry", "grn", "hzl", "oth"]
```

...instead of:
```
valid_eye_colors = ["amb", "blu", <b>"brn",</b> "gry", "grn", "hzl", "oth"]
```

Naturally, there were no `brn,` eye colors. With this quick fix, my validation was working as expected and I was able to get the right answer about two minutes before my spouse could! 😎 Luckily for me, he forgot to include the start and end of line matches in his regex, which not only let me squeak past him on this Day 4 puzzle but also reinforced my decision to skip out on regex today 😂