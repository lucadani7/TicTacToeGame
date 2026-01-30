import os
import sys

import pygame

from constants import DIMS, COLORS, screen, small_font, font
from game_logic import GameLogic


class TicTacToeGUI:
    """
    Manages the graphical user interface (GUI) for a Tic-Tac-Toe game.

    This class provides the main game loop, handles user inputs, and renders the game
    board, figures, and user interface elements on the screen. It also supports
    features like sound effects, adjustable difficulty levels, and game reset functionality.

    :ivar sounds: A dictionary containing loaded sound effects for events like moves,
        wins, and game over. The keys are the event names, and the values are
        pygame.mixer.Sound objects.
    :type sounds: Dict

    :ivar logic: An instance of the game logic class that manages the game board
        and AI moves.
    :type logic: GameLogic

    :ivar running: A flag indicating whether the main game loop is running.
    :type running: Bool

    :ivar game_over: A flag indicating whether the current game has ended.
    :type game_over: Bool

    :ivar difficulty: The difficulty level for AI moves. Possible values are:
        1 (easy), 2 (medium), and 3 (hard).
    :type difficulty: Int

    :ivar scores: A dictionary tracking the scores for the game. Includes keys 'X' for
        player wins, '0' for AI wins, and 'Draws' for tie games.
    :type scores: Dict

    :ivar winner_text: The text message is displayed when the game ends, indicating
        the result (e.g., "YOU WON!", "AI WON!", or "DRAW!").
    :type winner_text: Str

    :ivar btn_y: The vertical position of the buttons below the game board.
    :type btn_y: Int

    :ivar buttons: A list of dictionaries, each representing a button on the user
        interface. Each dictionary contains:
            - "rect": A pygame.Rect defining the button's position and size.
            - "text": The text label displayed on the button.
            - "Val": The value associated with the button (e.g., difficulty level
              or reset action).
    :type buttons: List
    """
    def __init__(self):
        self.sounds = None
        self.logic = GameLogic()
        self.running = True
        self.game_over = False
        self.difficulty = 3
        self.scores = {'X': 0, '0': 0, 'Draws': 0}
        self.winner_text = ""
        self.btn_y = DIMS.BOARD_SIZE + 20
        self.buttons = [
            {"rect": pygame.Rect(20, self.btn_y, 100, 50), "text": "EASY", "val": 1},
            {"rect": pygame.Rect(130, self.btn_y, 100, 50), "text": "MEDIUM", "val": 2},
            {"rect": pygame.Rect(240, self.btn_y, 100, 50), "text": "HARD", "val": 3},
            {"rect": pygame.Rect(450, self.btn_y, 130, 50), "text": "RESET", "val": 0}
        ]
        self.load_sounds()

    @staticmethod
    def get_resource_path(relative_path):
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def load_sounds(self):
        self.sounds = {}
        sound_folder = "sounds"
        files = {"move": "move.wav", "win": "win.wav", "over": "over.wav"}
        print(f"--- Checking audio files in {sound_folder} folder ---")
        for name, filename in files.items():
            relative_path = os.path.join(sound_folder, filename)
            full_path = TicTacToeGUI.get_resource_path(relative_path)
            if not os.path.exists(full_path):
                print(f"[WARNING] '{full_path}' is missing. No sound will not be played.")
            else:
                try:
                    sound = pygame.mixer.Sound(full_path)
                    sound.set_volume(0.3)
                    self.sounds[name] = sound
                    print(f"[OK] Sound loaded: {full_path}")
                except Exception as e:
                    print(f"[ERROR] Failed to load sound '{full_path}': {e}")

    def play_sound(self, name):
        if name in self.sounds:
            try:
                self.sounds[name].play()
            except:
                pass

    @staticmethod
    def draw_grid_lines():
        pygame.draw.line(screen, COLORS.LINE, (0, DIMS.CELL_SIZE), (DIMS.WIDTH, DIMS.CELL_SIZE), DIMS.LINE_WIDTH)
        pygame.draw.line(screen, COLORS.LINE, (0, 2 * DIMS.CELL_SIZE), (DIMS.WIDTH, 2 * DIMS.CELL_SIZE),
                         DIMS.LINE_WIDTH)
        pygame.draw.line(screen, COLORS.LINE, (DIMS.CELL_SIZE, 0), (DIMS.CELL_SIZE, DIMS.BOARD_SIZE), DIMS.LINE_WIDTH)
        pygame.draw.line(screen, COLORS.LINE, (2 * DIMS.CELL_SIZE, 0), (2 * DIMS.CELL_SIZE, DIMS.BOARD_SIZE),
                         DIMS.LINE_WIDTH)

    def draw_figures(self):
        for index, cell in enumerate(self.logic.board):
            if cell == ' ':
                continue
            row, col = index // 3, index % 3
            cx = col * DIMS.CELL_SIZE + DIMS.CELL_SIZE // 2
            cy = row * DIMS.CELL_SIZE + DIMS.CELL_SIZE // 2
            if cell == '0':
                pygame.draw.circle(screen, COLORS.CIRCLE, (cx, cy), DIMS.CIRCLE_RADIUS, DIMS.CIRCLE_WIDTH)
            elif cell == 'X':
                start_x = col * DIMS.CELL_SIZE + DIMS.SPACE
                start_y = row * DIMS.CELL_SIZE + DIMS.SPACE
                end_x = col * DIMS.CELL_SIZE + DIMS.CELL_SIZE - DIMS.SPACE
                end_y = row * DIMS.CELL_SIZE + DIMS.CELL_SIZE - DIMS.SPACE
                pygame.draw.line(screen, COLORS.CROSS, (start_x, start_y), (end_x, end_y), DIMS.CROSS_WIDTH)
                pygame.draw.line(screen, COLORS.CROSS, (start_x, end_y), (end_x, start_y), DIMS.CROSS_WIDTH)

    def draw_ui(self):
        pygame.draw.rect(screen, (20, 20, 20), (0, DIMS.BOARD_SIZE, DIMS.WIDTH, DIMS.HEIGHT - DIMS.BOARD_SIZE))
        score_txt = f"OM: {self.scores['X']} | AI: {self.scores['0']} | DRAWS: {self.scores['Draws']}"
        screen.blit(small_font.render(score_txt, True, COLORS.TEXT), (20, DIMS.BOARD_SIZE + 5))
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            color = COLORS.BTN_NORMAL
            if btn["rect"].collidepoint(mouse_pos):
                color = COLORS.BTN_HOVER
            if btn["val"] == self.difficulty and btn["val"] != 0:
                color = COLORS.BTN_ACTIVE
            pygame.draw.rect(screen, color, btn["rect"], border_radius=10)
            text_col = COLORS.OVERLAY if color == COLORS.BTN_ACTIVE else COLORS.TEXT
            txt_surf = small_font.render(btn["text"], True, text_col)
            screen.blit(txt_surf, txt_surf.get_rect(center=btn["rect"].center))
        if self.game_over:
            msg = font.render(self.winner_text, True, COLORS.BTN_ACTIVE)
            rect = msg.get_rect(center=(DIMS.WIDTH // 2, DIMS.BOARD_SIZE // 2))
            s = pygame.Surface((rect.width + 40, rect.height + 40))
            s.set_alpha(220)
            s.fill(COLORS.OVERLAY)
            screen.blit(s, s.get_rect(center=rect.center).topleft)
            screen.blit(msg, rect)

    def reset_game(self):
        self.logic.board = [' '] * 9
        self.game_over = False
        self.play_sound('move')

    def check_status(self):
        if self.logic.is_winner(self.logic.board, 'X'):
            self.game_over = True
            self.winner_text = "YOU WON!"
            self.scores['X'] += 1
            self.play_sound('win')
            return True
        elif self.logic.is_winner(self.logic.board, '0'):
            self.game_over = True
            self.winner_text = "AI WON!"
            self.scores['0'] += 1
            self.play_sound('over')
            return True
        elif self.logic.is_full(self.logic.board):
            self.game_over = True
            self.winner_text = "DRAW!"
            self.scores['Draws'] += 1
            self.play_sound('over')
            return True
        return False

    def run(self):
        while self.running:
            screen.fill(COLORS.BG)
            self.draw_grid_lines()
            self.draw_figures()
            self.draw_ui()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for btn in self.buttons:
                        if btn["rect"].collidepoint(pos):
                            if btn["val"] == 0:
                                self.reset_game()
                            else:
                                self.difficulty = btn["val"]
                                self.reset_game()
                    if not self.game_over and pos[1] < DIMS.BOARD_SIZE:
                        col = pos[0] // DIMS.CELL_SIZE
                        row = pos[1] // DIMS.CELL_SIZE
                        idx = row * 3 + col
                        if self.logic.board[idx] == ' ':
                            self.logic.board[idx] = 'X'
                            self.play_sound('move')
                            if not self.check_status():
                                screen.fill(COLORS.BG)
                                self.draw_grid_lines()
                                self.draw_figures()
                                self.draw_ui()
                                pygame.display.update()
                                pygame.time.delay(400)
                                ai_move = self.logic.get_ai_move(self.difficulty)
                                if ai_move is not None:
                                    self.logic.board[ai_move] = '0'
                                    self.play_sound('move')
                                    self.check_status()
            pygame.display.update()