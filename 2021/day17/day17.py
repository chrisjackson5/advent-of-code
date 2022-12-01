import math 

def read(file):
    with open(file) as f:
        x,y = f.read()[13:].split(', ')
        xtarget = tuple(int(i) for i in x[2:].split('..'))
        ytarget = tuple(int(j) for j in y[2:].split('..'))
        return xtarget,ytarget


def sign(num):
    return -1 if num < 0 else (1 if num > 0 else 0)


def launch(velocity, target):
    vx,vy = velocity
    (xmin,xmax),(ymin,ymax) = target
    x,y = 0,0

    path = []
    while x <= xmax and (y >= ymin or vy > 0):
        path.append((x,y))
        if (xmin <= x <= xmax) and (ymin <= y <= ymax):
            return True, path
        x += vx
        y += vy
        vx -= sign(vx)
        vy -= 1

    return False, path


def hunt(target):
    (xmin,xmax),(ymin,ymax) = target

    # Assuming target < 0, max height is when it hits the target 1 step after passing 0.
    # Hence, vy is 1 less than the distance.
    vy = max(abs(ymin), abs(ymax)) - 1
    vx = math.ceil((math.sqrt(8*xmin + 1) - 1) / 2)

    hit,path = launch((vx,vy), target)

    return (vx,vy), path


def trajectories(target):
    (xmin,xmax),(ymin,ymax) = target

    vymax = max(abs(ymin), abs(ymax)) - 1
    vymin = -vymax - 1
    traj = set()

    for vy in range(vymax, vymin-1, -1):
        # Fire vertically at vy to find number of steps
        _, ipath = launch((0,vy), target)
        n = len(ipath) - 1

        i = -1
        # In some cases, probe more than one step will be inside the target.
        # Find all valid vx's for target y
        while ymin <= ipath[i][1] <= ymax:
            # Depending on number of steps, probe may hit the target when vx = 0, or whilst in flight.
            # Select the initial/min vx accordingly.
            if (n * (n+1) / 2) >= xmin:
                # vx = 0 at end
                vx = math.ceil((math.sqrt(8*xmin + 1) - 1) / 2)
            else:
                # vx > 0 at end
                vx = math.ceil(xmin/n + (n-1)/2)

            hit, path = launch((vx, vy), target)
            while hit:
                traj.add((vx,vy))
                vx += 1
                hit, path = launch((vx, vy), target)

            n -= 1
            i -= 1

    return traj


def part1(target):
    v, path = hunt(target)
    ymax = max(y for x,y in path)
    return ymax


def part2(target):
    traj = trajectories(target)
    return len(traj)


target = read('input.txt')
print("Part 1:")
ymax = part1(target)
print(f"  Max Y: {ymax}")
print("Part 2:")
tcount = part2(target)
print(f"  Trajectories: {tcount}")
