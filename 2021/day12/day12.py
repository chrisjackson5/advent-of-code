from collections import defaultdict, Counter


def read(file):
    with open(file) as f:
        pairs = (tuple(p[:-1].split('-')) for p in f.readlines())
        paths = defaultdict(set)
        for (start,end) in pairs:
            paths[start].add(end)
            paths[end].add(start)

        return paths


def fork(route, paths, allowed_smalls=1):
    cur = route[-1]
    if cur == 'end':
        return [route]

    caves = paths[cur] - { 'start' }
    smalls = Counter(c for c in route if c.islower())

    routes = []
    for cave in caves:
        if smalls[cave] >= 1 and smalls.most_common(1)[0][1] >= allowed_smalls:
            continue

        forked = fork(route + [cave], paths, allowed_smalls)
        routes.extend(forked)

    return routes


def part1(paths):
    routes = fork(['start'], paths)
    return len(routes)


def part2(paths):
    routes = fork(['start'], paths, 2)
    return len(routes)


paths = read('input.txt')
print("Part 1:")
count1 = part1(paths)
print(f"  Count: {count1}")
print("Part 2:")
count2 = part2(paths)
print(f"  Count: {count2}")
