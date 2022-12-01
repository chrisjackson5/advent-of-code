def read(file):
    with open(file) as f:
        lines = (l[:-1].split(' | ') for l in f.readlines())
    return [([set(i) for i in inp.split()], [set(o) for o in out.split()]) for inp,out in lines]


def substitute(signal, mapping, patterns):
    corrected = {mapping[s] for s in signal}
    return next((v for pattern,v in patterns.items() if set(pattern)==corrected))


def resolve(signals, patterns: dict):
    mapping = {}
    patterns = [set(p) for p in patterns]
    segments = set().union(*patterns)
    pairings = [ (pattern, [signal for signal in signals if len(signal) == len(pattern)]) for pattern in patterns]

    while len(pairings) > 0:
        # Short signals are more likely to intersect, so use them first.
        pairings = sorted(pairings, key=lambda p: len(p[0]))
        pattern1, signals1 = pairings.pop(0)

        # We can't (easily) interesect using multiple signals, so skip them.
        if len(signals1) > 1:
            continue

        # Intersect pattern and signal with remaining items
        for j,(pattern2, signals2) in enumerate(pairings):
            # Check if patterns intersect
            if pattern1 == pattern2 or not pattern1.issubset(pattern2):
                continue

            # If patterns match, valid signals must contain signal1, so filter them.
            if len(signals2) > 1:
                signals2 = [s for s in signals2 if signals1[0].issubset(s)]
                pairings[j] = (pattern2, signals2)

            # Create a new pattern/signal combination from the deltas.
            new_pattern = pattern2 - pattern1
            new_signals = [s-signals1[0] for s in signals2]
            pairings.append((new_pattern, new_signals))

            # If the new pattern is a single character, add it to the mapping.
            if len(new_pattern) == 1:
                p = next(iter(new_pattern))
                s = next(iter(new_signals[0]))
                mapping[s] = p
                if len(mapping) == len(segments):
                    return mapping

    raise ValueError("Mapping not found")


def part1(readings):
    total = 0
    for _,out in readings:
        total += sum(1 for o in out if len(o) in [2,3,4,7])

    return total


def part2(readings):
    patterns = { 'abcefg': 0, 'cf': 1, 'acdeg': 2, 'acdfg': 3, 'bcdf': 4, 'abdfg': 5, 'abdefg': 6, 'acf': 7, 'abcdefg': 8, 'abcdfg': 9 }
    total = 0
    for inp, out in readings:
        mapping = resolve(inp, patterns)
        digits = [substitute(o, mapping, patterns) for o in out]
        result = int("".join(str(digit) for digit in digits))
        total += result

    return total


signals = read('input.txt')
print("Part1: ")
total1 = part1(signals)
print(f"  count: {total1}")
print("Part2: ")
total2 = part2(signals)
print(f"  total: {total2}")