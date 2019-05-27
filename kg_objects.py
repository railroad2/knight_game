import numpy as np
import pygame
import enum

cBLACK = (  0,   0,   0)
cWHITE = (255, 255, 255)
cBLUE  = (  0,   0, 255)
cGREEN = (  0, 255,   0)
cRED   = (255,   0,   0)
cBOARD = (0xbc, 0x5e, 0)
cBGND  = (0x4b, 0x4b, 0x4b)
sBGND  = (0x3c, 0x3c, 0x3c)

grid0 = np.transpose(np.array(np.meshgrid(np.arange(7), np.arange(8))), (1,2,0))
ang = np.arange(8) * np.pi/4 + np.pi/8
octagon0 = np.array([np.cos(ang), np.sin(ang)]).T 
polygon_s0 = np.array([[0,0], [1, 0], [1, 1], [0, 1]]) - np.array((0.5, 0.5))
polygon_k0 = np.array([[0,0], [1, 0], [1, 1], [0, 1]]) - np.array((0.5, 0.5))

coord_init = [ [2, 0], [2, 2], [2, 4], [2, 6],
              [1, 1], [1, 3], [1, 5],
              [5, 0], [5, 2], [5, 4], [5, 6],
              [6, 1], [6, 3], [6, 5]]


class Uid(enum.Enum):
    empty = -1
    r_s1 = 0; r_s2 = 1; r_s3 = 2; r_s4 = 3;
    r_k1 = 4; r_k2 = 5; r_k3 = 6;
    b_s1 = 7; b_s2 = 8; b_s3 = 9; b_s4 = 10;
    b_k1 = 11; b_k2 = 12; b_k3 = 13;


class Grid:
    def __init__(self, win_w, win_h):
        self._h = win_h * 0.8
        self._w = self._h * 7./8
        self._grid = grid0 * self._h / 7
        self._cell_w  = self._grid[0, 1, 0] - self._grid[0, 0, 0]
        self._cell_h = self._grid[1, 0, 1] - self._grid[0, 0, 1]
        self._x = (win_w - self._w)/2
        self._y = (win_h - self._h)/2
        self._grid[:, :, 0] += self._x
        self._grid[:, :, 1] += self._y
        self._stat = np.zeros((7, 8))

    def draw(self, screen):
        # Horizontal lines
        for i in range(7):
            pygame.draw.line(screen, cBLACK, self._grid[0, i], self._grid[-1, i], 1)

        # Vertical lines
        for i in range(8):  
            pygame.draw.line(screen, cBLACK, self._grid[i, 0], self._grid[i, -1], 1)

    @property
    def grid(self):
        return self._grid


class Board:
    def __init__(self, grid):
        self._w = grid._w + grid._cell_w
        self._h = grid._h + grid._cell_h
        self._x = grid._x - grid._cell_w/2
        self._y = grid._y - grid._cell_h/2
        self._d = grid._w/40
        self._rect = [self._x, self._y, self._w, self._h]
        self._shadow = [self._x + self._d, self._y + self._d, self._w, self._h]

    def draw(self, screen):
        pygame.draw.rect(screen, sBGND, self._shadow, 0)
        pygame.draw.rect(screen, cBOARD, self._rect, 0)


class Unit:
    def __init__(self, grid, coord, side, uid):
        self._grid = grid
        self._i, self_j = coord 
        self._x, self._y = self._grid.grid[self._i, self._j]
        self._side = side
        self._grid._stat[self._i, self._j] = self._side
        self._is_alive = 1
        self._uid = uid
        self._rect = []

    def draw_octagon(self, screen):
        octagon_s = octagon0 * self._scale + np.array([self._x, self._y])
        shadow_s = (octagon0 + 0.1)* self._scale + np.array([self._x, self._y])
        pygame.draw.polygon(screen, sBGND, shadow_s, 0)
        obj = pygame.draw.polygon(screen, cWHITE, octagon_s, 0)
        self._rect = obj

    def move(self, coord):
        self._grid._stat[self._i, self._j] = -1
        self._i, self._j = coord
        self._grid._stat[self._i, self._j] = self._uid
        self._x, self._y = self._grid.grid[self._i, self._j]

    def get_rect(self):
        return self._rect


class Unit_s(Unit):
    def __init__(self, grid, coord, side, uid):
        self._grid = grid
        self._i, self._j = coord
        self._x, self._y = self._grid.grid[self._i, self._j]
        self._side = side
        self._uid = uid
        self._grid._stat[self._i, self._j] = self._uid
        self._is_alive = 1
        self._scale = grid._cell_w / 2 * 0.7
        self._rect = []

    def draw_s(self, screen):
        if self._side == 1:
            color = cRED
        elif self._side == 2:
            color = cBLUE

        font_s = pygame.font.SysFont(None, 50)
        text_s = font_s.render('S', False, color)
        w = text_s.get_width()
        h = text_s.get_height()
        screen.blit(text_s, (self._x - w/2, self._y - h/2))

    def draw(self, screen):
        self.draw_octagon(screen)
        self.draw_s(screen)


class Unit_k(Unit):
    def __init__(self, grid, coord, side, uid):
        self._grid = grid
        self._i, self._j = coord 
        self._x, self._y = self._grid.grid[self._i, self._j]
        self._side = side
        self._uid = uid
        self._grid._stat[self._i, self._j] = self._uid
        self._is_alive = 1
        self._scale = grid._cell_w / 2 
        self._rect = []

    def draw_k(self, screen):
        if self._side == 1:
            color = cRED
        else:
            color = cBLUE

        font_s = pygame.font.SysFont(None, 70)
        text_s = font_s.render('K', False, color)
        w = text_s.get_width()
        h = text_s.get_height()
        screen.blit(text_s, (self._x - w/2, self._y - h/2))

    def draw(self, screen):
        self.draw_octagon(screen)
        self.draw_k(screen)


class Blocker_x:
    pass


