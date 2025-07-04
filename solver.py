from collections import deque
import copy

# Constants
WALL = '#'
GOAL = '.'
BOX = '$'
PLAYER = '@'
BOX_ON_GOAL = '*'
PLAYER_ON_GOAL = '+'
EMPTY = ' '

# Directions
DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

# Parse board and extract goal positions
def parse_board(raw_board):
    board = [list(row) for row in raw_board]
    goals = set()
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val in (GOAL, BOX_ON_GOAL, PLAYER_ON_GOAL):
                goals.add((i, j))
    return board, goals

# Locate player on the board
def find_player(board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell in ('@', '+'):
                return (i, j)
    return None

# Check if all goals have boxes
def is_completed(board, goals):
    for i, j in goals:
        if board[i][j] not in ('*', '+'):
            return False
    return True

# Attempt to move the player in the specified direction
def move(board, pos, direction, goals):
    di, dj = DIRECTIONS[direction]
    i, j = pos
    ni, nj = i + di, j + dj

    if not (0 <= ni < len(board) and 0 <= nj < len(board[0])):
        return None, None

    nni, nnj = ni + di, nj + dj
    if board[ni][nj] in (BOX, BOX_ON_GOAL):
        if not (0 <= nni < len(board) and 0 <= nnj < len(board[0])):
            return None, None

    cell = board[i][j]
    next_cell = board[ni][nj]
    beyond_cell = board[nni][nnj] if (0 <= nni < len(board) and 0 <= nnj < len(board[0])) else WALL

    new_board = copy.deepcopy(board)

    def update_cell(i, j, value):
        if (i, j) in goals:
            new_board[i][j] = {'@': '+', ' ': '.', '$': '*'}[value]
        else:
            new_board[i][j] = value

    if next_cell in (EMPTY, GOAL):
        update_cell(i, j, ' ')
        update_cell(ni, nj, '@')
        return new_board, (ni, nj)

    elif next_cell in (BOX, BOX_ON_GOAL):
        if beyond_cell in (EMPTY, GOAL):
            update_cell(i, j, ' ')
            update_cell(ni, nj, '@')
            update_cell(nni, nnj, '$')
            return new_board, (ni, nj)

    return None, None

# Convert board to a hashable key
def board_key(board):
    return tuple(tuple(row) for row in board)

# Solver using BFS
def sokoban_solver(raw_board):
    board, goals = parse_board(raw_board)
    start_pos = find_player(board)
    visited = set()
    queue = deque()
    queue.append((board, start_pos, ""))

    while queue:
        curr_board, curr_pos, path = queue.popleft()
        key = (board_key(curr_board), curr_pos)
        if key in visited:
            continue
        visited.add(key)

        if is_completed(curr_board, goals):
            return path

        for direction in 'UDLR':
            new_board, new_pos = move(curr_board, curr_pos, direction, goals)
            if new_board:
                queue.append((new_board, new_pos, path + direction))

    return "No solution found."
