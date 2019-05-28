import pygame
import numpy as np

import enum
from kg_tools import get_cell_mouseover, get_unit_mouseover, \
                     get_button_mouseover 

class Status(enum.Enum):
    block = 0
    newgame = 1
    exit = 2
    credit = 3

    red_idle = 10
    red_moving_unit = 11
    red_dropping_unit = 12
    red_moving_x = 13
    red_dropping_x = 14

    blue_idle = 20
    blue_moving_unit = 21
    blue_dropping_unit = 22
    blue_moving_x = 23
    blue_dropping_x = 24


def func_block(*_):
    return Status.red_idle 


def func_red_idle(grid, units, buttons):
    unit_indicies = list(range(len(units)))
    cell_mouseover = get_cell_mouseover(grid)
    unit_mouseover = get_unit_mouseover(units)
    botton_mouseover = get_button_mouseover(buttons)

    if unit_mouseover in unit_indicies:
        if units[unit_mouseover].side == 0:
            return Status.red_moving_unit
        else:
            return Status.red_idle
    elif button_mouseover in [1,2,3]:
        return Status(button_mouseover)  
    else:
        return Status.red_idle


def func_red_moving_unit(grid, units, *_):
    unit_mouseover = get_unit_mouseover(units)
    
    return Status.red_dropping_unit


def func_red_moving_x(grid, units, *_):
    return Status.red_dropping_x


def func_blue_idle(grid, units, buttons):
    unit_indicies = list(range(len(units)))
    cell_mouseover = get_cell_mouseover(grid)
    unit_mouseover = get_unit_mouseover(units)
    botton_mouseover = get_button_mouseover(buttons)

    if unit_mouseover in unit_indicies:
        if units[unit_mouseover].side == 1:
            return Status.blue_moving_unit
        else:
            return Status.blue_idle
    elif button_mouseover in [1,2,3]:
        return Status(button_mouseover)  
    else:
        return status.blue_idle


def func_blue_moving_unit(grid, units, *_):
    unit_indicies = list(range(len(units)))
    unit_mouseover = get_unit_mouseover(units)
    
    return Status.blue_dropping_unit


def func_blue_moving_x(grid, units):
    return Status.blue_dropping_x


def default(*_):
    return 0

switcher = {
        Status.block: func_block,
        Status.red_idle: func_red_idle,
        Status.red_moving_unit: func_red_moving_unit,
        Status.red_moving_x: func_red_moving_x,
        Status.blue_idle: func_blue_idle,
        Status.blue_moving_unit: func_blue_moving_unit,
        Status.blue_moving_x: func_blue_moving_x,
    }

def mouse_click_event(status, grid, units, buttons):
    func = switcher.get(status, default)
    return func(grid, units, buttons)
        
        
