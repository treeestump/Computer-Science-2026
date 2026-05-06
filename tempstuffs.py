"""
FUNCTION temp_check_yaya(yaya):

    SET highest TO 0
    SET lowest TO 0
    SET total TO 0

    FOR each value i IN yaya:
        TRY:
            CONVERT i TO float
            ADD i TO total

            IF i < lowest:
                SET lowest TO i

            IF i > highest:
                SET highest TO i

        IF conversion fails:
            DO nothing (skip value)

    DIVIDE total BY length of yaya

    RETURN "Average: total, lowest: lowest, highest: highest"
"""

yaya = (10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)

def temp_check_yaya(yaya):
    highest = 0
    lowest = 0
    total = 0
    for i in yaya:
        try:
            i = float(i)
            total += i
            if i < lowest:
                lowest = i
            if i > highest:
                highest = i
        except ValueError:
            pass
        
    total /= len(yaya)
    return f"Average: {total}, lowest: {lowest}, highest: {highest}"

print(temp_check_yaya(yaya))

wait = input("")