# --- Day 1: Report Repair ---

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