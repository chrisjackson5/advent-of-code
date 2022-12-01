def read(file):
    with open(file) as f:
        lines = f.read().splitlines()

    height = len(lines)
    width = len(lines[0])
    rights = { (x,y) for y,line in enumerate(lines) for x,c in enumerate(line) if c==">" }
    downs = { (x,y) for y,line in enumerate(lines) for x,c in enumerate(line) if c=="v" }

    return rights, downs, width, height


def draw(rights, downs, width, height):

    floor = [[">" if (x,y) in rights else ("v" if (x,y) in downs else ".") for x in range(0,width)] for y in range(0,height)]
    d = "\n".join("".join(row) for row in floor )
    print(d)


def step(rights, downs, width, height):    
    rmoves = { ((x+1) % width, y) for x,y in rights } - rights - downs
    rmoved = { ((x-1) % width, y) for x,y in rmoves }
    rights -= rmoved
    rights |= rmoves


    dmoves = { (x, (y+1) % height) for x,y in downs } - rights - downs
    dmoved = { (x, (y-1) % height) for x,y in dmoves }
    downs -= dmoved
    downs |= dmoves

    return (len(rmoves) + len(dmoves)) > 0


def count(rights, downs, width, height):
    moves = 1
    while step(rights, downs, width, height):
        moves += 1

    return moves


params = read('input.txt')
print("Part 1:")
count1 = count(*params)
print(f"  Count: {count1}")