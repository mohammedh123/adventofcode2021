from collections import defaultdict

BOARD_SIZE = 5


def sum_unmarked_numbers_on_board(board_markers, board):
    unmarked_sum = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if not board_markers[r + 1][c + 1]:
                unmarked_sum += board[r][c]
    return unmarked_sum


draws = []
boards = {}
index = defaultdict(list)  # A mapping of number to a list of (board #, row, col) tuples
with open('input') as f:
    draws = [int(c) for c in f.readline().split(',')]
    current_board = None

    while (line := f.readline()):
        line = line.strip()

        if not line:
            # Make a new board
            current_board = []
        else:
            # Otherwise add to the current board, and consider it done once
            # it hits the board size
            # While building the board, also build an index for fast marking
            new_row = [int(x) for x in line.split()]
            board_num = len(boards)

            for c, n in enumerate(new_row):
                r = len(current_board)
                index[n].append((board_num, r, c))

            current_board.append(new_row)
            if len(current_board) == BOARD_SIZE:
                boards[board_num] = {
                    'board': current_board,
                    'markers': None,
                    'has_won': False,
                }

# Create N matrices filled with False where N = len(boards)
# Note: these matrices are BOARD_SIZE + 1 rows and columns for sentinel values
# They'll be 0s for the first row and column, to keep track of the number of
# marked values for that given row/column, and False otherwise, so something like:
# 0 0 0 0 0 0
# 0 F F F F F
# 0 F F F F F
# 0 F F F F F
# 0 F F F F F
# 0 F F F F F
for board_num in boards:
    markers = [
        [False for c in range(BOARD_SIZE + 1)]
        for r
        in range(BOARD_SIZE + 1)
    ]

    for r in range(len(markers)):
        for c in range(len(markers[0])):
            if r == 0 or c == 0:
                markers[r][c] = 0

    boards[board_num]['markers'] = markers

first_winning_score = None
last_winning_score = None
for draw in draws:
    # Mark all the cells with this number (and update sentinels)
    for board_num, r, c in index[draw]:
        markers = boards[board_num]['markers']
        if markers[r + 1][c + 1]:  # Already marked; ignore
            continue

        # Remember to offset r and c by +1 due to sentinel values
        markers[r + 1][c + 1] = True

        # ...and update sentinel values
        markers[0][c + 1] += 1
        markers[r + 1][0] += 1

        # ...and process this winner if any rows/columns are complete now
        if markers[0][c + 1] == BOARD_SIZE or markers[r + 1][0] == BOARD_SIZE:

            # ...but only if this board isn't already a winner
            if boards[board_num]['has_won']:
                continue

            boards[board_num]['has_won'] = True

            unmarked_sum = sum_unmarked_numbers_on_board(markers, boards[board_num]['board'])
            score = unmarked_sum * draw

            if not first_winning_score:
                first_winning_score = score

            last_winning_score = score

print(f'Part 1 solution: {first_winning_score}')
print(f'Part 2 solution: {last_winning_score}')