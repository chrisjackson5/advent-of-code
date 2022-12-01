def read(file):
    with open(file) as f:
        algo, image = f.read().split('\n\n')
        algo = [1 if c == '#' else 0 for c in algo]
        image = [[1 if c == '#' else 0 for c in row] for row in image.splitlines()]

    return algo, image


def enhance(algo, image, background=0):
    height = len(image)
    width = len(image[0])

    enhanced = []
    for y in range(-1, height+1):
        row = []
        for x in range(-1, width+1):
            surround = [image[j][i] if (0<=i<width and 0<=j<height) else background 
                for j in range(y-1,y+2) 
                for i in range(x-1,x+2)]

            bin = "".join(str(c) for c in surround)
            index = int(bin, 2)
            lit = algo[index]
            row.append(lit)
        enhanced.append(row)

    background = algo[-1] if background == 1 else algo[0]

    return enhanced, background


def draw(image):
    drawing = "\n".join("".join('#' if c else ' ' for c in row) for row in image)
    print(drawing)


def part1(algo, image):
    image, bg = enhance(algo, image)
    image, bg = enhance(algo, image, bg)

    count = sum(sum(i for i in row) for row in image)
    return count


def part2(algo, image):
    bg = 0
    for i in range(0, 50):
        image, bg = enhance(algo, image, bg)

    count = sum(sum(i for i in row) for row in image)
    return count


algo, image = read('input.txt')
print('Part 1: ')
count1 = part1(algo, image)
print(f'  Count: {count1}')
print('Part 2: ')
count2 = part2(algo, image)
print(f'  Count: {count2}')
