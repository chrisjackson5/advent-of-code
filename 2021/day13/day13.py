def read(file):
    with open(file) as f:
        dots, folds = f.read().split('\n\n')
    
    dots = (d.split(',') for d in dots.splitlines())
    dots = {(int(x),int(y)) for x,y in dots}

    folds = (f[11:].split('=') for f in folds.splitlines())
    folds = [(0 if axis=='x' else 1, int(pos)) for axis,pos in folds]

    return (dots, folds)


def fold(dots, fold):
    axis, pos = fold
    folded = {d for d in dots if d[axis] > pos}
    dots -= folded
    dots |= {(pos+pos-x, y) if axis==0 else (x, pos+pos-y) for x,y in folded}


def draw(dots):
    xmax, ymax = tuple(max(axis) for axis in zip(*dots))
    canvas = [[' ' for i in range(0,xmax+1)] for j in range(0, ymax+1)]
    for x,y in dots:
        canvas[y][x] = '\u2588'

    return "\n".join("".join(c for c in row) for row in canvas)


def part1(dots, folds):
    fold(dots, folds[0])
    return len(dots)


def part2(dots, folds):
    for f in folds:
        fold(dots, f)
    return draw(dots)


dots1, folds = read('input.txt')
dots2 = {d for d in dots1}
print("Part 1:")
count1 = part1(dots1, folds)
print(f"  Count: {count1}")
print("Part 2:")
canvas = part2(dots2, folds)
print(canvas)