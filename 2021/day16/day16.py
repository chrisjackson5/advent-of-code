value_funcs = [
    lambda p: sum(value(s) for s in p),
    lambda p: prod(value(s) for s in p),
    lambda p: min(value(s) for s in p),
    lambda p: max(value(s) for s in p),
    lambda p: p,
    lambda p: 1 if value(p[0]) > value(p[1]) else 0,
    lambda p: 1 if value(p[0]) < value(p[1]) else 0,
    lambda p: 1 if value(p[0]) == value(p[1]) else 0,
]


def read(file):
    with open(file) as f:
        hex = f.read()
    return tobin(hex)


def prod(nums):
    p = 1
    for n in nums:
        p *= n
    return p


def tobin(hex):
    number = int(hex, 16)
    width = len(hex) * 4
    spec = f"0>{width}b"
    return format(number, spec)


def packetize(bin, i=0):
    version = int(bin[i:i+3], 2)
    ptype = int(bin[i+3:i+6], 2)

    i += 6
    if ptype == 4:
        bnum = bin[i+1:i+5]
        while bin[i] == '1':
            i += 5
            bnum += bin[i+1:i+5]
        i += 5
        packet = int(bnum, 2)

    elif bin[i] == '0':
        plen = int(bin[i+1:i+16], 2)
        i += 16
        pend = i + plen
        packet = []
        while i < pend:
            v,t,p,i = packetize(bin, i)
            packet.append((v,t,p))

    else:
        plen = int(bin[i+1:i+12], 2)
        i += 12
        packet = []
        for _ in range(0, plen):
            v,t,p,i = packetize(bin, i)
            packet.append((v,t,p))

    return version,ptype,packet,i


def sumversions(contents):
    version,ptype,packet = contents
    vsum = version
    if ptype != 4:
        vsum += sum(sumversions(sub) for sub in packet)

    return vsum


def value(contents):
    version,ptype,packet = contents
    return value_funcs[ptype](packet)


def part1(bin):
    version,ptype,res,i = packetize(bin)
    return sumversions((version,ptype,res))


def part2(bin):
    version,ptype,packet,i = packetize(bin)
    return value((version,ptype,packet))


bin = read('input.txt')
print("Part 1:")
vsum = part1(bin)
print(f"  Version Sum: {vsum}")
print("Part 2:")
v = part2(bin)
print(f"  Value: {v}")