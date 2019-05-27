import numpy as np
import pygame

import kg_objects as ko 
from kg_objects import Board, Grid, Unit_s, Unit_k, Blocker_x, Uid, coord_init

def get_cell_mouseover(grid):
    cells = grid.cell_rects
    point = pygame.mouse.get_pos()
    for i, cell in enumerate(cells):
        if cell.collidepoint(point):
            return i

    return -1

def main():
    pygame.init()
    pygame.font.init()
    win_w = 800
    win_h = win_w * 3 // 4
    screen = pygame.display.set_mode([win_w, win_h])
    pygame.display.set_caption("Knight Game")


    grid = Grid(win_w, win_h)
    board = Board(grid) 

    ## defining units
    units = []
    for name in Uid:
        val = name.value
        if (val < 0):
            pass
        elif (val < 4):
            units.append(Unit_s(grid, coord_init[val], 1, val))
        elif (val < 7):
            units.append(Unit_k(grid, coord_init[val], 1, val))
        elif (val < 11):
            units.append(Unit_s(grid, coord_init[val], 2, val))
        elif (val < 14):
            units.append(Unit_k(grid, coord_init[val], 2, val))

    # states
    done = False
    moving = False
    drop = False
    clock = pygame.time.Clock()

    ## main loop
    while not done:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if moving == False: 
                    moving = True
                elif moving == True:
                    moving = False
                    drop = True

        screen.fill(ko.cBGND)

        board.draw(screen)
        grid.draw(screen)

        print (pygame.mouse.get_pos())
        for u in units:
            u.draw(screen)
            if moving == False:
                if u.rect.collidepoint(pygame.mouse.get_pos()):
                    print ('The mouse cursor is hovering over {}'.format(u._uid))
                    mouse_on_unit = u._uid

        cell_mouseover = get_cell_mouseover(grid)
        print(cell_mouseover)

        if moving == True:
            print ('now moving {}'.format(mouse_on_unit))
            units[mouse_on_unit]._x, units[mouse_on_unit]._y = pygame.mouse.get_pos()
            
        if drop == True:
            units[mouse_on_unit]._x, units[mouse_on_unit]._y = grid.cells[cell_mouseover].center
            drop = False

        ## flush
        pygame.display.flip()


if __name__=='__main__':
    main()


