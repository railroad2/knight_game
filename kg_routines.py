import pygame 
from kg_objects import Uid

def get_cell_mouseover(grid):
    cells = grid.cell_rects
    point = pygame.mouse.get_pos()
    for i, cell in enumerate(cells):
        if cell.collidepoint(point):
            return i 

    return Uid.empty.value

def get_unit_mouseover(units):
    point = pygame.mouse.get_pos()
    for unit in units:
        if unit.rect.collidepoint(point):
            return unit.uid

    return Uid.empty.value

def mouse_down():
    pass

