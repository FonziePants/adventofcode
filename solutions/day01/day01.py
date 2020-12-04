# --- Day 1: Report Repair ---
# After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

# The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.

# To save your vacation, you need to get all fifty stars by December 25th.

# Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

# Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

# Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

# For example, suppose your expense report contained the following:

# 1721
# 979
# 366
# 299
# 675
# 1456
# In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

# Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?

# Your puzzle answer was 633216.

# --- Part Two ---
# The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

# Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

# In your expense report, what is the product of the three entries that sum to 2020?

# Your puzzle answer was 68348924.

def generate_list():
    #new_list = [1721, 979, 366, 299, 675, 1456]
    new_list = [1975,1600,113,1773,1782,1680,1386,1682,1991,1640,1760,1236,1159,1259,1279,1739,1826,1888,1072,416,1632,1656,1273,1631,1079,1807,1292,1128,1841,1915,1619,1230,1950,1627,1966,774,1425,1983,1616,1633,1559,1925,960,1407,1708,1211,1666,1910,1960,1125,1242,1884,1829,1881,1585,1731,1753,1784,1095,1267,1756,1226,1107,1664,1710,2000,1181,1997,1607,1889,1613,1859,1479,1763,1692,1967,522,1719,1816,1714,1331,1976,1160,1899,1906,1783,1061,2006,1993,1717,2009,1563,1733,1866,1651,1437,1517,1113,1743,1240,1629,1868,1912,1296,1873,1673,1996,1814,1215,1927,1956,1970,1887,1702,1495,1754,1621,1055,1538,1693,1840,1685,1752,1933,1727,1648,1792,1734,1305,1446,1764,1890,1904,1560,1698,1645,1214,1516,1064,1729,1835,1642,1932,1683,962,1081,1943,1502,1622,196,1972,1916,1850,1205,1971,1937,1575,1401,1351,2005,1917,1670,1388,1051,1941,1751,1169,510,217,1948,1120,1635,1636,1511,1691,1589,1410,1902,1572,1871,1423,1114,1806,1282,1193,1974,388,1398,1992,1263,1786,1723,1206,1363,1177,1646,1231,1140,1088,1322]
    return new_list

def find_product_of_two_2020_addends(entries_list):
    entries_list.sort()
    list_length = len(entries_list)
    for low in range(list_length):
        for high in reversed(range(len(entries_list))):
            if entries_list[low] + entries_list[high] < 2020:
                break
            if entries_list[low] + entries_list[high] == 2020:
                return entries_list[low] * entries_list[high]
    return "no two entries add up to 2020"

def find_product_of_three_2020_addends(entries_list):
    entries_list.sort()
    list_length = len(entries_list)
    entries_dict = {}

    for x in range(list_length):
        entry = entries_list[x]
        if entry in entries_dict:
            entries_dict[entry] = entries_dict[entry] + 1
        else:
            entries_dict[entry] = 1
    
    for low in range(list_length):
        for high in reversed(range(len(entries_list))):
            needed_addend = 2020 - (entries_list[low] + entries_list[high])
            if needed_addend in entries_dict:
                return needed_addend * entries_list[low] * entries_list[high]

    return "no three entries add up to 2020"

print(find_product_of_three_2020_addends(generate_list()))