import json
import math
import copy

def read(file):
    with open(file) as f:
        numbers = [json.loads(line) for line in f.read().splitlines()]
    return numbers


def get(num, path):
    cur = num
    for p in path:
        cur = cur[p]
    return cur


def set(num, path, value):
    cur = num
    for p in path[:-1]:
        cur = cur[p]
    cur[path[-1]] = value


def explode(num, path=[]):
    cur = get(num, path)

    if len(path) == 4 and isinstance(cur, list):
        # Do explode
        x,y = cur

        # Set left side
        lpath = path[:]
        while len(lpath) and lpath[-1] == 0:
            lpath.pop()
        if len(lpath):
            lpath[-1] = 0
            cur = get(num, lpath)
            while isinstance(cur, list):
                cur = cur[1]
                lpath.append(1)
            set(num, lpath, cur + x)

        # Set right side
        rpath = path[:]
        while len(rpath) and rpath[-1] == 1:
            rpath.pop()
        if len(rpath):
            rpath[-1] = 1
            cur = get(num, rpath)
            while isinstance(cur, list):
                cur = cur[0]
                rpath.append(0)
            set(num, rpath, cur + y)

        set(num, path, 0)

        return True

    exploded = False
    if isinstance(cur, list):
        exploded = explode(num, path + [0]) or explode(num, path + [1])

    return exploded


def split(num):
    for i in (0,1):
        if isinstance(num[i], list):
            if split(num[i]):
                return True
        elif num[i] > 9:
            num[i] = [math.floor(num[i]/2), math.ceil(num[i]/2)]
            return True

    return False


def reduce(num):
    return explode(num) or split(num)


def add(a, b):
    res = [copy.deepcopy(a), copy.deepcopy(b)]
    while reduce(res):
        pass

    return res


def magnitude(num):
    if not isinstance(num, list):
        return num

    return 3*magnitude(num[0]) + 2*magnitude(num[1])


def part1(numbers):
    res = numbers[0]
    for other in numbers[1:]:
        res = add(res, other)

    return magnitude(res)


def part2(numbers):
    mag = 0
    for i in range(0,len(numbers)):
        for j in range(0, len(numbers)):
            if i == j:
                continue

            res = add(numbers[i], numbers[j])
            resmag = magnitude(res)
            mag = max(mag, resmag)

    return mag


numbers = read('input.txt')
print("Part 1:")
mag = part1(numbers)
print(f"  Magnitude: {mag}")

print("Part 2:")
maxmag = part2(numbers)
print(f"  Max Magnitude: {maxmag}")