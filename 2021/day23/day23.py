from heapq import heappop, heappush

def read(file):
    with open(file) as f:
        lines = f.read().splitlines()
    
    Corridor.depth = len(lines) - 2
    Corridor.length = len(lines[0]) - 2
    positions = {}
    for y,line in enumerate(lines[2:-1]):
        for x,c in enumerate(line[1:]):
            if c != ' ' and c != '#':
                positions[(x,y+1)] = c

    return Corridor(positions)


def hashdict(d):
    return tuple((k,d[k]) for k in sorted(d))


class Corridor():
    length = 11
    depth = 3
    rooms = { 'A': (2,0), 'B': (4,0), 'C': (6,0), 'D': (8,0) }
    energies = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }

    def __init__(self, positions: dict):
        self.p = positions

    def __lt__(self, other):
        return False

    def __repr__(self):
        return "\n" + repr(self.p) + "\n"


    def get(self, x, y=None):
        if x is not None and y is not None:
            yield ((x,y), self.p.get((x,y), None))
        elif x is not None:
            yield from ((c,a) for c,a in self.p.items() if c[0] == x)
        elif y is not None:
            yield from ((c,a) for c,a in self.p.items() if c[1] == y)
        else:
            yield from self.p.items()

    def owner(self, pos):
        return next(a for a,p in self.rooms.items() if p[0] == pos[0])

    def room(self, amphi):
        return { a for a in self.get(self.rooms[amphi][0]) }

    def corridor(self):
        return { a for a in self.get(None,0) }

    def between(self, start, end):
        if start[0] > end[0]:
            start,end = end,start
        return { c for c,a in self.corridor() if start[0]<c[0]<end[0] }

    def around(self, middle):
        start = 0
        end = self.length
        for (x,y),_ in self.corridor():
            if start<=x<middle[0]:
                start = x + 1
            elif middle[0]<x<=end:
                end = x
        return { (pos,0) for pos in range(start,end) }


    def ismixed(self, amphi):
        return any(a != amphi for c,a in self.room(amphi))

    def isfull(self, amphi):
        return sum(a == amphi for c,a in self.room(amphi)) == (self.depth - 1)

    def issolved(self):
        return all(self.isfull(a) for a in self.rooms)


    def solve(self):
        cache = {}
        queue = []
        corridor = self
        energy = 0

        while not corridor.issolved():
            for coord in corridor.p:
                if coord[1] == 0:
                    node = corridor.enter(coord)
                    nodes = [node] if node[0] >=0 else []
                else:
                    nodes = corridor.exit(coord)
                
                for e,c in nodes:
                    
                    e += energy
                    chash = hashdict(c.p)
                    cenergy = cache.get(chash, -1)
                    if 0<=cenergy<=e:
                        # Faster route allready found for this arrangement
                        continue

                    cache[chash] = e
                    heappush(queue, (e,c))

            energy, corridor = heappop(queue)

        return energy


    def enter(self, pos):
        amphi = self.p[pos]

        if self.ismixed(amphi):
            # Incorrect amphis in the room - don't enter
            return -1, None

        endpos = self.rooms[amphi]
        if any(self.between(pos, endpos)):
            # Amphis in the way - don't move
            return -1, None

        depth = self.depth - len(self.room(amphi)) - 1
        steps = abs(endpos[0] - pos[0]) + depth
        energy = steps * self.energies[amphi]
        
        positions = self.p.copy()
        positions.pop(pos)
        positions[(endpos[0], depth)] = amphi

        return energy, Corridor(positions)


    def exit(self, pos):
        amphi = self.p[pos]
        owner = self.owner(pos) 
        depth = self.depth - len(self.room(owner))

        if not self.ismixed(owner) or depth != pos[1]:
            # Room is only correct amphis, or pos is not first - don't exit
            return
        
        endpositions = self.around(pos) - set(self.rooms.values())
        for endpos in endpositions:
            steps = abs(endpos[0] - pos[0]) + depth
            energy = steps * self.energies[amphi]

            positions = self.p.copy()
            positions.pop(pos)
            positions[endpos] = amphi

            yield energy, Corridor(positions)


corridor1 = read('input1.txt')
print("Part 1:")
energy1 = corridor1.solve()
print(f"  Energy: {energy1}")
corridor2 = read('input2.txt')
print("Part 2:")
energy2 = corridor2.solve()
print(f"  Energy: {energy2}")