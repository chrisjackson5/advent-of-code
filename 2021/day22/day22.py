def read(file):
    with open(file) as f:
        lines = f.read().splitlines()
    
    instructions = []
    for line in lines:
        cmd, range = line.split(' ')
        cmd = cmd == 'on'
        range = (r[2:].split('..') for r in range.split(','))
        cube = Cuboid(*((int(start), int(end)) for start,end in range))
        instructions.append((cmd, cube))

    return instructions


class Cuboid():
    def __init__(self, *range):
        self.x,self.y,self.z = range

    def __repr__(self):
        return f'Cuboid({self.x}, {self.y}, {self.z})'

    @property
    def range(self):
        return (self.x, self.y, self.z)

    @property
    def vertices(self):
        return tuple((self.x[i], self.y[i], self.z[i]) for i in (0,1))

    @property
    def cells(self):
        return { (x,y,z) for x in range(self.x[0], self.x[1]+1)
                         for y in range(self.y[0], self.y[1]+1)
                         for z in range(self.z[0], self.z[1]+1) }

    def size(self):
        return (self.x[1]-self.x[0]+1) * (self.y[1]-self.y[0]+1) * (self.z[1]-self.z[0]+1)

    def remove(self, other):
        if not self.isintersect(other):
            yield self
            return

        c1 = ((self.x[0], other.x[0]-1), self.y, self.z)
        c2 = ((other.x[1]+1, self.x[1]), self.y, self.z)

        c3 = ((max(self.x[0], other.x[0]),min(self.x[1], other.x[1])), (self.y[0], other.y[0]-1), self.z)
        c4 = (c3[0], (other.y[1]+1, self.y[1]), self.z)

        c5 = (c3[0], (max(self.y[0], other.y[0]),min(self.y[1], other.y[1])), (self.z[0], other.z[0]-1))
        c6 = (c3[0], c5[1], (other.z[1]+1,self.z[1]))

        for c in (c1,c2,c3,c4,c5,c6):
            if self.isvalid(c):
                yield Cuboid(*c)

    def intersect(self, other):
        if not self.isintersect(other):
            return None

        irange = ((max(s[0],o[0]), min(s[1],o[1])) for s,o in zip(self.range, other.range))
        return Cuboid(*irange)

    def combine(self, other):
        yield self
        yield from other.remove(self)

    def isintersect(self, other):
        return (self.x[1] >= other.x[0] and self.x[0] <= other.x[1] and 
                self.y[1] >= other.y[0] and self.y[0] <= other.y[1] and
                self.z[1] >= other.z[0] and self.z[0] <= other.z[1])

    @classmethod
    def isvalid(cls, range):
        return all(start <= end for start,end in range)


def execute(instruction, cubes, limits=None):
    cmd, icube = instruction
    if limits:
        icube = icube.intersect(limits)
        if not icube:
            return cubes

    if cmd:
        additions = [icube]
        for c in cubes:
            additions = [split for addition in additions for split in addition.remove(c)]
        cubes.extend(additions)
    else:
        cubes = [split for c in cubes for split in c.remove(icube)]
    
    return cubes


def part1(instructions):
    lim = (-50,50)
    limits = Cuboid(lim,lim,lim)
    cubes = []
    for instruction in instructions:
        cubes = execute(instruction, cubes, limits)
    
    return sum(c.size() for c in cubes)


def part2(instructions):
    cubes = []
    for instruction in instructions:
        cubes = execute(instruction, cubes)
    
    return sum(c.size() for c in cubes)


instructions = read('input.txt')
print('Part 1:')
count1 = part1(instructions)
print(f'  Count: {count1}')
print('Part 2:')
count2 = part2(instructions)
print(f'  Count: {count2}')