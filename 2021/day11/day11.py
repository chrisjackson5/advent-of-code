def read(file):
    with open(file) as f:
        octopi = [[int(o) for o in line[:-1]] for line in f.readlines()]
        return octopi


def flash(octopi, pos):
    flashes = 0
    x,y = pos
    if octopi[y][x] > 9:
        flashes += 1
        octopi[y][x] = 0
        rows = len(octopi)
        cols = len(octopi[0])

        adj = ((1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1))
        adj = ((x+i, y+j) for i,j in adj)
        for i,j in adj:
            if 0<=i<cols and 0<=j<rows and octopi[j][i] != 0:
                octopi[j][i] += 1
                flashes += flash(octopi, (i,j))

    return flashes


def step(octopi):
    rows = len(octopi)
    cols = len(octopi[0])

    # Increment all octopi
    for y in range(0, rows):
        for x in range(0, cols):
            octopi[y][x] += 1

    flashes = 0
    for y in range(0, rows):
        for x in range(0, cols):
            flashes += flash(octopi, (x,y))

    return flashes


def part1(octopi):
    flashes = 0
    for i in range(0, 100):
        flashes += step(octopi)

    return flashes


def part2(octopi):
    count = len(octopi) * len(octopi[0])
    steps = 0
    flashes = 0
    while flashes != count:
        flashes = step(octopi)
        steps += 1

    return steps


octopi1 = read('input.txt')
octopi2 = [[o for o in row] for row in octopi1]
print("Part 1:")
flashes = part1(octopi1)
print(f"  Flashes: {flashes}")
print("Part 2:")
steps = part2(octopi2)
print(f"  Sync Step: {steps}")