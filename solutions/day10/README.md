# [Day 10: Adapter Array](https://adventofcode.com/2020/day/10)
>--- Day 10: Adapter Array ---
>
>Patched into the aircraft's data port, you discover weather forecasts of a massive tropical storm. Before you can figure out whether it will impact your vacation plans, however, your device suddenly turns off!
>
>Its battery is dead.
>
>You'll need to plug it in. There's only one problem: the charging outlet near your seat produces the wrong number of jolts. Always prepared, you make a list of all of the joltage adapters in your bag.
>
>Each of your joltage adapters is rated for a specific output joltage (your puzzle input). Any given adapter can take an input 1, 2, or 3 jolts lower than its rating and still produce its rated output joltage.
>
>In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the highest-rated adapter in your bag. (If your adapter list were 3, 9, and 6, your device's built-in adapter would be rated for 12 jolts.)
>
>Treat the charging outlet near your seat as having an effective joltage rating of 0.
>
>Since you have some time to kill, you might as well test all of your adapters. Wouldn't want to get to your resort and realize you can't even charge your device!
>
>If you use every adapter in your bag at once, what is the distribution of joltage differences between the charging outlet, the adapters, and your device?
>
>For example, suppose that in your bag, you have adapters with the following joltage ratings:
>```
>16
>10
>15
>5
>1
>11
>7
>19
>6
>12
>4
>```
>With these adapters, your device's built-in joltage adapter would be rated for `19 + 3 = 22` jolts, 3 higher than the highest-rated adapter.
>
>Because adapters can only connect to a source 1-3 jolts lower than its rating, in order to use every adapter, you'd need to choose them like this:
>
>- The charging outlet has an effective rating of 0 jolts, so the only adapters that could connect to it directly would need to have a joltage rating of 1, 2, or 3 jolts. Of these, only one you have is an adapter rated 1 jolt (difference of 1).
>- From your 1-jolt rated adapter, the only choice is your 4-jolt rated adapter (difference of 3).
>- From the 4-jolt rated adapter, the adapters rated 5, 6, or 7 are valid choices. However, in order to not skip any adapters, you have to pick the adapter rated 5 jolts (difference of 1).
>- Similarly, the next choices would need to be the adapter rated 6 and then the adapter rated 7 (with difference of 1 and 1).
>- The only adapter that works with the 7-jolt rated adapter is the one rated 10 jolts (difference of 3).
>- From 10, the choices are 11 or 12; choose 11 (difference of 1) and then 12 (difference of 1).
>- After 12, only valid adapter has a rating of 15 (difference of 3), then 16 (difference of 1), then 19 (difference of 3).
>- Finally, your device's built-in adapter is always 3 higher than the highest adapter, so its rating is 22 jolts (always a difference of 3).
>
>In this example, when using every adapter, there are 7 differences of 1 jolt and 5 differences of 3 jolts.
>
>Here is a larger example:
>```
>28
>33
>18
>42
>31
>14
>46
>20
>48
>47
>24
>23
>49
>45
>19
>38
>39
>11
>1
>32
>25
>35
>8
>17
>7
>9
>4
>2
>34
>10
>3
>```
>In this larger example, in a chain that uses all of the adapters, there are 22 differences of 1 jolt and 10 differences of 3 jolts.

The standard thing to do here would be to sort the number array in order to get the list of sequential numbers. This was as easy as reading a file line by line, casting the lines to ints before storing them in an array, and then running `.sort()`.

Because I'd need to account for the seat's charging outlet, I added a value of `0` to the beginning of the array. Likewise, because I needed to account for the device, I took the last value, added `3`, and plopped it at the end of the collection.

## Part 1
>Find a chain that uses all of your adapters to connect the charging outlet to your device's built-in adapter and count the joltage differences between the charging outlet, the adapters, and your device. What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
>
>Your puzzle answer was **2040**.

This was pretty straightforward with the sorted array. All that was needed was to:

- Create summing variables for the difference-of-one and difference-of-three counts (personally, I used a dictionary where the key was the difference, e.g. `3`, and the value was the count of occurrences -- this allowed me to store bigger or small differences if part 2 demanded it)
```
diff_count = {}
```
- Iterate through each joltage, look at the difference between it and its predecessor, and then increment that difference's count in the summing value (in my case, a dictonary entry)
```
for i in range(1,len(adapters)):
    diff = adapters[i] - adapters[i-1]

    if diff in diff_count:
        diff_count[diff] = diff_count[diff] + 1
    else:
        diff_count[diff] = 1
```
- Lastly, multiply the difference-counts for 1 and 2
```
return diff_count[1] * diff_count[3]
```


## Part
>--- Part Two ---
>
>To completely determine whether you have enough adapters, you'll need to figure out how many different ways they can be arranged. Every arrangement needs to connect the charging outlet to your device. The previous rules about when adapters can successfully connect still apply.
>
>The first example above (the one that starts with 16, 10, 15) supports the following arrangements:
>```
>(0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
>(0), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
>(0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
>(0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
>(0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
>(0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
>(0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
>(0), 1, 4, 7, 10, 12, 15, 16, 19, (22)
>```
>(The charging outlet and your device's built-in adapter are shown in parentheses.) Given the adapters from the first example, the total number of arrangements that connect the charging outlet to your device is 8.
>
>The second example above (the one that starts with 28, 33, 18) has many arrangements. Here are a few:
>```
>(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
>32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49, (52)
>
>(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
>32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 49, (52)
>
>(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
>32, 33, 34, 35, 38, 39, 42, 45, 46, 48, 49, (52)
>
>(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
>32, 33, 34, 35, 38, 39, 42, 45, 46, 49, (52)
>
>(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
>32, 33, 34, 35, 38, 39, 42, 45, 47, 48, 49, (52)
>
>(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
>46, 48, 49, (52)
>
>(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
>46, 49, (52)
>
>(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
>47, 48, 49, (52)
>
>(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
>47, 49, (52)
>
>(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
>48, 49, (52)
>In total, this set of adapters can connect the charging outlet to your device in 19208 distinct arrangements.
>
>You glance back down at your bag and try to remember why you brought so many adapters; there must be more than a trillion valid ways to arrange them! Surely, there must be an efficient way to count the arrangements.
>
>What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?
>
>Your puzzle answer was **28346956187648**.

This problem was a ton of fun! While I was tempted to just brute force the answer in order to finish the problem before the others on my Advent of Code leaderboard did, the challenge of thinking through this algorithmically was just too tempting. So, instead of rushing to write a bunch of nested loops that generated and stored all permutations, I took out a pencil and paper and wrote out the possible forking choices per element of the smaller test data set:
```
data:         0   1   4   5   6   7  10  11  12  15  16  19  22
fork options: 1   1   3   2   1   1   2   1   1   1   1   1   1
```

At first, I thought, "let's multiply these!" because intuitively it made sense that every fork later in the list would multiple the number of options for earlier forks. However, this clearly wasn't correct because `3 * 2 * 2 = 12` and not the correct answer of `8`.

So, I wrote out the individual fork options for each element to get a better idea of where the 4 _duplicative_ options came from.
```
data:         0   1   4   5   6   7  10  11  12  15  16  19  22
fork options: 1   1   3   2   1   1   2   1   1   1   1   1   0
             --  --  --  --  --  --  --  --  --  --  --  --  --
fork opt 1:   1   4   5   6   7  10  11  12  15  16  19  22
fork opt 2:           6   7          12
fork opt 3:           7
```

The issue became more clear upon examining joltage `4`: multiplying `4`'s option count of `3` by `5`'s option count of 2 doesn't make sense because only `4`'s first fork option would result in the doubling of options. Why? Because both `4`'s second fork option (i.e. `6`) and third fork option (i.e. `7`) have a single path until hitting joltage `10`. Basically, the math needed to be as follows:

- Joltage `19` only has **one** option
- Joltage `16`'s number of options is equal to the number of options of its only option (i.e. `19`), so **one** again
- ^ Same logic goes for joltages `11` through `15` -- they each only have one option, so their number of options is always **one**
- Joltage `10` has two _immediate_ options, so its total number of options is the number of options for its first option (i.e. one for `11`) plus the number of options for its second option (i.e. one for `12`) -- so a total of **two** total options created for the rest of the sequence
- Joltage `7` only has one option, but that one option (i.e. `10`) has two options, so `7`'s options are also two
- Likewise, joltage `6` only has one option, so its options are also two
- Joltage `5` has two _immediate_ options, so its total number of options is the number of options for its first option (i.e. two for `6`) plus the number of options for its second option (i.e. two for `6`) -- so a total of **four** total options created for the rest of the sequence
- Joltage `4`, as mentioned previously, gets tricky. Its first option, `5`, has _four_ options, but its next two options, `6` and `7`, each only have two options, so the total options for joltage `4` is **`4 + 2 + 2 = 8`** for a total options value of **eight**
- None of the prior joltages introduce any potential forking, so the total number of permutations of adapter-chains comes out to **eight**

Basically, the math required is to **sum the "total option values" of an element's immediate options**. To get this number, I did the following:

1. Create a map that for each **joltage key** stores an **array of possible subsequent joltages** as values
```
options_map = {}

for i in range(0,len(adapters)):
    options = []

    for j in range(1,4):
        if adapters_can_connect(adapters,i,i+j):
            options.append(adapters[i+j])

    options_map[adapters[i]] = options
```

2. Create an empty map where each **joltage key** stores a **total number of permutations for the rest of the array** -- _this_ we will use to calculate total permutations for any preceeding voltages
3. **Starting from the final, highest adapter, iterate** and calculate each adapter's total downstream options by summing the downstream options for each of its values
```
decisions_map = {}

decisions_map[adapters[len(adapters)-1]] = 1
for i in reversed(range(len(adapters)-1)):
    option_sum = 0
    for option in options_map[adapters[i]]:
        option_sum += decisions_map[option]
    decisions_map[adapters[i]] = option_sum
```
4. Return the total options value of the **first element** because that will be the total number of permutations for the list
```
return decisions_map[adapters[0]]
```

I enjoyed this problem because it required understanding the tree-nature of multiplying options without requiring you to actually traverse a tree. I was happy with my simple loops and quick dictionary and array lookups.

Lastly, I enjoyed the option to create convenience functionality, such as making my print statements toggle-able with `debug=False` method parameters and `if debug:` checks as well as making method to reduce code duplicity. For example, instead of checking each possible acceptable joltage difference:
```
if i < len(adapters):
    if i+1 < len(adapters) and (adapters[i+1] - adapters[i] <= 3):
        options.append(adapters[i+1])
    if i+2 < len(adapters) and (adapters[i+2] - adapters[i] <= 3):
        options.append(adapters[i+2])
    if i+3 < len(adapters) and (adapters[i+3] - adapters[i] <= 3):
        options.append(adapters[i+3])
```

I could run the following:
```
for j in range(1,4):
    if adapters_can_connect(adapters,i,i+j):
        options.append(adapters[i+j])
```
```
def adapters_can_connect(adapters,index1,index2):
    if index1 >= len(adapters) or index2 >= len(adapters):
        return False
    
    return (adapters[index2] - adapters[index1]) <= 3
```

The value-add here is that if a future problem ever increased the acceptable joltage difference from `3` to any other number, I could abstract it out without a significant code rewrite.

All said and done, I thought today's problem was a nice little challenge.