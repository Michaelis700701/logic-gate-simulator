import pygame
from settings import *
from pygame.math import Vector2


class LogicGate():
    def __init__(
            self,
            position: Vector2,
            name: str,
            symbol_label: str,
            connector_inputs: list,
            connector_outputs: list,
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
        self.connector_inputs = connector_inputs
        self.connector_outputs = connector_outputs
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
        for index, input in enumerate(self.connector_inputs):
            self.connector_list.append(
                Connector(
                    self,
                    Vector2(
                        -CONNECTOR_SIZE.x,
                        (
                            (self.block_rect.height - (self.connectors_height_margin * (len(self.connector_inputs) - 1) + CONNECTOR_SIZE.y * len(self.connector_inputs))) / 2
                        ) + (
                            (self.connectors_height_margin + CONNECTOR_SIZE.y) * index
                        )
                    ),
                    True,
                    input
                )
            )
        for index, output in enumerate(self.connector_outputs):
            self.connector_list.append(
                Connector(
                    self,
                    Vector2(
                        self.block_rect.width,
                        (
                            (self.block_rect.height - (self.connectors_height_margin * (len(self.connector_outputs) - 1) + CONNECTOR_SIZE.y * len(self.connector_outputs))) / 2
                        ) + (
                            (self.connectors_height_margin + CONNECTOR_SIZE.y) * index
                        )
                    ),
                    False,
                    output
                )
            )

        for connector in self.connector_list:
            self.image.blit(connector.surface, connector.relative_position_from_logic_gate + Vector2(CONNECTOR_SIZE.x, 0))


    def _create_image(
            self
    ) -> None:
        """
        Creates the image of the logic gate and the rect.
        """
        max_connectors = max(len(self.connector_inputs), len(self.connector_outputs))
        self.block_rect = pygame.Rect(
            self.position + Vector2(CONNECTOR_SIZE.x, 0),
            (
                self.symbol_label.get_width() + self.symbol_label_width_margin * 2,
                (self.connectors_height_margin * (max_connectors + 1)) + CONNECTOR_SIZE.y * max_connectors
            )
        )

        self.image = pygame.Surface(
            (
                self.block_rect.width + (CONNECTOR_SIZE.x * 2),
                self.block_rect.height
            ),
            pygame.SRCALPHA
        ).convert_alpha()
        
        block_rect_copy = self.block_rect.copy()
        block_rect_copy.topleft = (CONNECTOR_SIZE.x, 0)
        pygame.draw.rect(self.image, WHITE, block_rect_copy)
        pygame.draw.rect(self.image, BLACK, block_rect_copy, 2)
        self.rect = self.image.get_rect()


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
            name: str
    ) -> None:
        """
        SubAsset
        ------
        This is a sub asset class for the connectors for logic gates.

        Parameters
        ----------
        logic_gate : LogicGate
            The logic gate object that this connector is connected to.
        relative_position_from_logic_gate : Vector2
            The position from the logic gate center.
        is_input : bool
            if the connector is an input or output.
        name : str
            The name of the connector.
        """
        self.logic_gate = logic_gate
        self.relative_position_from_logic_gate = relative_position_from_logic_gate
        self.is_input = is_input
        self.name = name
        self.value = 0
        self.surface = pygame.Surface(CONNECTOR_SIZE, pygame.SRCALPHA).convert_alpha()
        self.__create_image()

        self.rect = pygame.Rect(
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
        
        if self.is_input:
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
        
        else:
            pygame.draw.circle(
                self.surface,
                WHITE,
                (self.surface.get_width() - radius, radius),
                radius
            )
            pygame.draw.circle(
                self.surface,
                BLACK,
                (self.surface.get_width() - radius, radius),
                radius,
                width
            )