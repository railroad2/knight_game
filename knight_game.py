import numpy as np
import pygame

from kg_objects import Board, Grid, Unit_s, Unit_k, Blocker_x, Uid, coord_init, Team
from kg_tools import get_cell_mouseover, get_unit_mouseover, coord2idx, idx2coord

from kg_main import Knight_game
from kg_draw import Draw_ui

def doit():
    pygame.init()
    pygame.font.init()
    win_w = 800
    win_h = win_w * 3 // 4
    screen = pygame.display.set_mode([win_w, win_h])
    clock_tick = 100

    kg = Knight_game(screen, clock_tick)
    kg.initialize()
    kg.main_loop()

    print ("Bye bye :)")

def old_doit():
    pygame.init()
    pygame.font.init()
    win_w = 800
    win_h = win_w * 3 // 4
    screen = pygame.display.set_mode([win_w, win_h])
    pygame.display.set_caption("Knight Game")

    grid = Grid(win_w, win_h)
    board = Board(grid) 

    ## defining units
    red = Team(grid, 0)
    blue = Team(grid, 1)
    
    units = []
    units = [u for u in red.units] + [u for u in blue.units]
    unit_indicies = list(range(len(units)))
    
    # states
    flag_done = False
    flag_moving = False
    flag_drop = False
    clock = pygame.time.Clock()

    cell_mouseover = -1
    mouse_on_unit = -1

    ## main loop
    while not flag_done:
        clock.tick(1000)

        # event loop
        for event in pygame.event.get():
            # quit 
            if event.type == pygame.QUIT:
                flag_done = True
            # mouse button down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if flag_moving == False: 
                    if mouse_on_unit in unit_indicies: 
                        flag_moving = True
                elif flag_moving == True:
                    if mouse_on_unit in unit_indicies: 
                        flag_drop = True

        # draw
        screen.fill(ko.cBGND)
        board.draw(screen)
        grid.draw(screen)
        red.draw_units(screen)
        blue.draw_units(screen)

        #state machine
        if flag_moving == False:
            cell_mouseover = get_cell_mouseover(grid)
            mouse_on_unit = get_unit_mouseover(units)
            #print ('cell_mouseover is {}, mouse_on_unit {}'.format(cell_mouseover, mouse_on_unit))

        if flag_moving == True:
            #print ('now moving {}'.format(mouse_on_unit))
            cell_mouseover = get_cell_mouseover(grid)
            if mouse_on_unit in unit_indicies: 
                units[mouse_on_unit].set_movable_cells()
                units[mouse_on_unit].draw(screen)
                units[mouse_on_unit].draw_movable_cells(screen)
                units[mouse_on_unit]._x, units[mouse_on_unit]._y = pygame.mouse.get_pos()
            
        if flag_drop == True:
            if mouse_on_unit in unit_indicies: 
                units[mouse_on_unit].move(cell_mouseover)
            mouse_on_unit = Uid.empty.value
            flag_moving = False
            flag_drop = False

        #print (grid.stat.reshape(8,7))

        ## flush
        #print (clock.tick())
        pygame.display.flip()

    print ("Bye bye :)")


if __name__=='__main__':
    doit()


