# [Day 16: Ticket Translation](https://adventofcode.com/2020/day/16)
>--- Day 16: Ticket Translation ---
>
>As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should probably figure out what it says before you get to the train station after the next flight.
>
>Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure out the fields these tickets must have and the valid ranges for values in those fields.
>
>You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the same train service (via the airport security cameras) together into a single document you can reference (your puzzle input).
>
>The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).
>
>Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:
>```
>.--------------------------------------------------------.
>| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
>|                                                        |
>| ??: 301  ??: 302             ???????: 303      ??????? |
>| ??: 401  ??: 402           ???? ????: 403    ????????? |
>'--------------------------------------------------------'
>```
>Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've extracted just the numbers in such a way that the first number is always the same specific field, the second number is always a different specific field, and so on - you just don't know what each position actually means!

This problem looked fun right away! It was easy to guess the ultimate goal of this would be to identify which fields were which. Accordingly, I kicked off this problem by writing:
- A `Field` class that takes a line and stores its `name` and a list of its valid `values`
- A method to read the file, to store each field as a `Field` option in a `fields` list, to store the tickets each as an array of ints and store them in a `tickets` array

## Part 1
>Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for any field. Ignore your ticket for now.
>
>For example, suppose you have the following notes:
>```
>class: 1-3 or 5-7
>row: 6-11 or 33-44
>seat: 13-40 or 45-50
>
>your ticket:
>7,1,14
>
>nearby tickets:
>7,3,47
>40,4,50
>55,2,20
>38,6,12
>```
>It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.
>
>Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
>
>Your puzzle answer was **27802**.

Because I love the instant-lookup aspect of dictionaries, I decided to create a dictionary `valid_values` where each key was a numeric value and each value was an array of possible fields it could apply to:
```
valid_values = {}
    
for field in fields:
    for value in field.values:
        if value in valid_values:
            valid_values[value].append(field.name)
        else:
            valid_values[value] = [field.name]
```

Then, I iterated through each ticket and:

1. Went through each value in a ticket
2. Checked to see if this value was in the `valid_values` dictionary
3. If there was an invalid value, I multiplied it by an `error_rate` variable
4. However, if all the values in the ticket were valid, I added the ticket to a `valid_tickets` array

```
error_rate = 0
for ticket in tickets:
    valid = True
    for value in ticket:
        if value not in valid_values:
            error_rate += value
            valid = False
    if valid:
        valid_tickets.append(ticket)
```

## Part 2
>--- Part Two ---
>
>Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.
>
>Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.
>
>For example, suppose you have the following notes:
>```
>class: 0-1 or 4-19
>row: 0-5 or 8-19
>seat: 0-13 or 16-19
>
>your ticket:
>11,12,13
>
>nearby tickets:
>3,9,18
>15,1,5
>5,14,9
>```
>Based on the nearby tickets in the above example, the first position must be row, the second position must be class, and the third position must be seat; you can conclude that in your ticket, class is 12, row is 11, and seat is 13.
>
>Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?
>
>Your puzzle answer was **279139880759**.

I really enjoyed thinking through how to logically determine which fields were which. I figured I could solve this by going through all the fields (that is, indices in the ticket) until I found one where there was only one possible field according to the `valid_values` dictionary. Once I found this field, I removed it from the options in `valid_values` and then went through all the ticket indices again.

These were the steps:

1. Create an array of fields called `field_indices` where each entry's index matches its position in the actual tickets. I defaulted the value of each element to `False` with the plan to replace it with a field name once it was determined

```
field_indices = []
for i in range(len(fields)):
    field_indices.append(False)
```

2. Create a loop that does not break until all `False` values in the `field_indices` array have been replaced

```
while False in field_indices:
```

3. Create a for-loop that iterates through each position in a ticket 

```
for i in range(len(field_indices)):
```

4. Create a list of values for that ticket position by iterating through all of the tickets

```
values = []
for ticket in tickets:
    if ticket[i] not in values:
        values.append(ticket[i])
```

5. Create a `possible_fields` list initiated with the possible fields based on the `valid_values` entry for the first ticket's (that is, _your_ ticket's) value at position `i`

```
possible_fields = valid_values[values[0]].copy()
```

6. Iterating through each value already collected in the `values` collection, remove fields one by one from the `possible_fields` collection if a value does not fall within its range

```
for j in range(1,len(values)):
    for field in possible_fields:
        if field not in valid_values[values[j]]:
            possible_fields.remove(field)
```

7. The final step in the whole loop is to check if the `possible_fields` collection has been whittled down to only one possible value. If so, then replace that the corresponding entry in the `field_indices` with that field's name and remove that field from the remaining options in `valid_values`

```
if len(possible_fields) == 1:
    field = possible_fields[0]
    field_indices[i] = field
    remove_field(valid_values,field)
```

8. Once the loop completes and all the fields have been identified, loop through each field in `field_indices` and multiply its value in your ticket (the ticket at position `0`) by an `answer` variable if that field contains `departure`

```
answer = 1
for i in range(len(field_indices)):
    if "departure" in field_indices[i]:
        answer *= tickets[0][i]
```