"""
breadth first search maze runner with super cool and epic stuffs yaya
"""

yayaya = "maze_runner.txt"

def yaya(yaya):
    yayayaya = []
    with open(str(yaya), "r") as ayay:
        for line in ayay:
            ayayaya = []
            for char in line:
                if char != "\n":
                    ayayaya.append(char)
            yayayaya.append(ayayaya)
    ayay.close()
    return yayayaya

map = yaya(yayaya)

def search_map(map):
    next_up = []
    start = map[1][1]
    cur_pos = start
    step = 1
    x = 1
    y = 1
    searched = {}
    while cur_pos != "E":
        if map[x - 1][y] != "#" and (x - 1, y) not in searched:
            next_up.append([map[x - 1][y], [x - 1, y]])
        elif (x - 1, y) in searched:
            if searched[(x - 1, y)] < step:
                step = searched[(x - 1, y)] + 1
        if map[x + 1][y] != "#" and (x + 1, y) not in searched:
            next_up.append([map[x + 1][y], [x + 1, y]])
        elif (x + 1, y) in searched:
            if searched[(x + 1, y)] < step:
                step = searched[(x + 1, y)] + 1
        if map[x][y - 1] != "#" and (x, y - 1) not in searched:
            next_up.append([map[x][y - 1], [x, y - 1]])
        elif (x, y - 1) in searched:
            if searched[(x, y - 1)] < step:
                step = searched[(x, y - 1)] + 1
        if map[x][y + 1] != "#" and (x, y + 1) not in searched:
            next_up.append([map[x][y + 1], [x, y + 1]])
        elif (x, y + 1) in searched:
            if searched[(x, y + 1)] < step:
                step = searched[(x, y + 1)] + 1
        searched[x, y] = step
        step += 1
        cur_pos = next_up[0][0]
        x = next_up[0][1][0]
        y = next_up.pop(0)[1][1]
        print(f"cur_pos: {cur_pos}, x: {x}, y: {y}")
    print(searched)

search_map(map)

wait = input()