from collections import Counter

def read(file):
    with open(file) as f:
        lines = f.read().splitlines()

    polymer = lines[0]
    insertions = { pair: (pair[0]+insert, insert+pair[1]) for pair,insert in (l.split(' -> ') for l in lines[2:]) }
    return polymer, insertions


def insert(polymer: Counter, insertions: dict):
    additions = Counter()
    for k,count in polymer.items():
        ins = insertions.get(k, None)
        if ins:
            polymer[k] = 0
            additions[ins[0]] += count
            additions[ins[1]] += count
    polymer += additions
  

def elements(polymer: str, insertions: dict, steps: int):
    els = Counter(polymer[-1])
    polymer = Counter(polymer[i:i+2] for i in range(0, len(polymer)-1))
    for _ in range(0, steps):
        insert(polymer, insertions)

    for key,count in polymer.items():
        els[key[0]] += count

    return els


def part1(polymer: str, insertions: dict):
    els = elements(polymer, insertions, 10)
    counts = els.most_common()
    return counts[0][1] - counts[-1][1]


def part2(polymer: str, insertions: dict):
    els = elements(polymer, insertions, 40)
    counts = els.most_common()
    return counts[0][1] - counts[-1][1]


polymer, insertions = read('input.txt')
print("Part 1:")
diff = part1(polymer, insertions)
print(f"  Diff: {diff}")
print("Part 2:")
diff = part2(polymer, insertions)
print(f"  Diff: {diff}")

