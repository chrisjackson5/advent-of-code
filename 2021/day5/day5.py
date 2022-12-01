def read():
    with open('input.txt') as f:
        lines = []
        for line in f:
            line = line[:-1]
            startString,endString = line.split(' -> ')
            start = tuple(map(int, startString.split(',')))
            end = tuple(map(int, endString.split(',')))

            lines.append(Line(start, end))

    return lines


class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @property
    def length(self):
        return max(abs(self.dx), abs(self.dy))

    @property
    def dx(self):
        return self.end[0] - self.start[0]

    @property
    def dy(self):
        return self.end[1] - self.start[1]

    @property
    def isperpendicular(self):
        return self.dx == 0 or self.dy == 0

    @property
    def points(self):
        stepx = 1 if self.dx > 0 else (-1 if self.dx < 0 else 0)
        stepy = 1 if self.dy > 0 else (-1 if self.dy < 0 else 0)

        return ((self.start[0] + stepx*i, self.start[1] + stepy*i) for i in range(0, self.length+1))


def draw(floormap, line):
    for x,y in line.points:
        if y not in floormap:
            floormap[y] = {}
        if x not in floormap[y]:
            floormap[y][x] = 0
        floormap[y][x] += 1


def findclouds(lines):
    floormap = {}
    for line in lines:
        draw(floormap, line)

    return [(x,y) for y,row in floormap.items() for x,v in row.items() if v > 1]


def part1(lines):
    lines = filter(lambda l: l.isperpendicular, lines)
    clouds = findclouds(lines)

    return len(clouds)


def part2(lines):
    clouds = findclouds(lines)
    return len(clouds)


lines = read()
print("Part1:")
count1 = part1(lines)
print(f"  count: {count1}")
print("Part2:")
count2 = part2(lines)
print(f"  count: {count2}")