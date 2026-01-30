import math
import random


class GameLogic:
    """
    A class for managing game logic in a Tic-Tac-Toe game.

    This class provides functionality to manage the game board, determine valid moves,
    check for winning or tie conditions, and implement AI behavior through the Minimax algorithm.
    It uses different levels of difficulty to determine the AI's decision-making process.

    :ivar board: The current state of the game board is represented as a list of 9 spaces,
                 where each space is either empty (' ') or occupied by the player's
                 symbol ('X' for human and '0' for AI).
    :type board: List[str]
    :ivar human: The symbol representing the human player on the board, default is 'X'.
    :type human: Str
    :ivar ai: The symbol representing the AI player on the board, default is '0'.
    :type ai: Str
    """
    def __init__(self):
        self.board = [' '] * 9
        self.human = 'X'
        self.ai = '0'

    @staticmethod
    def is_winner(board, player):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for w in wins:
            if board[w[0]] == board[w[1]] == board[w[2]] == player:
                return True
        return False

    @staticmethod
    def is_full(board):
        return ' ' not in board

    @staticmethod
    def available_moves(board):
        return [i for i, x in enumerate(board) if x == ' ']

    def minimax(self, board, depth, is_maximizing):
        if self.is_winner(board, self.ai):
            return 10 - depth
        if self.is_winner(board, self.human):
            return -10 + depth
        if self.is_full(board):
            return 0
        if is_maximizing:
            best_score = -math.inf
            for move in self.available_moves(board):
                board[move] = self.ai
                score = self.minimax(board, depth + 1, False)
                board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in self.available_moves(board):
                board[move] = self.human
                score = self.minimax(board, depth + 1, True)
                board[move] = ' '
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        if self.board[4] == ' ':
            return 4
        for move in self.available_moves(self.board):
            self.board[move] = self.ai
            score = self.minimax(self.board, 0, False)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def get_ai_move(self, difficulty):
        available = self.available_moves(self.board)
        if not available:
            return None
        match difficulty:
            case 1:
                return random.choice(available)
            case 2:
                return random.choice(available) if random.random() < 0.5 else self.get_best_move()
            case _:
                return self.get_best_move()