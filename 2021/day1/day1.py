def read(file):
    with open(file) as f:
        return [int(x) for x in f.readlines()]


def part1(lines):
    count = 0
    for i in range(1, len(lines)):
        if lines[i] > lines[i-1]:
            count += 1

    print("Part 1:")
    print(f"  count: {count}")


def part2(lines):
    increases = 0
    for i in range(3, len(lines)):
        sum1 = sum(lines[i-3:i])
        sum2 = sum(lines[i-2:i+1])
        if sum2 > sum1:
            increases += 1

    print("Part 2:")
    print(f"  increases: {increases}")


lines = read('input.txt')
part1(lines)
part2(lines)