j = "BALLOON"
g = "BALLfdfdadfOON"
d = "BALLfdfdadfONBALLfdBfOdadfONALLfdfdadf)N"

chars = ["B", "A", "L", "O", "N"]

def count_chars(s):
    count = []
    count.append(s.count("B"))
    count.append(s.count("A"))
    count_l = s.count("L")
    if count_l % 2 == 0 and count_l != 1:
        count.append(count_l / 2)
        count.append(count_l / 2)
    elif (count_l - (count_l % 2)) % 2 == 0:
        count.append((count_l - (count_l % 2)) / 2)
        count.append((count_l - (count_l % 2)) / 2)
    else:
        count.append(1)
        count.append(0)

    count_o = s.count("O")
    if count_o % 2 == 0 and count_o != 1:
        count.append(count_o / 2)
        count.append(count_o / 2)
    elif (count_o - (count_o % 2)) % 2 == 0:
        count.append((count_o - (count_o % 2)) / 2)
        count.append((count_o - (count_o % 2)) / 2)
    else:
        count.append(1)
        count.append(0)
    count.append(s.count("N"))

    print(count)
    min_val = min(count)
    if min_val > 0:
        return min_val
    else:
        return -1

def find_balloon(s):
    for i in s:
        if i not in chars:
            s = s.replace(i, "")

    return count_chars(s)



print(find_balloon(d))