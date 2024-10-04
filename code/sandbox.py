import pygame
from pygame.math import Vector2
from settings import *
from pygame_support.support.app_state import AppState
from logic_gate import LogicGate

class Sandbox(AppState):
    def __init__(self) -> None:
        """
        Appstate
        --------
        This class takes inputs and simulates logic gates.
        """
        super().__init__(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            BACKGROUND_COLOR,
            KEYS_PRESSED,
            zoomable=True,
            panable=True,
            maximum_zoom=2,
            minimum_zoom=0.34)

        self.grid_spacing = Vector2(25, 25)
        self.logic_gate_list = [LogicGate(Vector2(25, 25),'TEST GATE', 'TEST GATE', ['1', '2', '3', '4'], ['1'], self)]


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


    def draw_logic_gates(self) -> None:
        """
        Draws all logic gates in the logic_gate_list.
        """
        for logic_gate in self.logic_gate_list:
            self.surface.blit(logic_gate.image, logic_gate.position + self.origin)


    def event_loop(self, event) -> None:
        """
        """
        for logic_gate in self.logic_gate_list:
            logic_gate.pick_up(event)
            print(logic_gate.picked_up)


    def draw_assets(self) -> None:
        """
        Draws all assets onto surface.
        """
        pygame.draw.circle(self.surface, WHITE, self.origin, 10)
        self.draw_grid_lines()
        self.draw_logic_gates()