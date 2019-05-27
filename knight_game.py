import numpy as np
import pygame

import kg_objects as ko 
from kg_objects import Board, Grid, Unit_s, Unit_k, Blocker_x, Uid, coord_init

def main():
    pygame.init()
    pygame.font.init()
    win_w = 800
    win_h = win_w * 3 // 4
    screen = pygame.display.set_mode([win_w, win_h])
    pygame.display.set_caption("Knight Game")


    g0 = Grid(win_w, win_h)
    b0 = Board(g0) 

    ## defining units
    units = []
    for name in Uid:
        val = name.value
        if (val < 0):
            pass
        elif (val < 4):
            units.append(Unit_s(g0, coord_init[val], 1, val))
        elif (val < 7):
            units.append(Unit_k(g0, coord_init[val], 1, val))
        elif (val < 11):
            units.append(Unit_s(g0, coord_init[val], 2, val))
        elif (val < 14):
            units.append(Unit_k(g0, coord_init[val], 2, val))

    # states
    done = False
    moving = False
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

        screen.fill(ko.cBGND)

        b0.draw(screen)
        g0.draw(screen)

        print (pygame.mouse.get_pos())
        for u in units:
            u.draw(screen)
            if moving == False:
                if u.get_rect().collidepoint(pygame.mouse.get_pos()):
                    print ('The mouse cursor is hovering over {}'.format(u._uid))
                    mouse_on_unit = u._uid

        if moving == True:
            print ('now moving {}'.format(mouse_on_unit))
            units[mouse_on_unit]._x, units[mouse_on_unit]._y = pygame.mouse.get_pos()


        ## flush
        pygame.display.flip()


if __name__=='__main__':
    main()


