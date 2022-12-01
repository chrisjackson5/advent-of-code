def read(file):
    with open(file) as f:
        return [l[:-1] for l in f.readlines()]


def error(line):
    pairs = { '(':')','[':']','{':'}','<':'>' }
    stack = []
    for i,c in enumerate(line):
        if c in pairs:
            stack.append(c)
        else:
            expected = pairs[stack.pop()]
            if c != expected:
                return c,i

    closing = (pairs[c] for c in reversed(stack))
    return "".join(closing), -1


def part1(lines):
    scoremap = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
    errs = (error(l) for l in lines)
    errs = (e for e,i in errs if i >= 0)
    points = (scoremap.get(e, 0) for e in errs)
    return sum(points)


def part2(lines):
    scoremap = {')': 1, ']': 2, '}': 3, '>': 4 }
    errs = (error(l) for l in lines)
    errs = (e for e,i in errs if i < 0)
    scores = []
    for closing in errs:
        score = 0
        for c in closing:
            score = score*5 + scoremap[c]
        scores.append(score)
    scores = sorted(scores)
    return scores[len(scores)//2]


lines = read('input.txt')
print("Part1:")
score1 = part1(lines)
print(f"  Score: {score1}")
print("Part2:")
score2 = part2(lines)
print(f"  Score: {score2}")
