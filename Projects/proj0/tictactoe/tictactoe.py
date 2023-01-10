"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O: str = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return "X"

    count_X = 0
    count_O = 0

    for line in board:
        for position in line:
            if position == X:
                count_X += 1
            elif position == O:
                count_O += 1

    return X if count_X <= count_O else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    _actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                _actions.add((i, j))

    return _actions


def checkAction(board, action):
    if len(action) != 2:
        raise Exception("result function: incorrect action")
    if action[0] > 2 or action[0] < 0 or action[1] > 2 or action[1] < 0:
        raise Exception('Value invalid')
    if board[action[0]][action[1]] != EMPTY:
        raise Exception('Target position of the board is not empty')
    return


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    checkAction(board, action)
    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = player(board)
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for y in range(3):
        # Check horizontal lines
        if (board[y][0] == board[y][1] == board[y][2]) and (board[y][0] != EMPTY):
            return board[y][0]
        # check vertical lines
        if (board[0][y] == board[1][y] == board[2][y]) and (board[0][y] != EMPTY):
            return board[0][y]

        # Check diagonals
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]) \
            and board[1][1] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]) or winner(board) == X or winner(
            board) == O:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    _actions = actions(board)
    _player = player(board)
    if _player == X:
        score = -math.inf
        action_to_take = None

        for _action in _actions:
            min_val = minValue(result(board, _action))
            if min_val > score:
                score = min_val
                action_to_take = _action

        return action_to_take

    elif _player == O:
        score = math.inf
        action_to_take = None

        for _action in _actions:
            max_val = maxValue(result(board, _action))
            if max_val < score:
                score = max_val
                action_to_take = _action

        return action_to_take


def minValue(board):
    if terminal(board):
        return utility(board)

    max_value = math.inf
    for action in actions(board):
        max_value = min(max_value, maxValue(result(board, action)))

    return max_value


def maxValue(board):
    if terminal(board):
        return utility(board)

    min_value = - math.inf
    for action in actions(board):
        min_value = max(min_value, minValue(result(board, action)))

    return min_value
