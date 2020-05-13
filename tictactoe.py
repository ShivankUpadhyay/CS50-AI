"""
Tic Tac Toe Player
"""
import random

X = "X"
O = "O"
EMPTY = "_"


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
    X_count = 0
    O_count = 0
    for i in board:
        for j in i:
            if j is X:
                X_count += 1
            elif j is O:
                O_count += 1

    if O_count < X_count:
        return O

    return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                possible_actions.append((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board[action[0]][action[1]] = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_sequence = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    for x, y, z in win_sequence:
        if board[int(x / 3)][x % 3] == board[int(y / 3)][y % 3] == board[int(z / 3)][z % 3]:
            if board[int(x / 3)][x % 3] == X:
                return X
            if board[int(x / 3)][x % 3] == O:
                return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return len(actions(board)) == 0 or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)

    if result == X:
        return 1
    elif result == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    possible_actions = actions(board)

    if len(possible_actions) == 9:
        return random.choice(possible_actions)

    current_player = player(board)

    opt_action = help(board, current_player)

    return opt_action[1]


def help(board, current_player):
    """
    Implements the Minimax for both X and O
    """
    if terminal(board):
        return utility(board), None

    else:

        all_actions = actions(board)
        val = 1.0
        action = []

        if current_player == X:
            val = -1.0

            for i in all_actions:
                temp = result(board, i)
                ans = help(temp, O)
                temp_val = val
                val = max(val, ans[0])
                if val > temp_val:
                    action = i
                board[i[0]][i[1]] = EMPTY
                if val == 1:
                    break

        else:

            for i in all_actions:
                temp = result(board, i)
                ans = help(temp, X)
                temp_val = val
                val = min(val, ans[0])
                if val < temp_val:
                    action = i
                board[i[0]][i[1]] = EMPTY
                if val == -1:
                    break

        return val, action
