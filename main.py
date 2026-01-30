from gui import TicTacToeGUI
from sound_generator import SoundGenerator

if __name__ == "__main__":
    SoundGenerator.generate_sound()
    game = TicTacToeGUI()
    game.run()
