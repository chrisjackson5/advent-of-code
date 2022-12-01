import functools

def read(file):
    with open(file) as f:
        p1,p2 = f.read().splitlines()
    p1 = int(p1[28])
    p2 = int(p2[28])

    return p1,p2


def roll(n):
    return 3 + ((n-1) % 100) + (n % 100) + ((n+1) % 100)


@functools.lru_cache(maxsize=None)
def play(p1, p2, winscore = 21):
    probs = {
        3: 1,
        4: 3,
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1
    }

    p1pos, p1score = p1
    p1wins = 0
    p2wins = 0

    for roll, count in probs.items():
        new_pos = 1 + ((p1pos + roll - 1) % 10)
        new_score = p1score + new_pos

        if new_score >= winscore:
            p1wins += count
        else:
            p2count, p1count = play(p2, (new_pos,new_score), winscore)
            p1wins += p1count * count
            p2wins += p2count * count

    return p1wins, p2wins


def part1(p1,p2, winscore):
    p1score = 0
    p2score = 0
    n = 1
    while p1score < winscore and p2score < winscore:
        p1 += roll(n)
        p1 = 1 + ((p1-1) % 10)
        p1score += p1

        n += 3

        if p1score >= winscore:
            continue

        p2 += roll(n)
        p2 = 1 + ((p2-1) % 10)
        p2score += p2

        n += 3

    n -= 1

    res = n * min(p1score, p2score)
    return res


def part2(p1, p2, winscore):
    p1wins, p2wins = play((p1,0), (p2,0), winscore)

    return max(p1wins, p2wins)


p1,p2 = read('input.txt')
print('Part 1:')
res = part1(p1, p2, 1000)
print(f'  Result: {res}')

print('Part 2:')
res = part2(p1, p2, 21)
print(f'  Result: {res}')

