
#first problem
print("")
print("First problem: ")
print("")

data = [10, 20, 30, 40, 50]
n = len(data)

for i in range(n):
    if i == 0:
        last = data[i]
    try:
        data[i] = data[i + 1]
    except IndexError:
        data[i] = last
    
print(data)

#end of first problem

#second problem
print("")
print("Second problem: ")
print("")

stack = []

stack.append("Hello")
stack.append("World")

def undo_removing(stack):
    try:
        print(f"Undo removing: {stack.pop()}")
    except:
        print("No remaining objects in the stack.")
    return stack

stack = undo_removing(stack)
stack = undo_removing(stack)
stack = undo_removing(stack)

print(f"Remaining stack: {stack}")

#end of second problem

#third problem
print("")
print("Third problem: ")
print("")

queue = []

queue.append("Doc A")
queue.append("Doc B")
queue.append("Doc C")

print("Printing...")

while len(queue) > 0:
    print(f"Printint: {queue.pop(0)}")

#end of third problem

#start of challenge
print("")
print("Challenge: ")
print("")

bitcoin_prices = [61240, 61890, 60575, 62150, 63010, 64200, 63520, 64830, 65210, 64050, 63300, 61575, 60990, 59840, 60210, 61050, 62340, 63775, 64520, 65900, 67120, 66350, 65480, 64890, 63610, 62975, 61730, 60820, 59950]

def search_list(list, target):
    for i in range(len(list)-1):
        if list[i] == target:
            return i
        
    return "Could not find"

def sort_list(list):
    for i in range(len(list)-2):
        min = i
        
        for swap in range(i+1, len(list)):
            if list[swap] < list[min]:
                min = swap
        
        
        swappy = list[i]
        list[i] = list[min]
        list[min] = swappy
    return list

print("Search: ")
print(search_list(bitcoin_prices, 63010))
print("Sort: ")
print(sort_list(bitcoin_prices))

#end of challenge

#extra challenge
print("")
print("Extra extra")
print("")
#trying to read csv files and save info as a list
import csv

data = []

file = open("test.csv")
reader = csv.reader(file)
for row in reader:
    for obj in row:
        try:
            data.append(int(obj))
        except ValueError:
            pass

print(data)
