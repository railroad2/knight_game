import pygame 
#from kg_objects import Uid
import kg_objects as ko

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

    return ko.Uid.empty.value


def get_button_mouseover(buttons):
    point = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(point):
            return button.button_id

    return ko.Uid.empty.value



def coord2idx(i, j):
    return i*7 + j


def idx2coord(idx):
    return divmod(idx, 7)
