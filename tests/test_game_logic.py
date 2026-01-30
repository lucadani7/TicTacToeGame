# tests/test_game_logic.py

import unittest

from game_logic import GameLogic


class TestGameLogicInit(unittest.TestCase):

    def test_initial_board(self):
        """Test if the initial board is a list of 9 spaces."""
        game_logic = GameLogic()
        expected_board = [' '] * 9
        self.assertEqual(expected_board, game_logic.board)

    def test_initial_human_symbol(self):
        """Test if the default human symbol is 'X'."""
        game_logic = GameLogic()
        expected_human_symbol = 'X'
        self.assertEqual(expected_human_symbol, game_logic.human)

    def test_initial_ai_symbol(self):
        """Test if the default AI symbol is '0'."""
        game_logic = GameLogic()
        expected_ai_symbol = '0'
        self.assertEqual(expected_ai_symbol, game_logic.ai)


if __name__ == "__main__":
    unittest.main()
