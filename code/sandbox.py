import pygame
from pygame.math import Vector2
from settings import *
from pygame_support.support.app_state import AppState

class Sandbox(AppState):
    def __init__(self) -> None:
        """
        Appstate
        --------
        This class takes inputs and simulates logic gates.
        """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, KEYS_PRESSED, zoomable=True, panable=True)

        self.grid_spacing = Vector2(25, 25)


    def draw_grid_lines(self) -> None:
        """
        This method draws grid lines onto this class' surface.
        TODO: make the grid lines a set size while zooming to make sure it does not change thickness
        """
        origin_multiple = self.origin - Vector2(
            x = self.origin.x - int(self.origin.x / self.grid_spacing.x) * self.grid_spacing.x,
            y = self.origin.y - int(self.origin.y / self.grid_spacing.y) * self.grid_spacing.y
        )

        relative_origin = self.origin - origin_multiple

        for line_x_pos in range(int(relative_origin.x), int(self.surface.get_width() + relative_origin.x), int(self.grid_spacing.x)):
            line_start_pos = (line_x_pos, 0)
            line_end_pos = (line_x_pos, relative_origin.y + self.surface.get_height())

            pygame.draw.line(self.surface, GRID_LINE_COLOR, line_start_pos, line_end_pos)

        for line_y_pos in range(int(relative_origin.y), int(self.surface.get_height() + relative_origin.y), int(self.grid_spacing.y)):
            line_start_pos = (0, line_y_pos)
            line_end_pos = (relative_origin.x + self.surface.get_width(), line_y_pos)

            pygame.draw.line(self.surface, GRID_LINE_COLOR, line_start_pos, line_end_pos)


    def draw_assets(self) -> None:
        """
        Draws all assets onto surface.
        """
        pygame.draw.circle(self.surface, WHITE, self.origin, 10)
        self.draw_grid_lines()