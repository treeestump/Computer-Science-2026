 #seperates each problem with its number cus im too lazy to type that every time
number = 1
def newproblem(number):
    print()
    print(f"Problem #{number}")
    print()
    return number + 1

#nums one to ten

number = newproblem(number)

for n in range(0, 10):
    print(n + 1)

#even nums 1 to 20

number = newproblem(number)

for n in range(1, 21):
    if n % 2 == 0:
        print(n)

#sum of numbers 1 to 100

number = newproblem(number)

total = 0

for n in range(1, 101):
    total += n

print(total)

#chars in "Hello, world!"

number = newproblem(number)

helloworld = "Hello, world!"

for n in helloworld:
    print(n)

#10 elements of the fibinacci sequence

number = newproblem(number)

previous = 0
current = 0

for n in range(1, 11):
    print(current)
    newprev = current
    current = previous + current
    previous = newprev
    if current == 0:
        current = 1

#star triangle

number = newproblem(number)

for n in range(1, 6):
    print("*" * n)

#10 to 1

number = newproblem(number)

for n in range(10, 0, -1):
    print(n)

#every third num 3 to 30

number = newproblem(number)

step = 0

for n in range(3, 31):
    if step == 0:
        print(n)
        step = 3
    step -= 1

#factorials of given num

number = newproblem(number)

dumb = True

while dumb == True:
    try:
        num = input("number: ")
        num = int(num)
        dumb = False
    except ValueError:
        dumb = True
        print("integer please dumb")

total = 1

for n in range(num, 1, -1):
    total *= n

print(total)

#pyramid 12345 pattern thing

number = newproblem(number)

thingy = ""

for n in range(1, 6):
    thingy += str(n)
    print(thingy)

#while loop time

number = 1
print("---------------")
print("While loop time")
print("---------------")

#constant input until negative number

number = newproblem(number)

dumb = True
tries = 1

while dumb == True:
    num = input("Number: ")
    try:
        if float(num) < 0:
            dumb = False
            print(f"Congradulations, that took {tries} tries")
        else:
            print("lower silly")
    except ValueError:
        dumb = True
        print("Numbers please silly goose.")
    tries += 1

#password is secret

number = newproblem(number)

tries = 0
password = ""

while password != "secret":
    tries += 1
    password = input("Password: ")
    if tries == 3:
        print("Taking a while aren't you?")
    elif tries == 5:
        print("Heres a hint, the password is secret")
    elif tries == 8:
        print("The password is secret")
    elif tries == 10:
        print("You're a lost cause")

print(f"Correct!, only took you {tries} tries")

#random number until over 90

number = newproblem(number)

import random

num = random.randint(1, 100)

while num < 90:
    num = random.randint(1, 100)
    print(num)

#sum of even nums until 0 is inputed

number = newproblem(number)

num = 1
total = 0

while num != 0:
    num = input("Even numbers only: ")
    try:
        num = int(num)
        if num % 2 == 0:
            total += num
    except:
        pass
    
print(total)

#guessing game

number = newproblem(number)

wanttoplay = input("Want to play? ")
play = True
randnum = random.randint(1, 100)
tries = 1

if wanttoplay.lower() == "no" or wanttoplay.lower() == "n":
    play = False

while play == True:
    try:
        guess = input("Guess: ")
        guess = int(guess)
        if guess < randnum:
            print("Try higher.")
        elif guess > randnum:
            print("Try lower.")
        elif guess == randnum:
            print(f"Correct, you guessed it in {tries} tries!")
            play = False
        tries += 1
    except ValueError:
        print("Please only enter an integer.")

#print all nums between two inputed ints

number = newproblem(number)

dumb = True

while dumb == True:
    try:
        num1 = input("Integer: ")
        num2 = input("Another integer: ")
        num1 = int(num1)
        num2 = int(num2)
        if num1 > num2:
            for n in range(num2, num1 + 1):
                print(n)
        elif num2 > num1:
            for n in range(num1, num2 + 1):
                print(n)
        else:
            print(num1)
        dumb = False
    except ValueError:
        print("Must be integers.")
        dumb = True

#10 primes

number = newproblem(number)

done = False
minosPrime = 1 #sneaky lil ultrakill refrence
step = 1


def check_prime(n):
    if n <= 1:
        return False
    else:
        sisyphusPrime = True #another ultrakill refrence :P
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                sisyphusPrime = False
                break
    return sisyphusPrime

while done == False:
    prime = check_prime(minosPrime)
    if prime == True:
        print(minosPrime)
        step += 1
    minosPrime += 1
    if step == 10:
        done = True

#vowles in string

number = newproblem(number)

sentance = input("stuff: ")

vowels = {
    "a": 0,
    "e": 0,
    "i": 0,
    "o": 0,
    "u": 0
}

for char in sentance:
    if char.lower() in vowels:
        vowels[char.lower()] += 1

print(vowels)

#tacocat but number

number = newproblem(number)

dumb = True

while dumb == True:
    try:
        num = input("Integer pretty please: ")
        num = int(num)
        if num > 0:
            dumb = False
        else:
            dumb = True
    except ValueError:
        dumb = True
        print("Integer silly, and positive please!")

newnum = ""
numlist = []

for char in str(num):
    numlist.append(char)

for char in range(len(str(num)) - 1, -1, -1):
    newnum += numlist[char]

if str(newnum) == str(num):
    print("This is a palindrome!")
else:
    print("No tacocat or racecar for you :(")

#star pyramid but start at two

number = newproblem(number)

for n in range(2, 6):
    print("*" * n)

#used for seeing the output when run by opening the file, otherwise it closes as soon as it finishes
wait = input()