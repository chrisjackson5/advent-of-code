def read(file):
    with open(file) as f:
        data = f.read()

    sections = data.split('\n\n')
    scanners = [Scanner.read(s.splitlines()) for s in sections]
    return scanners


class Scanner():
    def __init__(self, scanners, beacons):
        self.scanners = scanners
        self.beacons = beacons

    @classmethod
    def read(cls, section):
        scanner = section[0][12:-4]
        beacons = {
                    (int(x), int(y), int(z)) for x,y,z in 
                        (line.split(',') for line in section[1:])
                }
        return cls([scanner], beacons)

    @property
    def rotations(self):
        rotations = [[
                (x,y,z), (x,z,-y), (x,-y,-z), (x,-z,y),
                (y,z,x), (y,x,-z), (y,-z,-x), (y,-x,z),
                (z,x,y), (z,y,-x), (z,-x,-y), (z,-y,x)
            ] for x,y,z in self.beacons]
        rotations = [set(r) for r in zip(*rotations)]
        reverse = [{(-x,y,-z) for x,y,z in beacons} for beacons in rotations]
        return rotations + reverse

    def combine(self, other):
        for rot in other.rotations:
            for x,y,z in self.beacons:
                for rx,ry,rz in rot:
                    dx,dy,dz = x-rx, y-ry, z-rz
                    offset = { (i+dx, j+dy, k+dz) for i,j,k in rot }
                    matches = self.beacons & offset
                    if len(matches) >= 12:
                        combined = self.beacons | offset
                        scanners = self.scanners + other.scanners
                        return Scanner(scanners, combined), (dx,dy,dz)

        return None, None


def combine_all(scanners):
    combined = scanners[0]
    remaining = scanners[1:]
    offsets = {}

    while len(remaining) > 0:
        anyCombined = False
        for i,other in enumerate(remaining):
            c,offset = combined.combine(other)
            if c is not None:
                anyCombined = True
                combined = c
                offsets[other.scanners[0]] = offset
                remaining.pop(i)

        if not anyCombined:
            raise SystemError("No matches found.")

    return combined, offsets


def parts(scanners):
    combined, offsets = combine_all(scanners)
    count = len(combined.beacons)

    positions = [(0,0,0)] + [o for o in offsets.values()]
    deltas = []
    for i,(ix,iy,iz) in enumerate(positions):
        for jx,jy,jz in positions[i+1:]:
            delta = jx-ix, jy-iy, jz-iz
            deltas.append(delta)

    distance = max(abs(x)+abs(y)+abs(z) for x,y,z in deltas)

    return count, distance


scanners = read('input.txt')
count, distance = parts(scanners)
print("Part 1: ")
print(f"  Count: {count}")
print("Part 2:")
print(f"  Distance: {distance}")
