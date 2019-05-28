import numpy as np
import pygame 
import enum

from kg_objects import Board, Grid, Unit_s, Unit_k, \
                       Blocker_x, Uid, coord_init, Team, \
                       Button

from kg_tools import get_cell_mouseover, get_unit_mouseover, \
                     coord2idx, idx2coord

from kg_draw import Draw_ui
from kg_events import Status, mouse_click_event

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# body of algorithm part
class Knight_game:
    def __init__(self, screen, clock_tick):
        self._clock_tick = clock_tick
        self._win_w, self._win_h = screen.get_size()
        self._screen = screen 
        pygame.display.set_caption("Knight Game")
        self.initialize()

    def initialize(self):
        self._grid = Grid(self._win_w, self._win_h)
        self._board = Board(self._grid)
        self._red = Team(self._grid, 0)
        self._blue = Team(self._grid, 1)
        self._units = [u for u in self._red.units] \
                    + [u for u in self._blue.units]
        self._unit_indicies = list(range(len(self._units)))
        self._buttons = [Button('New', 1), 
                         Button('Credit', 2),
                         Button('Exit', 3)]
        self._status = Status.red_idle

    def main_loop(self):
        draw = Draw_ui(self._board, self._grid, self._red, self._blue)
        clock.tick(self._clock_tick)

        while True:
            ## event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._status = mouse_click_event(
                                        self._status, 
                                        self._grid,
                                        self._units, 
                                        self._buttons) 

            draw.all(self._screen)
            pygame.display.update() 
        

