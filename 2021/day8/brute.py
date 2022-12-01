import re

def read(file):
    with open(file) as f:
        lines = (l[:-1].split(' | ') for l in f.readlines())
        return [(inp.split(), out.split()) for inp,out in lines]

def part1(readings):
    count = 0
    for inp,out in readings:
        for o in out:
            l = len(o)
            if l==2 or l==3 or l==4 or l==7:
                count += 1

    return count

segments = "abcdefg"
char_map = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

def substitute(pattern: str, mapping: str):
    segs = [segments[mapping.index(p)] for p in pattern]
    segs = sorted(segs)
    sub = "".join(segs)
    try:
        return char_map.index(sub)
    except ValueError:
        return -1

def check(patterns, mapping):
    for pattern in patterns:
        num = substitute(pattern, mapping)
        if num < 0:
            return False

    return True

def permutations(mapping: str):
    a = [c for c in mapping]
    n = len(a)
    def sub(i):
        if i == n - 1:
            yield "".join(a)
        else:
            for k in range(i, n):
                a[i], a[k] = a[k], a[i]
                yield from sub(i + 1)
                a[i], a[k] = a[k], a[i]
    yield from sub(0)

def resolve(patterns):
    mapping = segments
    
    for mapping in permutations(segments):
        if check(patterns, mapping):
            return mapping

    return mapping


# def cross(first, second):
#     res = ""
#     for c in first:
#         if c in second:
#             res += c

#     return res

# def resolve(patterns):
#     print(patterns)
#     segments = "abcdefg"
#     clues = []
#     for c in char_map:
#         pc = [p for p in patterns if len(p) == len(c)]
#         clues.append((c, pc))

#     #clues = [ (c, [p for p in patterns if len(p)==len(c)]) for c in char_map.sort(key=len) ]
#     mapping = {}

#     i = 0
#     while i < len(clues):
#         ci, pi = clues[i]
#         for j in range(0, len(clues)):
#             cj, pj = clues[j]
#             if i == j or len(cj)==1:
#                 continue
#             if all(ck in ck for ck in ci):
#                 if len(pi) == 1 and len(pj) > 1:
#                     pj = [l for l in pj if all(k in l for k in pi[0])]
#                     clues[j] = (cj, pj)

#                 newc = re.sub(f'[{ci}]', '', cj)
#                 newp = [re.sub(f'[{pi}]', '', pk) for pk in pj]
#                 clues.append((newc, newp))
#                 if len(newc) == 1:
#                     mapping[newp[0]] = newc

#         if len(mapping) == len(segments):
#             break

#     return mapping

    


def part2(readings):
    total = 0
    for inp, out in readings:
        mapping = resolve(inp)
        chars = [substitute(o, mapping) for o in out]
        val = "".join(str(c) for c in chars)
        res = int(val)
        total += res
        print("Mapping: " + mapping)
        print("Out: " + str(res))

    return total






readings = read('input.txt')
count = part1(readings)
print("Part1: ")
print("  count: " + str(count))

total = part2(readings)
print("Part2: ")
print("  total: " + str(total))