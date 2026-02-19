l1 = [3, 6, 9, 12, 15, 18, 21] 
l2 = [4, 8, 12, 16, 20, 24, 28]
l3 = []

def makeyippeelist(one, two):
    yippee = []
    done = False
    indexnum = 0
    while done == False:
        try:
            if indexnum % 2 == 0:
                yippee.append(two[indexnum])
            else:
                yippee.append(one[indexnum])
            indexnum += 1
        except IndexError:
            if len(one) > len(two):
                if indexnum > len(one) - 1:
                    done = True
            else:
                if indexnum > len(two) - 1:
                    done = True
            indexnum += 1
        
    #code for if it was wanting the odd numbers rather than odd indexes
    """
    for element in one:
        if element % 2 != 0:
            yippee.append(element)
    for element in two:
        if element % 2 == 0:
            yippee.append(element)
    """
    return yippee

l3 = makeyippeelist(l1, l2)
print(l3)
wait = input("")