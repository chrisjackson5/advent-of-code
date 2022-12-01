def read(file):
    with open(file) as f:
        return [(direction, int(amount)) for direction,amount in (l.split(" ") for l in f.readlines())]

def part1(commands):
    depth = 0
    horizontal = 0

    for command, amount in commands:
        if command == "forward":
            horizontal += amount
        elif command == "up":
            depth -= amount
        elif command == "down":
            depth += amount
        else:
            raise KeyError("Invalid command.")

    multiple = depth*horizontal

    print("Part 1:")
    print(f"  horizontal: {horizontal}")
    print(f"  depth: {depth}")
    print(f"  multiple: {multiple}")

def part2(commands):
    aim = 0
    depth = 0
    horizontal = 0

    for command, amount in commands:
        if command == "forward":
            depth += aim*amount
            horizontal += amount
        elif command == "up":
            aim -= amount
        elif command == "down":
            aim += amount
        else:
            raise KeyError("Invalid command.")

    multiple = depth*horizontal

    print("Part 2:")
    print(f"  horizontal: {horizontal}")
    print(f"  depth: {depth}")
    print(f"  aim: {aim}")
    print(f"  multiple: {multiple}")


commands = read('input.txt')
part1(commands)
part2(commands)
