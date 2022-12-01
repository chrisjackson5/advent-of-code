
def read():
    with open("input.txt") as f:
        return [l.strip() for l in f]

def dofilter(lines, bitIndex, flip=False):
    if len(lines) == 1:
        return lines

    # Count the 1s for the current bit
    countOnes = sum(int(l[bitIndex]) for l in lines)
    # Determine whether the bit to keep should be a 1 or 0
    shouldBeOne = (countOnes < len(lines)-countOnes) == flip
    expectedChar = '1' if shouldBeOne else '0'
    return [l for l in lines if l[bitIndex]==expectedChar]
    
def part1(lines):
    # Count the 1s for each bit
    counts = [sum(int(l[i]) for l in lines) for i,c in enumerate(lines[0])]
    # Sum the int value for each bit that there are more 1s than 0s
    gamma = sum(1 << pos for pos,count in enumerate(reversed(counts)) if count > len(lines)-count)
    epsilon = (1 << len(lines[0])) - 1 - gamma
    power = gamma * epsilon

    print("Part1")
    print(f"  gamma: {gamma}")
    print(f"  epsilon: {epsilon}")
    print(f"  power: {power}")

def part2(lines):
    oxys = lines
    co2s = lines
    for i in range(0, len(lines[0])):
        oxys = dofilter(oxys, i, False)
        co2s = dofilter(co2s, i, True)

    oxy = int(oxys[0], 2)
    co2 = int(co2s[0], 2)
    life = oxy*co2

    print("Part2")
    print(f"  oxy: {oxy}")
    print(f"  co2: {co2}")
    print(f"  life: {life}")

lines = read()
part1(lines)
part2(lines)
