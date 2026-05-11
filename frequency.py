
file = "testingstuffs.txt"

def count_words(file):
    listyay = []
    words = {}
    with open(file) as stuff:

        listofwords = stuff.read().translate(str.maketrans({"!": " ", "@": " ", "#": " ", "$": " ", "%": " ", "^": " ", "&": " ", "*": " ", "(": " ", ")": " ", ",": " ", "<": " ", ".": " ", ">": " ", "?": " ", "/": " ", "_": " ", "+": " ", "=": " ", "[": " ", "]": " ", "{": " ", "}": " ", "|": " ", '"': " ", ":": " ", ";": " ", "`": " ", "~": " ", }))
        listofwords = listofwords.split()

        stuff.close()
    for word in listofwords:
        word = word.lower()
        try:
            words[word] += 1
        except KeyError:
            words[word] = 1
    for key in words:
        if listyay == []:
            listyay.append(key)
            continue
        else:
            num = words[key]
            i = 0
            for word in listyay:
                if words[word] < num:
                    listyay.insert(i, key)
                    break
                i += 1
                if i == len(listyay):
                    listyay.append(key)
                    break
    for word in listyay:
        print(word)


count_words(file)