import pickle

grades = [[183], [1], [23]]
people = {}

p1name = input("Who is the first person: ")
p2name = input("Who is the second person: ")
p3name = input("Who is the third person: ")

people = {
    p1name: 0,
    p2name: 1,
    p3name: 2
}

poop = True

file_path = "grade_save.pickle"

#save function, edits the save files in binary and puts the variable values into the file
def save():
    global grades
    with open(file_path, "wb") as file:
        pickle.dump(grades, file)

#load function, reads the save files and converts the binary into python values wich the variables are then set to
def load():
    global grades
    with open(file_path, "rb") as file:
        grades = pickle.load(file)

load()

def change_grades(grades, people, name):
    splitted = input("Grades: ")
    splitter = splitted.split(", ")
    grades[people[name]] = []
    try:
        for n in range(0, len(splitter)):
            grades[people[name]].append(float(splitter[n]))
    except:
        print(f"Grades must only contain numbers")
    save()

def averagegrade(grades, people, what_do):
    try:
        total_sum = 0
        for num in grades[people[what_do]]:
            total_sum += num
        total_sum /= 4
        print(f"{what_do}'s average grade is {total_sum}")
    except:
        print(f"Could not find {what_do}'s average grade.")

def main(grades, people):
    global poop
    what_do = input("Name of student: ")
    what_do = what_do.lower()
    try:
        print(f"{what_do}'s current grades are: {grades[people[what_do]]}")
        averagegrade(grades, people, what_do)
    except:
        print(f"Cant find student {what_do}")
        return
    name = what_do
    what_do = input(f"Would you like to change one of {name}'s grades?(Y/N): ")
    if what_do.lower() == "y":
        change_grades(grades, people, name)
    what_do = input("Continue?(Y/N): ")
    if what_do.lower() == "y":
        pass
    else:
        poop = False


while poop == True:
    main(grades, people)
