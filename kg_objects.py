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

coord_init = [[[2, 0], [2, 2], [2, 4], [2, 6], # red s
               [1, 1], [1, 3], [1, 5]],        # red k
              [[5, 0], [5, 2], [5, 4], [5, 6], # blue s
               [6, 1], [6, 3], [6, 5]]]        # blue k

imax = 7
jmax = 6

class Uid(enum.Enum):
    empty = -99;
    s1 = 0; s2 = 1; s3 = 2; s4 = 3;
    k1 = 4; k2 = 5; k3 = 6; 
    x = 99;


class Grid:
    def __init__(self, win_w, win_h):
        self._h = win_h * 0.8
        self._w = self._h * 7./8
        self._x = (win_w - self._w)/2
        self._y = (win_h - self._h)/2

        self._grid_pos = grid0 * self._h / 7
        self._grid_pos[:, :, 0] += self._x
        self._grid_pos[:, :, 1] += self._y
        self._grid_stat = np.full(56, Uid.empty.value, dtype=int)
        self._grid_idx = [(i, j) for j in range(8) for i in range(7)]

        self._cell_w = self._grid_pos[0, 1, 0] - self._grid_pos[0, 0, 0]
        self._cell_h = self._grid_pos[1, 0, 1] - self._grid_pos[0, 0, 1]
        self._cell_rects = [] 
        self._define_cell_rects()

    def draw(self, screen):
        # Horizontal lines
        for i in range(7):
            pygame.draw.line(screen, cBLACK, self._grid_pos[0, i], self._grid_pos[-1, i], 1)

        # Vertical lines
        for i in range(8):  
            pygame.draw.line(screen, cBLACK, self._grid_pos[i, 0], self._grid_pos[i, -1], 1)

    def _define_cell_rects(self):
        for i in range(8):
            for j in range(7):
                rect = pygame.Rect((0, 0), (self._cell_w, self._cell_h)) 
                rect.center = (self._grid_pos[i, j, 0], self._grid_pos[i, j, 1])
                self._cell_rects.append(rect)

    @property
    def grid_pos(self):
        return self._grid_pos

    @property
    def cell_rects(self):
        return self._cell_rects 

    @property
    def stat(self):
        return self._grid_stat


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
        self._x, self._y = self._grid.grid_pos[self._i, self._j]
        self._side = side
        self._uid = uid
        self._grid.stat[coord2idx(self._i, self._j)] = self._uid
        self._is_alive = 1
        self._rect = []
        self._movable_cells = []
        self.set_movable_cells()

    def draw_octagon(self, screen):
        octagon_s = octagon0 * self._scale + np.array([self._x, self._y])
        shadow_s = (octagon0 + 0.1)* self._scale + np.array([self._x, self._y])
        pygame.draw.polygon(screen, sBGND, shadow_s, 0)
        obj = pygame.draw.polygon(screen, cWHITE, octagon_s, 0)
        pygame.draw.polygon(screen, cBLACK, octagon_s, 1)
        self._rect = obj

    def move(self, dest):
        if dest in self._movable_cells: 
            orig = coord2idx(self._i, self._j)
            self._grid.stat[orig] = Uid.empty.value
            self._i, self._j = idx2coord(dest)
            self._grid.stat[dest] = self._uid
            self._x, self._y = self._grid.grid_pos[self._i, self._j]
            self.set_movable_cells()
        else:
            self._x, self._y = self._grid.grid_pos[self._i, self._j]
            self.set_movable_cells()

    def set_movable_cells(self):
        pass

    def draw_movable_cells(self, screen):
        for idx in self._movable_cells:
            pos = self._grid._grid_pos[idx2coord(idx)]
            pygame.draw.circle(screen, cGREEN, (int(pos[0]), int(pos[1])), 15, 5)

    @property
    def rect(self):
        return self._rect

    @property
    def movable_cells(self):
        return self._movable_cells

    @property
    def uid(self):
        return self._uid


class Unit_s(Unit):
    def __init__(self, grid, coord, side, uid):
        self._grid = grid
        self._i, self._j = coord
        self._x, self._y = self._grid.grid_pos[self._i, self._j]
        self._side = side
        self._uid = uid
        self._grid.stat[coord2idx(self._i, self._j)] = self._uid
        self._is_alive = 1
        self._scale = grid._cell_w / 2 * 0.7
        self._rect = []
        self._movable_cells = []
        self.set_movable_cells()

    def draw_s(self, screen):
        if self._side == 0:
            color = cRED
        elif self._side == 1:
            color = cBLUE

        font_s = pygame.font.SysFont(None, 50)
        text_s = font_s.render('S', False, color)
        w = text_s.get_width()
        h = text_s.get_height()
        screen.blit(text_s, (self._x - w/2, self._y - h/2))

    def draw(self, screen):
        self.draw_octagon(screen)
        self.draw_s(screen)

    def set_movable_cells(self):
        self._movable_cells = []
        if self._i > 0:
            dest = coord2idx(self._i-1, self._j)
            if self._grid.stat[dest] == Uid.empty.value:
                self._movable_cells.append(dest)
        if self._j > 0:
            dest = coord2idx(self._i, self._j-1)
            if self._grid.stat[dest] == Uid.empty.value:
                self._movable_cells.append(dest)
        if self._j < 6:
            dest = coord2idx(self._i, self._j+1)
            if self._grid.stat[dest] == Uid.empty.value:
                self._movable_cells.append(dest)
        if self._i < 7:
            dest = coord2idx(self._i+1, self._j)
            if self._grid.stat[dest] == Uid.empty.value:
                self._movable_cells.append(dest)


class Unit_k(Unit):
    def __init__(self, grid, coord, side, uid):
        self._grid = grid
        self._i, self._j = coord 
        self._x, self._y = self._grid.grid_pos[self._i, self._j]
        self._side = side
        self._uid = uid
        self._grid.stat[coord2idx(self._i, self._j)] = self._uid
        self._is_alive = 1
        self._scale = grid._cell_w / 2 
        self._rect = []
        self._movable_cells = []
        self.set_movable_cells()

    def draw_k(self, screen):
        if self._side == 0:
            color = cRED
        elif self._side ==1:
            color = cBLUE

        font_s = pygame.font.SysFont(None, 70)
        text_s = font_s.render('K', False, color)
        w = text_s.get_width()
        h = text_s.get_height()
        screen.blit(text_s, (self._x - w/2, self._y - h/2))

    def draw(self, screen):
        self.draw_octagon(screen)
        self.draw_k(screen)

    def set_movable_cells(self):
        self._movable_cells = []
        if self._i > 1:
            stopover = coord2idx(self._i-1, self._j)
            if self._grid.stat[stopover] == Uid.empty.value:
                if self._j > 0:
                    dest = coord2idx(self._i-2, self._j-1)
                    if self._grid.stat[dest] == Uid.empty.value:
                        print ("#1")
                        self._movable_cells.append(dest)
                if self._j < jmax:
                    dest = coord2idx(self._i-2, self._j+1)
                    if self._grid.stat[dest] == Uid.empty.value:
                        print ("#2")
                        self._movable_cells.append(dest)
            
        if self._j > 1:
            stopover = coord2idx(self._i, self._j-1)
            if self._grid.stat[stopover] == Uid.empty.value:
                if self._i > 0:
                    dest = coord2idx(self._i-1, self._j-2)
                    if self._grid.stat[dest] == Uid.empty.value:
                        print ("#3")
                        self._movable_cells.append(dest)
                if self._i < imax:
                    dest = coord2idx(self._i+1, self._j-2)
                    if self._grid.stat[dest] == Uid.empty.value:
                        print ("#4")
                        self._movable_cells.append(dest)

        if self._j < jmax-1:
            stopover = coord2idx(self._i, self._j+1)
            if self._grid.stat[stopover] == Uid.empty.value:
                if self._i > 0:
                    dest = coord2idx(self._i-1, self._j+2)
                    if self._grid.stat[dest] == Uid.empty.value:
                        print ("#5")
                        self._movable_cells.append(dest)
                if self._i < imax:
                    dest = coord2idx(self._i+1, self._j+2)
                    if self._grid.stat[dest] == Uid.empty.value:
                        print ("#6")
                        self._movable_cells.append(dest)

        if self._i < imax-1:
            stopover = coord2idx(self._i+1, self._j)
            if self._grid.stat[stopover] == Uid.empty.value:
                if self._j > 0:
                    dest = coord2idx(self._i+2, self._j-1)
                    if self._grid.stat[dest] == Uid.empty.value:
                        print ("#7")
                        self._movable_cells.append(dest)
                if self._j < jmax:
                    dest = coord2idx(self._i+2, self._j+1)
                    if self._grid.stat[dest] == Uid.empty.value:
                        print ("#8")
                        self._movable_cells.append(dest)
        return


class Team:
    def __init__(self, grid, side):
        self._grid = grid
        self._units = []
        self._side = side
        self.max_x = 56
        self.cnt_x = 0
        self.cnt_alive_s = 4
        self.cnt_alive_k = 3
        self.set_units()

    def set_units(self):
        for unit_id in Uid: 
            if unit_id.value < 0:
                pass
            elif unit_id.value < 4:
                self._units.append(
                    Unit_s(
                        self._grid, 
                        coord_init[self._side][unit_id.value], 
                        self._side, 
                        self._side*7+unit_id.value
                        )
                    )
            elif unit_id.value < 7:
                self._units.append(
                    Unit_k(
                        self._grid, 
                        coord_init[self._side][unit_id.value], 
                        self._side, 
                        self._side*7+unit_id.value
                        )
                    )
        return

    def draw_units(self, screen):
        for u in self._units:
            if u._is_alive:
                u.draw(screen)

    @property
    def units(self):
        return self._units


class Blocker_x:
    pass


def coord2idx(i, j):
    return i*7 + j


def idx2coord(idx):
    return divmod(idx, 7)
