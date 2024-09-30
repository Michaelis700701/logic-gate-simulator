import pygame

WINDOW_WIDTH = (16 * 64) * 1.2
WINDOW_HEIGHT = (9 * 64) * 1.2

TILE_SIZE = 64

ACTIVE_STATE = {'active_state': None}

TEXT_FONT = 'assets/text/Arial.ttf'

KEYS_PRESSED = {
    pygame.K_F3: False,
    pygame.K_UP: False,
    pygame.K_RIGHT: False,
    pygame.K_DOWN: False,
    pygame.K_LEFT: False,
}


# Colors

BACKGROUND_COLOR = (50, 50, 50)
GRID_LINE_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)