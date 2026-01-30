from collections import namedtuple
from pathlib import Path

import pygame

SOUND_DIR = Path(__file__).resolve().parent / "sounds"

ColorConfig = namedtuple('ColorConfig', [
    'BG', 'LINE', 'CIRCLE', 'CROSS', 'TEXT',
    'BTN_NORMAL', 'BTN_HOVER', 'BTN_ACTIVE', 'OVERLAY'
])

DimConfig = namedtuple('DimConfig', [
    'WIDTH', 'HEIGHT', 'BOARD_SIZE', 'CELL_SIZE',
    'LINE_WIDTH', 'CIRCLE_RADIUS', 'CIRCLE_WIDTH',
    'CROSS_WIDTH', 'SPACE'
])

_BOARD_SIZE = 600
_CELL_SIZE = _BOARD_SIZE // 3

COLORS = ColorConfig(
    BG=(28, 170, 156),
    LINE=(23, 145, 135),
    CIRCLE=(239, 231, 200),
    CROSS=(84, 84, 84),
    TEXT=(255, 255, 255),
    BTN_NORMAL=(20, 120, 110),
    BTN_HOVER=(28, 170, 156),
    BTN_ACTIVE=(255, 200, 50),
    OVERLAY=(0, 0, 0)
)

DIMS = DimConfig(
    WIDTH=600,
    HEIGHT=700,
    BOARD_SIZE=_BOARD_SIZE,
    CELL_SIZE=_CELL_SIZE,
    LINE_WIDTH=10,
    CIRCLE_RADIUS=_CELL_SIZE // 3,
    CIRCLE_WIDTH=15,
    CROSS_WIDTH=20,
    SPACE=55
)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((DIMS.WIDTH, DIMS.HEIGHT))
pygame.display.set_caption("TicTacToe - NamedTuple Edition")

font = pygame.font.SysFont('consolas', 30, bold=True)
small_font = pygame.font.SysFont('consolas', 20)

