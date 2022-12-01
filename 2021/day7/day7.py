def read(file):
    with open(file) as f:
        crabs = list(map(int, f.read().split(',')))

    return crabs


def part1(crabs):
    start = min(crabs)
    end = max(crabs)

    minPos = -1
    minFuel = 0
    for pos in range(start, end+1):
        fuel = sum(abs(crab-pos) for crab in crabs)
        if not minFuel or fuel < minFuel:
            minPos = pos
            minFuel = fuel

    return minPos, minFuel


def part2(crabs):
    start = min(crabs)
    end = max(crabs)

    minPos = -1
    minFuel = 0
    for pos in range(start, end+1):
        steps = (abs(crab-pos) for crab in crabs)
        fuel = sum(((step+1) * step/2) for step in steps)
        if not minFuel or fuel < minFuel:
            minPos = pos
            minFuel = fuel

    return minPos, minFuel


crabs = read('input.txt')
print("Part1:")
minPos1, minFuel1 = part1(crabs)
print(f"  pos: {minPos1}")
print(f"  fuel: {minFuel1}")

print("Part2:")
minPos2, minFuel2 = part2(crabs)
print(f"  pos: {minPos2}")
print(f"  fuel: {minFuel2}")