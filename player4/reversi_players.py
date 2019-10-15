# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy

# John Hunter

class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size()+1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, ( x, y) ):
                    no_valid_move = False
                    return [x, y]
                else:
                    print('Not a valid move.')
            else:
                print('Bad input. Type valid x digit, then the y digit.')


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))


class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        all_valid_moves = board.calc_valid_moves(self.symbol)
        best_move = (board, 0, None)
        for x in all_valid_moves:

            # make a copy of the board
            new_board = copy.deepcopy(board)

            # make a move on the board
            new_board.make_move(self.symbol, x)

            # get the score of the new board
            new_score = new_board.calc_scores()[self.symbol]

            # if the score is better, save it
            if new_score > best_move[1]:
                best_move = (new_board, new_score, x)

        return best_move[2]


# With the current implementation, minimax must be 'X'
class MinimaxComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        move = minimax(board, 5, True)[0]
        return move


def minimax(board, depth, my_turn):

    if my_turn:
        best = [(0, 0), -999]
        symbol = 'X'
    else:  # opponents turn
        best = [(0, 0), 999]
        symbol = 'O'

    # break case
    if depth == 0 or not board.game_continues():
        end_scores = board.calc_scores()
        if end_scores['X'] > end_scores['O']:
            return [None, 1]
        if end_scores['X'] < end_scores['O']:
            return [None, -1]
        else:
            # tie game
            return [None, 0]

    for move in board.calc_valid_moves(symbol):
        # set up possible board
        new_board = copy.deepcopy(board)
        new_board.make_move(symbol, move)
        score = minimax(new_board, depth-1, not my_turn)
        score[0] = move

        if score[1] == 999 or score[1] == -999:
             score[1] = -1

        # compare the results of the possible board
        if my_turn:
            if score[1] > best[1]:
                best = score
        else:
            if score[1] < best[1]:
                best = score

    return best
