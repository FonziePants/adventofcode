# --- Day 4: Passport Processing ---
# You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually valid documentation for travel in most of the world.

# It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport scanners, and the delay could upset your travel itinerary.

# Due to some questionable network security, you realize you might be able to solve both of these problems at the same time.

# The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:

# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)
# Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

# Here is an example batch file containing four passports:

# ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
# byr:1937 iyr:2017 cid:147 hgt:183cm

# iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
# hcl:#cfa07d byr:1929

# hcl:#ae17e1 iyr:2013
# eyr:2024
# ecl:brn pid:760753108 byr:1931
# hgt:179cm

# hcl:#cfa07d eyr:2025 pid:166559648
# iyr:2011 ecl:brn hgt:59in
# The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).

# The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.

# The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.

# According to the above rules, your improved system would report 2 valid passports.

# Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?

# Your puzzle answer was 260.

# --- Part Two ---
# The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data are getting through. Better add some data validation, quick!

# You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.
# Your job is to count the passports where all required fields are both present and valid according to the above rules. Here are some example values:

# byr valid:   2002
# byr invalid: 2003

# hgt valid:   60in
# hgt valid:   190cm
# hgt invalid: 190in
# hgt invalid: 190

# hcl valid:   #123abc
# hcl invalid: #123abz
# hcl invalid: 123abc

# ecl valid:   brn
# ecl invalid: wat

# pid valid:   000000001
# pid invalid: 0123456789
# Here are some invalid passports:

# eyr:1972 cid:100
# hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

# iyr:2019
# hcl:#602927 eyr:1967 hgt:170cm
# ecl:grn pid:012533040 byr:1946

# hcl:dab227 iyr:2012
# ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

# hgt:59cm ecl:zzz
# eyr:2038 hcl:74454a iyr:2023
# pid:3556412378 byr:2007
# Here are some valid passports:

# pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
# hcl:#623a2f

# eyr:2029 ecl:blu cid:129 byr:1989
# iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

# hcl:#888785
# hgt:164cm byr:2001 iyr:2015 cid:88
# pid:545766238 ecl:hzl
# eyr:2022

# iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
# Count the number of valid passports - those that have all required fields and valid values. Continue to treat cid as optional. In your batch file, how many passports are valid?

# Your puzzle answer was 153.

class Constants:
    BIRTH_YEAR = "byr"
    ISSUE_YEAR = "iyr"
    EXPIRATION_YEAR = "eyr"
    HEIGHT = "hgt"
    HAIR_COLOR = "hcl"
    EYE_COLOR = "ecl"
    PASSPORT_ID = "pid"
    COUNTRY_ID = "cid"

    CENTIMETERS = "cm"
    INCHES = "in"

def validate_year(year, min_year, max_year):
    return not ((year is None) or
                (int(year) < min_year) or
                (int(year) > max_year))

class Passport:
    def __init__(self, byr=None, iyr=None, eyr=None, hgt=None, hcl=None, ecl=None, pid=None, cid=None):
        self.birth_year = byr
        self.issue_year = iyr
        self.expiration_year = eyr
        self.height = hgt
        self.hair_color = hcl
        self.eye_color = ecl
        self.passport_id = pid
        self.country_id = cid
    
    def set_value(self,key,value):
        if key == Constants.BIRTH_YEAR:
            self.birth_year = value
        elif key == Constants.ISSUE_YEAR:
            self.issue_year = value
        elif key == Constants.EXPIRATION_YEAR:
            self.expiration_year = value
        elif key == Constants.HEIGHT:
            self.height = value
        elif key == Constants.HAIR_COLOR:
            self.hair_color = value
        elif key == Constants.EYE_COLOR:
            self.eye_color = value
        elif key == Constants.PASSPORT_ID:
            self.passport_id = value
        elif key == Constants.COUNTRY_ID:
            self.country_id = value
        else:
            print("key '" + key + "' was invalid.")

    def valid_birth_year(self):
        return validate_year(self.birth_year, 1920, 2002)
    
    def valid_issue_year(self):
        return validate_year(self.issue_year, 2010, 2020)
    
    def valid_expiration_year(self):
        return validate_year(self.expiration_year, 2020, 2030)
    
    def valid_height(self):
        if (self.height is not None and len(self.height) > 2):
            unit = self.height[-2:]
            value = int(self.height.split(unit)[0])
            if (unit == Constants.CENTIMETERS):
                return value >= 150 and value <= 193
            elif (unit == Constants.INCHES):
                return value >= 59 and value <= 76
        return False
    
    def valid_hair_color(self):
        valid_alpha_hex_chars = ["a", "b", "c", "d", "e", "f"]
        if (    self.hair_color is not None and
                len(self.hair_color) == 7 and
                self.hair_color[0] == "#"
            ):
            for index in range(1,6):
                if not (self.hair_color[index].isdigit() or (self.hair_color[index].lower() in valid_alpha_hex_chars)):
                    return False
            return True
        
        return False
    
    def valid_eye_color(self):
        valid_eye_colors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

        return self.eye_color is not None and self.eye_color in valid_eye_colors
    
    def valid_passport_id(self):
        if self.passport_id is None or len(self.passport_id) != 9:
            return False
        
        for digit in self.passport_id:
            if not digit.isdigit():
                return False
        
        return True
    
    def is_valid(self):
        # only country id is optional
        return (self.valid_birth_year() and
                self.valid_issue_year() and
                self.valid_expiration_year() and
                self.valid_height() and 
                self.valid_hair_color() and 
                self.valid_eye_color() and
                self.valid_passport_id())
    
    def print(self):
        print("Birth Year:      " + str(self.birth_year))
        print("Issue Year:      " + str(self.issue_year))
        print("Expiration Year: " + str(self.expiration_year))
        print("Height:          " + str(self.height))
        print("Hair Color:      " + str(self.hair_color))
        print("Eye Color:       " + str(self.eye_color))
        print("Passport ID:     " + str(self.passport_id))
        print("Country ID:      " + str(self.country_id))

def parse_passports(input_file):
    # open file
    file = open(input_file, "r")

    # create list to store passports
    passport_list = []
    temp_passport_string = ""
    temp_passport = Passport()

    for line in file:
        temp_passport_string += line.rstrip() + " "
        if not line.rstrip():
            temp_passport = create_passport(temp_passport_string)
            passport_list.append(temp_passport)
            temp_passport_string = ""
    
    # add last passport if necessary
    if len(temp_passport_string.rstrip()) > 1:
        temp_passport = create_passport(temp_passport_string)
        passport_list.append(temp_passport)
    
    file.close()

    return passport_list

def create_passport(input_string):
    kvp_list = input_string.replace("  "," ").split()
    temp_passport = Passport()
    for kvp in kvp_list:
        if len(kvp) < 5 or kvp[3] != ":":
            print("kvp is malformed")
            continue
        key = kvp[0:3]
        value = kvp[4:]
        temp_passport.set_value(key, value)
    return temp_passport

def count_valid_passports(passport_list):
    valid_passport_count = 0
    for passport in passport_list:
        if passport.is_valid():
            valid_passport_count += 1

    print(str(valid_passport_count) + " of " + str(len(passport_list)) + " passports are valid")
    return valid_passport_count

passport_list = parse_passports("solutions/day04/day04_real.txt")
count_valid_passports(passport_list)