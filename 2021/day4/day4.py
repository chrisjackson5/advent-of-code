
def read():
    with open('input.txt') as f:
        boards = []
        board = None
        numbers = None

        for line in f:
            line = line[:-1]
            if not numbers:
                numbers = [int(n) for n in line.split(",")]
            elif not line:
                board = []
                boards.append(board)
            else:
                board.append([int(n) for n in line.split()])

    return numbers,boards

def check(board):
    for r in range(0, 5):
        if not any(board[r]):
            return True
    for c in range(0, 5):
        if not any(r[c] for r in board):
            return True
    return False

def mark(number, board):
    for r in range(0, 5):
        for c in range(0, 5):
            if board[r][c] == number:
                board[r][c] = 0

def part1(numbers, boards):
    for i, number in enumerate(numbers):
        for j, board in enumerate(boards):
            mark(number, board)
            if i >= 4 and check(board):
                score = sum(map(sum, board))
                score *= number
                winner = j
                return winner,score

    raise ValueError("No winners")


def part2(numbers, boards):
    for i, number in enumerate(numbers):
        for j, board in enumerate(boards):
            if not board:
                continue
            mark(number, board)
            if i >= 4 and check(board):
                score = sum(map(sum, board))
                score *= number
                winner = j
                boards[j] = None

    return winner, score


numbers, boards = read()
print("Part 1:")
winner1, score1 = part1(numbers, boards)
print(f"  Winner: {winner1}")
print(f"  Score: {score1}")
print("Part 2:")
winner2, score2 = part2(numbers, boards)
print(f"  Winner: {winner2}")
print(f"  Score: {score2}")