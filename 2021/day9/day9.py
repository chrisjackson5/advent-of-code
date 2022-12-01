def read(file):
    with open(file) as f:
        floor = [[int(c) for c in line[:-1]] for line in f.readlines()]
        return floor


def get(pos, floor):
    x,y = pos
    return floor[y][x]


def adjacent(pos, floor):
    x,y = pos
    for i,j in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
        if i >= 0 and i < len(floor[0]) and j >= 0 and j < len(floor):
            yield (i,j)


def lows(floor):
    for y, row in enumerate(floor):
        for x, height in enumerate(row):
            heights = (get(pos, floor) for pos in adjacent((x,y), floor))
            if all(height < h for h in heights):
                yield (x, y)


def basin(low, floor):
    basin = { low }
    queue = [ low ]

    while len(queue) > 0:
        cur = queue.pop(0)
        adj = { adj for adj in adjacent(cur, floor) if (get(cur, floor) <= get(adj, floor) < 9) }
        adj -= basin
        queue.extend(adj)
        basin.update(adj)

    return basin


def part1(floor):
    heights = [get(low, floor) for low in lows(floor)]
    risk = sum(h+1 for h in heights)
    return risk


def part2(floor):
    basins = {}
    for low in lows(floor):
        basins[low] = basin(low, floor)

    sizes = sorted((len(b) for b in basins.values()), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


floor = read("input.txt")
print("Part1: ")
risk = part1(floor)
print(f"  Risk: {risk}")
print("Part2: ")
product = part2(floor)
print(f"  Product: {product}")