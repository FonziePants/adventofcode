# --- Day 2: Password Philosophy ---

class PasswordEntry:
    def __init__(self, full_line):
        # default values
        self.password = ""
        self.required_character = ''
        self.min_required_character = 0
        self.max_required_character = 0
        self.first_character_position = -1
        self.second_character_position = -1

        entry_elements = full_line.split()
        if len(entry_elements) == 3:
            self.password = entry_elements[2]
            self.required_character = entry_elements[1].replace(":","")
            character_range = entry_elements[0].split("-")
            if len(character_range) == 2:
                self.min_required_character = int(character_range[0])
                self.max_required_character = int(character_range[1])
                self.first_character_position = self.min_required_character-1
                self.second_character_position = self.max_required_character-1
        else:
            print("WARNING: invalid password; there were " + str(len(entry_elements))) + " entry elements instead of 3."
    
    def print(self):
        print("Password: " + self.password)
        print("Required Character: " + self.required_character)
        print("Required Character Occurrences: " + str(self.min_required_character) + " to " + str(self.max_required_character))
        if self.is_valid_part1():
            print("This password is valid by the old standards.")
        else:
            print("This password is not valid by the old standards.")
        if self.is_valid_part2():
            print("This password is valid by the new standards.")
        else:
            print("This password is not valid by the new standards.")
    
    def is_valid_part1(self):
        character_count = self.password.count(self.required_character)
        return character_count >= self.min_required_character and character_count <= self.max_required_character
    
    def is_valid_part2(self):
        password_length = len(self.password)
        if self.first_character_position < 0 or self.second_character_position < 0 or self.first_character_position >= password_length or self.second_character_position >= password_length:
            # out of bounds error
            return False

        first_position_contains_character = self.password[self.first_character_position] == self.required_character

        second_position_contains_character = self.password[self.second_character_position] == self.required_character

        return first_position_contains_character != second_position_contains_character

def create_password_list(input_file):
    # open file
    file = open(input_file, "r")

    # create password list line by line
    password_list = []
    for line in file:
        password_list.append(PasswordEntry(line))
    
    file.close()
    
    return password_list

def count_valid_passwords(input_file):
    valid_password_count = 0
    password_list = create_password_list(input_file)

    for password_entry in password_list:
        if password_entry.is_valid_part2():
            valid_password_count += 1

    print(str(valid_password_count) + " of " + str(len(password_list)) + " are valid.")

count_valid_passwords("day02.txt")