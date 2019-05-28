import pygame
import numpy as np

cBLACK = (  0,   0,   0)
cWHITE = (255, 255, 255)
cBLUE  = (  0,   0, 255)
cGREEN = (  0, 255,   0)
cRED   = (255,   0,   0)
cBOARD = (0xbc, 0x5e, 0)
cBGND  = (0x4b, 0x4b, 0x4b)
sBGND  = (0x3c, 0x3c, 0x3c)

ang = np.arange(8) * np.pi/4 + np.pi/8
octagon0 = np.array([np.cos(ang), np.sin(ang)]).T 

class Draw_ui:
    def __init__(self, board, grid, red, blue):
        self._board = board
        self._grid = grid
        self._red = red
        self._blue = blue
        self._units = [u for u in red.units] \
                    + [u for u in blue.units]

        self._font_s = pygame.font.SysFont(None, 50)
        self._text_rs = self._font_s.render('S', False, cRED)
        self._text_bs = self._font_s.render('S', False, cBLUE)
        self._font_k = pygame.font.SysFont(None, 70)
        self._text_rk = self._font_k.render('K', False, cRED)
        self._text_bk = self._font_k.render('K', False, cBLUE)
        self._s_w = self._text_rs.get_width()
        self._s_h = self._text_rs.get_height()
        self._k_w = self._text_rk.get_width()
        self._k_h = self._text_rk.get_height()

    def clear(self, screen):
        screen.fill(cBGND) 

    def all(self, screen):
        #self.clear(screen)
        #self._board.draw(screen) 
        #self._red.draw_units(screen)
        #self._blue.draw_units(screen)
        self.clear(screen) 
        self.board(screen)
        self.all_units(screen)

    def board(self, screen):
        pygame.draw.rect(screen, sBGND, self._board._shadow, 0)
        pygame.draw.rect(screen, cBOARD, self._board._rect, 0)
        # drawing grid lines
        for i in range(7):
            pygame.draw.line(
                screen, 
                cBLACK, 
                self._grid._grid_pos[0, i], 
                self._grid._grid_pos[-1, i], 
                1)
        for i in range(8):
            pygame.draw.line(
                screen, 
                cBLACK, 
                self._grid._grid_pos[i, 0], 
                self._grid._grid_pos[i, -1], 
                1)

    def draw_octagon(self, screen, unit):
        if unit.type == 's': 
            scale = self._grid._cell_w / 2 * 0.7
        elif unit.type == 'k':
            scale = self._grid._cell_w / 2

        octagon = octagon0 * scale + np.array([unit._x, unit._y])
        shadow = (octagon0 + 0.1)* scale + np.array([unit._x, unit._y])
        pygame.draw.polygon(screen, sBGND, shadow, 0)
        obj = pygame.draw.polygon(screen, cWHITE, octagon, 0)
        pygame.draw.polygon(screen, cBLACK, octagon, 1)
        unit.rect = obj 

    def char_s(self, screen, unit):
        if unit.side == 0:
            screen.blit(self._text_rs, (unit._x - self._s_w/2, unit._y - self._s_h/2))
        elif unit.side == 1:
            screen.blit(self._text_bs, (unit._x - self._s_w/2, unit._y - self._s_h/2))
        

    def char_k(self, screen, unit):
        if unit.side == 0:
            screen.blit(self._text_rk, (unit._x - self._k_w/2, unit._y - self._k_h/2))
        elif unit.side == 1:
            screen.blit(self._text_bk, (unit._x - self._k_w/2, unit._y - self._k_h/2))


    def an_unit(self, screen, unit):
        self.draw_octagon(screen, unit)
        if unit.type == 's':
            self.char_s(screen, unit)
        elif unit.type == 'k':
            self.char_k(screen, unit)

    def all_units(self, screen):
        for u in self._units:
            self.an_unit(screen, u)

            
if __name__=='__main__':
    from kg_objects import Board, Grid, Team
    pygame.init()
    pygame.font.init()
    win_w = 800
    win_h = win_w * 3 // 4
    screen = pygame.display.set_mode([win_w, win_h])

    pygame.display.set_caption("ui test")
    grid = Grid(win_w, win_h)
    board = Board(grid)
    red = Team(grid, 0)
    blue = Team(grid, 1)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
        draw = Draw_ui(board, grid, red, blue) 
        draw.all(screen)

        pygame.display.update()
