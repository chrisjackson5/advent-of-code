from collections import defaultdict

def read(file):
    with open(file) as f:
        instructions = (l.split(' ') for l in f.read().splitlines())
        instructions = [(cmd,a,coerce(b[0])) if b else (cmd,a) for cmd,a,*b in instructions]
    return instructions


def coerce(a):
    try:
        a = int(a)
    except:
        pass
    return a


class ALU():
    cmds = {
        'inp': lambda a,b: b,
        'add': lambda a,b: a + b,
        'mul': lambda a,b: a * b,
        'div': lambda a,b: a // b,
        'mod': lambda a,b: a % b,
        'eql': lambda a,b: 1 if a==b else 0
    }

    def __init__(self):
        self.state = { 'w': 0, 'x': 0, 'y': 0, 'z': 0 }

    def __getitem__(self, a):
        return self.state.get(a, a)

    def __setitem__(self, a, b):
        self.state[a] = b

    def exec(self, instruction, inp):
        cmd,a,b = instruction if len(instruction)==3 else instruction + (inp,)
        self[a] = self.cmds[cmd](self[a], self[b])

    def run(self, instructions, inp):
        for instruction in instructions:
            self.exec(instruction, inp)

        return self.state


def split(instructions):
    start = 0
    end = 1
    sections = []
    for cmd,*_ in instructions[1:]:
        if cmd == 'inp':
            sections.append(instructions[start:end])
            start = end
        end += 1

    sections.append(instructions[start:])
    return sections


def reduce(instructions):
    sections = split(instructions)
    reduced = []
    for instructions in zip(*sections):
        cmd, a, *b = (item for item in zip(*instructions))
        
        cmd = cmd[0] if len(set(cmd)) == 1 else cmd
        a = a[0] if len(set(a)) == 1 else a
        b = None if not b else (b[0][0] if len(set(b[0])) < 2 else b[0])

        reduced.append((cmd,a,b))

    return reduced


def algo(w,z,a,b,c):
    """Reduction of the model checking algorithm."""
    x = (z % 26) + b
    y1 = 26 if x != w else 1
    y2 = w + c if x != w else 0

    z //= a
    z *= y1
    z += y2

    return z


def solve(ai,bi,ci):
    cache = []
    zs = {0}
    for a,b,c in zip(ai,bi,ci):
        solutions = defaultdict(dict)
        cache.append(solutions)

        nextz = set()
        
        if a == 26:
            for z in zs:
                w = z % 26 + b
                if not 1 <= w <= 9:
                    continue

                out = algo(w,z,a,b,c)
                solutions[z][w] = out
                nextz.add(out)

        else:
            for w in range(1,10):
                for z in zs:
                    out = algo(w,z,a,b,c)
                    solutions[z][w] = out
                    nextz.add(out)

        zs = nextz

    return cache


def find_solution(cache, z=0, max=True):
    nodes = cache[0][z]
    
    ws = range(1,10)
    if max:
        ws = range(9,0,-1)

    for w in ws:
        subz = nodes.get(w, None)
        if subz is None:
            continue

        digits = find_solution(cache[1:], subz, max) if len(cache) > 1 else ''
        if digits is not None:
            return str(w) + digits

    return None


def parts(instructions):
    reduced = reduce(instructions)
    ai = reduced[4][2]
    bi = reduced[5][2]
    ci = reduced[15][2]

    cache = solve(ai,bi,ci)

    max_solution = int(find_solution(cache))
    min_solution = int(find_solution(cache, max=False))
    return max_solution, min_solution


instructions = read('input.txt')
max_model, min_model = parts(instructions)
print("Part 1:")
print(f"  Model: {max_model}")
print("Part 2:")
print(f"  Model: {min_model}")