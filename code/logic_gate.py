import pygame
from settings import *
from pygame.math import Vector2
from typing import Literal


class LogicGate():
    def __init__(
            self,
            position: Vector2,
            name: str,
            symbol_label: str,
            connectors: dict[Literal['N', 'E', 'S', 'W'], list[tuple[str, bool]]],
            sandbox: object
    ) -> None:
        """
        Asset
        ------
        This is an Asset parent class for all logic gates.

        Parameters
        ----------
        type : str
        """
        self.sandbox = sandbox
        self.font = pygame.Font("assets/text/Arial.ttf", 15)
        self.name = name
        self.symbol_label = self.font.render(symbol_label, True, BLACK)
        self.connectors: dict = connectors
        self.position = position
        self.symbol_label_width_margin = 10
        self.connectors_height_margin = 20
        self.picked_up = False
        self._create_image()
        self._create_connectors()
    

    def _create_connectors(
            self
    ) -> None:
        """
        Creates the input and output connectors of the logic gate.
        """
        self.connector_list: list[Connector] = []
        
        for direction in self.connectors:
            for index, name_isinput_tuple in enumerate(self.connectors[direction]):

                if direction == "N":
                    relative_position_from_logic_gate = Vector2(
                        (
                            (self.block_rect.width - (self.connectors_height_margin * (len(self.connectors[direction]) - 1) + CONNECTOR_SIZE.y * len(self.connectors[direction]))) / 2
                        ) + (
                            (self.connectors_height_margin + CONNECTOR_SIZE.y) * index
                        ), 
                        -CONNECTOR_SIZE.x
                    )
                elif direction == "E":
                    relative_position_from_logic_gate = Vector2(
                        self.block_rect.width,
                        (
                            (self.block_rect.height - (self.connectors_height_margin * (len(self.connectors[direction]) - 1) + CONNECTOR_SIZE.y * len(self.connectors[direction]))) / 2
                        ) + (
                            (self.connectors_height_margin + CONNECTOR_SIZE.y) * index
                        )
                    )
                elif direction == "S":
                    relative_position_from_logic_gate = Vector2(
                        (
                            (self.block_rect.width - (self.connectors_height_margin * (len(self.connectors[direction]) - 1) + CONNECTOR_SIZE.y * len(self.connectors[direction]))) / 2
                        ) + (
                            (self.connectors_height_margin + CONNECTOR_SIZE.y) * index
                        ),
                        self.block_rect.height
                    )
                else:
                    relative_position_from_logic_gate = Vector2(
                        -CONNECTOR_SIZE.x,
                        (
                            (self.block_rect.height - (self.connectors_height_margin * (len(self.connectors[direction]) - 1) + CONNECTOR_SIZE.y * len(self.connectors[direction]))) / 2
                        ) + (
                            (self.connectors_height_margin + CONNECTOR_SIZE.y) * index
                        )
                    )

                self.connector_list.append(
                    Connector(
                        self,
                        relative_position_from_logic_gate,
                        name_isinput_tuple[1],
                        direction,
                        name_isinput_tuple[0]
                    )
                )

        for connector in self.connector_list:
            self.image.blit(connector.surface, connector.relative_position_from_logic_gate + Vector2(CONNECTOR_SIZE.x, CONNECTOR_SIZE.x))


    def _create_image(
            self
    ) -> None:
        """
        Creates the image of the logic gate and the rect.
        """
        """
        if not len(self.connectors['N']) == 0 or not len(self.connectors['S']) == 0:
            max_connectors_x = max(len(self.connectors['N']), len(self.connectors['S']))
        elif len(self.connectors['N']) == 0:
            max_connectors_x = len(self.connectors['S'])
        else:
            max_connectors_x = len(self.connectors['N'])
        if not len(self.connectors['E']) == 0 or not len(self.connectors['W']) == 0:
            max_connectors_y = max(len(self.connectors['E']), len(self.connectors['W']))
        elif len(self.connectors['E']) == 0:
            max_connectors_y = len(self.connectors['W'])
        else:
            max_connectors_y = len(self.connectors['E'])
        """
        max_connectors_x = max(len(self.connectors['N']), len(self.connectors['S']))
        max_connectors_y = max(len(self.connectors['W']), len(self.connectors['E']))
        if ((self.connectors_height_margin * (max_connectors_x + 1)) + CONNECTOR_SIZE.y * max_connectors_x) > self.symbol_label.get_width() + self.symbol_label_width_margin * 2:
            self.block_rect = pygame.Rect(
                self.position + Vector2(CONNECTOR_SIZE.x, 0),
                (
                    (self.connectors_height_margin * (max_connectors_x + 1)) + CONNECTOR_SIZE.y * max_connectors_x,
                    (self.connectors_height_margin * (max_connectors_y + 1)) + CONNECTOR_SIZE.y * max_connectors_y
                )
            )
        else:
            self.block_rect = pygame.Rect(
                self.position + Vector2(CONNECTOR_SIZE.x, 0),
                (
                    self.symbol_label.get_width() + self.symbol_label_width_margin * 2,
                    (self.connectors_height_margin * (max_connectors_y + 1)) + CONNECTOR_SIZE.y * max_connectors_y
                )
            )
        
        self.image = pygame.Surface(
            (
                self.block_rect.width + (CONNECTOR_SIZE.x * 2),
                self.block_rect.height + (CONNECTOR_SIZE.x * 2)
            ),
            pygame.SRCALPHA
        ).convert_alpha()
        
        self.rect = self.image.get_rect()
        
        block_rect_copy = self.block_rect.copy()
        block_rect_copy.topleft = (CONNECTOR_SIZE.x, CONNECTOR_SIZE.x)

        pygame.draw.rect(self.image, WHITE, block_rect_copy)
        pygame.draw.rect(self.image, BLACK, block_rect_copy, 2)
        self.image.blit(self.symbol_label, block_rect_copy.center - (Vector2(self.symbol_label.get_size()) / 2))


    def pick_up(
            self,
            event: pygame.event.Event
    ) -> None:
        """
        Checks if the logic gate is picked up and moves it to the cursor if it is
        and moves it to the dropped position.

        Parameters
        ----------
        event : Event
            Paramenter from the pygame method pygame.event.get() in the event loop.
        """
        mouse_pos_relative_to_origin = (Vector2(pygame.mouse.get_pos()) / self.sandbox.zoom) - self.sandbox.origin
        mouse_pressed = pygame.mouse.get_pressed()

        if self.block_rect.collidepoint(mouse_pos_relative_to_origin.x, mouse_pos_relative_to_origin.y):
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_pressed[0]:
                self.sandbox.pan_active = False
                self.picked_up = True
                self.mouse_pos_relitive_from_block_rect_center = mouse_pos_relative_to_origin - self.block_rect.center
        if event.type == pygame.MOUSEBUTTONUP and self.picked_up == True:
            self.picked_up = False
            self.mouse_pos_relitive_from_block_rect_center = Vector2(0, 0)
        
        if self.picked_up:
            self.block_rect.center = mouse_pos_relative_to_origin - self.mouse_pos_relitive_from_block_rect_center
            self.rect.center = mouse_pos_relative_to_origin - self.mouse_pos_relitive_from_block_rect_center
            self.position = self.rect.topleft
    

class Connector():
    def __init__(
            self,
            logic_gate: LogicGate,
            relative_position_from_logic_gate: Vector2,
            is_input: bool,
            logic_gate_side: Literal['N', 'E', 'S', 'W'],
            name: str
    ) -> None:
        """
        SubAsset
        --------
        This is a sub asset class for the connectors for logic gates.

        Parameters
        ----------
        logic_gate : LogicGate
            The logic gate object that this connector is connected to.
        relative_position_from_logic_gate : Vector2
            The position from the logic gate center.
        is_input : bool
            if the connector is an input or output.
        logic_gate_side : Literal['N', 'E', 'S', 'W']
            The logic gate side the connector is on ['N', 'E', 'S', 'W'] for cardinal directions.
        name : str
            The name of the connector.
        """
        self.logic_gate: LogicGate = logic_gate
        self.relative_position_from_logic_gate: Vector2 = relative_position_from_logic_gate
        self.is_input: bool = is_input
        self.logic_gate_side: Vector2 = logic_gate_side
        self.name: str = name
        self.value: int = 0
        self.surface: pygame.Surface = pygame.Surface(CONNECTOR_SIZE, pygame.SRCALPHA).convert_alpha()
        self.__create_image()

        self.rect: pygame.Rect = pygame.Rect(
            (self.logic_gate.position + self.relative_position_from_logic_gate),
            CONNECTOR_SIZE
        )
    

    def __create_image(self) -> None:
        """
        Creates the image of the connector depending on if it an input or not
        """
        radius = CONNECTOR_SIZE.y / 2
        width = 2

        pygame.draw.line(self.surface, BLACK, (0, radius), (self.surface.get_width(), radius), width)
        
        
        pygame.draw.circle(
            self.surface,
            WHITE,
            (radius, radius),
            radius
        )
        pygame.draw.circle(
            self.surface,
            BLACK,
            (radius, radius),
            radius,
            width
        )

        if self.logic_gate_side == "N":
            self.surface = pygame.transform.rotate(self.surface, 270)
        elif self.logic_gate_side == "E":
            self.surface = pygame.transform.rotate(self.surface, 180)
        elif self.logic_gate_side == "S":
            self.surface = pygame.transform.rotate(self.surface, 90)