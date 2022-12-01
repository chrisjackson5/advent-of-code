from heapq import heappop, heappush
from itertools import chain

def read(file):
    with open(file) as f:
        lines = f.read().splitlines()

    size = sum(c=='.' for c in lines[1])

    rooms = {}
    room_positions = ( i for i in range(0, len(lines[2])) if lines[2][i] != '#' )
    room_owners = 'ABCD'
    for pos,owner in zip(room_positions, room_owners):
        contents = tuple(lines[i][pos] for i in range(len(lines)-2,1,-1))
        rooms[pos-1] = Room(contents, owner, len(contents))

    return Corridor({}, rooms, size)


class Room():
    def __init__(self, contents, owner, size=2):
        self.contents = contents
        self.owner = owner
        self.size = size

    def __repr__(self):
        return f"{self.owner}: { self.contents }"

    def ismixed(self):
        return any(c != self.owner for c in self.contents)

    def ishome(self):
        return sum(c == self.owner for c in self.contents) == self.size

    def leave(self):
        amphi = self.contents[-1]
        steps = self.size - len(self.contents) + 1
        return amphi, steps, Room(self.contents[:-1], self.owner, self.size)

    def enter(self, amphi):
        steps = self.size - len(self.contents)
        return steps, Room(self.contents + (amphi,), self.owner, self.size)


class Corridor():
    def __init__(self, contents, rooms, size=11):
        self.contents = contents
        self.rooms = rooms
        self.size = size

    def __lt__(self, other):
        # Implemented to allow heap to order
        return False

    def __repr__(self):
        str = f"{self.contents}:"
        for pos,room in self.rooms.items():
            str += f"\n  {pos}: {room}"
        return str

    def estimate(self, energies):
        energy = 0
        posindex = { room.owner: pos for pos,room in self.rooms.items() }
        for startpos,room in self.rooms.items():
            for amphi in room.contents:
                roompos = posindex[amphi]
                energy += abs(roompos-startpos) * energies[amphi]
        for startpos,amphi in self.contents.items():
            roompos = posindex[amphi]
            energy += abs(roompos-startpos) * energies[amphi]

        return energy

    def ashashable(self):
        content_hash = tuple( self.contents.get(i,None) for i in range(0,self.size) )
        room_hash = tuple(self.rooms[entrance].contents for entrance in sorted(self.rooms))
        return content_hash, room_hash

    def issolved(self):
        return all(room.ishome() for room in self.rooms.values())

    def domoves(self, energies):
        queue = []
        nodes = {}
        energy = 0
        corridor = self
        while not corridor.issolved():
            exitnodes = corridor.doexits(energies)
            enternodes = corridor.doenters(energies)
            for e,c in chain(exitnodes, enternodes):
                e += energy
                hashable = c.ashashable()
                curenergy = nodes.get(hashable, -1)
                if 0 < curenergy < e:
                    # print(curenergy)
                    # print(e)
                    # print(c)
                    # input("Continue")
                    continue

                nodes[hashable] = e
                estimate = c.estimate(energies)
                heappush(queue, (e+estimate,-estimate,c))
            # for e,c in enternodes:
            #     est = c.estimate(energies)
            #     esum = energy+e+est
            #     heappush(queue, (esum,est,c))

            energy,estimate,corridor = heappop(queue)
            energy += estimate

        return energy

    def doenters(self, energies):
        nodes = []

        # Try enters
        for startpos,amphi in self.contents.items():
            roompos,room = next((p,r) for p,r in self.rooms.items() if r.owner == amphi)
            if room.ismixed():
                # Can't enter until others leave
                continue

            if any(startpos<a<=roompos or roompos<=a<startpos for a in self.contents):
                # There's an amphi in the way.
                continue

            entersteps, room = room.enter(amphi)
            energy = (entersteps + abs(roompos-startpos)) * energies[amphi]
            rooms = self.rooms.copy()
            rooms[roompos] = room
            contents = self.contents.copy()
            contents.pop(startpos)

            corridor = Corridor(contents, rooms)
            nodes.append((energy, corridor))

        return nodes

    def doexits(self, energies):
        mixed_rooms = ( (pos,room) for pos,room in self.rooms.items() if room.ismixed() )
        entrances = set(self.rooms)
        nodes = []
        for roompos,room in mixed_rooms:
            amphi,exitsteps,room = room.leave()

            start,end = 0,self.size
            for k in self.contents:
                if k < roompos:
                    start = max(start,k+1)
                elif k > roompos:
                    end = min(end,k)

            positions = { i for i in range(start, end) } - entrances

            for endpos in positions:
                energy = (exitsteps + abs(endpos - roompos)) * energies[amphi]
                rooms = self.rooms.copy()
                rooms[roompos] = room
                contents = self.contents.copy()
                contents[endpos] = amphi

                corridor = Corridor(contents, rooms)
                nodes.append((energy, corridor))

        return nodes


corridor = read('input2.txt')
print("Part 1:")
energies = { 'A':1, 'B':10, 'C':100, 'D':1000}
energy = corridor.domoves(energies)
print(f"  Energy: {energy}")