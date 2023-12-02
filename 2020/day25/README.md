# [Day 25: Combo Breaker](https://adventofcode.com/2020/day/25)
>--- Day 25: Combo Breaker ---
>
>You finally reach the check-in desk. Unfortunately, their registration systems are currently offline, and they cannot check you in. Noticing the look on your face, they quickly add that tech support is already on the way! They even created all the room keys this morning; you can take yours now and give them your room deposit once the registration system comes back online.
>
>The room key is a small RFID card. Your room is on the 25th floor and the elevators are also temporarily out of service, so it takes what little energy you have left to even climb the stairs and navigate the halls. You finally reach the door to your room, swipe your card, and - beep - the light turns red.
>
>Examining the card more closely, you discover a phone number for tech support.
>
>"Hello! How can we help you today?" You explain the situation.
>
>"Well, it sounds like the card isn't sending the right command to unlock the door. If you go back to the check-in desk, surely someone there can reset it for you." Still catching your breath, you describe the status of the elevator and the exact number of stairs you just had to climb.
>
>"I see! Well, your only other option would be to reverse-engineer the cryptographic handshake the card does with the door and then inject your own commands into the data stream, but that's definitely impossible." You thank them for their time.
>
>Unfortunately for the door, you know a thing or two about cryptographic handshakes.
>
>The handshake used by the card and the door involves an operation that transforms a subject number. To transform a subject number, start with the value 1. Then, a number of times called the loop size, perform the following steps:
>
>Set the value to itself multiplied by the subject number.
>Set the value to the remainder after dividing the value by 20201227.
>The card always uses a specific, secret loop size when it transforms a subject number. The door always uses a different, secret loop size.
>
>The cryptographic handshake works like this:
>
>- The card transforms the subject number of 7 according to the card's secret loop size. The result is called the card's public key.
>- The door transforms the subject number of 7 according to the door's secret loop size. The result is called the door's public key.
>- The card and door use the wireless RFID signal to transmit the two public keys (your puzzle input) to the other device. Now, the card has the door's public key, and the door has the card's public key. Because you can eavesdrop on the signal, you have both public keys, but neither device's loop size.
>- The card transforms the subject number of the door's public key according to the card's loop size. The result is the encryption key.
>- The door transforms the subject number of the card's public key according to the door's loop size. The result is the same encryption key as the card calculated.
>
>If you can use the two public keys to determine each device's loop size, you will have enough information to calculate the secret encryption key that the card and door use to communicate; this would let you send the unlock command directly to the door!
>
>For example, suppose you know that the card's public key is 5764801. With a little trial and error, you can work out that the card's loop size must be 8, because transforming the initial subject number of 7 with a loop size of 8 produces 5764801.
>
>Then, suppose you know that the door's public key is 17807724. By the same process, you can determine that the door's loop size is 11, because transforming the initial subject number of 7 with a loop size of 11 produces 17807724.
>
>At this point, you can use either device's loop size with the other device's public key to calculate the encryption key. Transforming the subject number of 17807724 (the door's public key) with a loop size of 8 (the card's loop size) produces the encryption key, 14897079. (Transforming the subject number of 5764801 (the card's public key) with a loop size of 11 (the door's loop size) produces the same encryption key: 14897079.)
>
>What encryption key is the handshake trying to establish?
>
>Your puzzle answer was **545789**.

I thought this problem was so straightforward that I wrote methods as I read the problem:

1. I updated my standard `read_data(file_path)` method to store its `data` array elements as `int` instead of `str` by changing `data.append(line.rstrip())` to `data.append(int(line.rstrip()))`.
2. I wrote a `transform_subject_number(...)` method based on the instructions:
    ```
    def transform_subject_number(loop_size, subject_number):
        value = 1
        for loop in range(loop_size):
            value *= subject_number
            value %= 20201227
        return value
    ```
3. I wrote a `find_secret_loop_size(...)` method, first _so_ inefficiently that I started to believe my rival's assertions that "_`7` isn't the subject number for the REAL data_". Eventually, after learning that the top of the leaderboard solved today's problem in 2 minutes, I trusted my initial instincts that this was straightforward and updated my method to be more efficient:
    ```
    def find_secret_loop_size(public_key, subject_number):
        value = 1
        loop = 0
        while value != public_key:
            loop += 1
            value *= subject_number
            value %= 20201227
        return loop
    ```
4. I wrote a `calculate_encryption_key` method which is really just a wrapper for `transform_subject_number`. The only benefit here was that I wouldn't get as confused on where to plug in the subject number versus the public key and I'd be able to change the logic easily if Part 2 threw some twist at us.
    ```
    def calculate_encryption_key(device_1_public_key,device_2_loop_size):
        return transform_subject_number(device_2_loop_size,device_1_public_key)
    ```
5. Lastly, I simply ran the program by (A) reading the public keys from file, (B) finding the secret loop size for device 2, and (C) calculating the encryption key with device 1's public key and device 2's secret loop size:
    ```
    file_path = "day25.txt"
    
    data = read_data(file_path)

    pk1 = data[0]
    pk2 = data[1]

    ls2 = find_secret_loop_size(pk2,7)

    ek = calculate_encryption_key(pk1,ls2)

    print("Encryption Key: {0}\n\n".format(ek))
    ```

## Part 2
>--- Part Two ---
>
>The light turns green and the door unlocks. As you collapse onto the bed in your room, your pager goes off!
>
>"It's an emergency!" the Elf calling you explains. "The soft serve machine in the cafeteria on sub-basement 7 just failed and you're the only one that knows how to fix it! We've already dispatched a reindeer to your location to pick you up."
>
>You hear the sound of hooves landing on your balcony.
>
>The reindeer carefully explores the contents of your room while you figure out how you're going to pay the 50 stars you owe the resort before you leave. Noticing that you look concerned, the reindeer wanders over to you; you see that it's carrying a small pouch.
>
>"Sorry for the trouble," a note in the pouch reads. Sitting at the bottom of the pouch is a gold coin with a little picture of a starfish on it.
>
>Looks like you only needed 49 stars after all.
>
>Both parts of this puzzle are complete! They provide two gold stars: **

There wasn't really a Part 2 -- it just required you to have completed all of the _other_ Part 2s. Luckily for me, not only did I wrap up my last outstanding Part 2 yesterday (for Day 19), but I also beat my crepe-maker at today's Part 1, so I nabbed a lot of stars today! ✨