from heapq import heappush, heappop

def read(file):
    with open(file) as f:
        risks = [[int(risk) for risk in row] for row in f.read().splitlines()]
    return risks


def tile(risks, x, y):
    xmax = len(risks[0])
    ymax = len(risks)
    tiled = [
        [ 1 + ((r-1) % 9) 
            for r in 
                (risks[j % ymax][i % xmax] + i//xmax + j//ymax for i in range(0,x*xmax))
            ] 
        for j in range(0,y*ymax)]

    return tiled


def path(risks, start, end):
    xmax = len(risks[0]) - 1
    ymax = len(risks) - 1
    ex,ey = end

    cur = start
    # Path nodes, pointing at their previous node.
    paths = { start: None }
    # Total risk calculated for encountered nodes.
    trisks = { start: 0}
    # Priority queue to track the leaf nodes
    leafs = []
    while cur != end:
        cx,cy = cur
        moves = ((cx+x, cy+y) for x,y in ((1,0), (0,1), (-1,0), (0,-1)))
        moves = ((x,y) for x,y in moves if 0<=x<=xmax and 0<=y<=ymax and (x,y) != paths[cur])
        for move in moves:
            x,y = move
            moverisk = trisks[cur] + risks[y][x]
            if 0 <= trisks.get(move,-1) <= moverisk:
                continue
            paths[move] = cur
            trisks[move] = moverisk

            # Add the min remaining risk to help prioritise later stage paths
            prisk = moverisk + (ex-x + ey-y - 1)
            heappush(leafs, (prisk, move))

        # Select the next node as the end point with lowest risk
        prisk, cur = heappop(leafs)

    return paths, trisks


def part1(risks):
    start = (0,0)
    end = (len(risks[0])-1, len(risks)-1)
    paths, trisks = path(risks, start, end)
    return trisks[end]


def part2(risks):
    risks = tile(risks, 5, 5)
    return part1(risks)


risks = read('input.txt')
print("Part 1:")
risk1 = part1(risks)
print(f"  Risk: {risk1}")

print("Part 2:")
risk2 = part2(risks)
print(f"  Risk: {risk2}")