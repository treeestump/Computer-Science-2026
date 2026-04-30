totalSlots = 120
occupied = 0
garageCode = "G"
ratePerHour = 2.50
isWeekend = False

def generate_ticket(vehicle_plate, hoursText):
    global totalSlots 
    global occupied 
    global garageCode 
    global ratePerHour 
    global isWeekend 
    localHours = int(hoursText)
    if occupied >= totalSlots:
        return "Garage Full"
    
    if isWeekend == True:
        localRate = 3.00
    else:
        localRate = ratePerHour
    localCost = localHours * localRate
    ticket = garageCode + "-" + vehicle_plate + "-" + str(occupied)
    file = open("tickets.txt", "a")
    file.write("\n" + ticket + ", " + str(localCost))
    file.close()
    occupied += 1
    return (ticket + " costs " + str(localCost))

print(generate_ticket("AB12CD", "2"))
print(generate_ticket("ZZ99YY", "4"))
isWeekend = True
print(generate_ticket("K1NG", "3"))


wait = input()
