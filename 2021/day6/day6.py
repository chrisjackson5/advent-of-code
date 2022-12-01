from collections import Counter

def read(file):
    with open(file) as f:
        fish = list(map(int, f.read().split(',')))

    return fish


def spawn(fish):
    spawn_count = fish[0]
    for i in range(0,8):
        fish[i] = fish[i+1]
    fish[6] += spawn_count
    fish[8] = spawn_count

    return sum(fish.values())


def part1(fish):
    for day in range(1,81):
        count = spawn(fish)

    return count


def part2(fish):
    for day in range(1,257):
        count = spawn(fish)

    return count


fish = read('input.txt')
print("Part1: ")
count1 = part1(Counter(fish))
print(f"  count: {count1}")

print("Part2: ")
count2 = part2(Counter(fish))
print(f"  count: {count2}")