#!/usr/bin/python
# -*-coding:Utf-8 -*
"""
This is a test of wargame
"""

import math
import sfml as sf
from hexagon import Hexagon
import time
from unit import Cavalry
import operator
from render import Renderer, Ground


MARGIN = 70
GRAY_127 = sf.Color(127, 127, 127)
BORDER = sf.Color(127, 127, 127, 127)
OVERLOAD = sf.Color(127, 127, 127, 100)
SIZE = 50


class Node(object):
    """
    Représente une case sur le plateau
    """
    def __init__(self, pos=(0, 0), ground=Ground.plain,
                 color=sf.Color.WHITE):
        """Constructor"""
        self.color = color
        self.position = pos
        self.ground = ground

    def get_position(self):
        """Return the position of node in graph."""
        return self.position

    def get_color(self):
        """Return the color of node."""
        return self.color

    def set_color(self, color):
        """Set a new color for this node."""
        self.color = color

    def get_ground(self):
        """Return a ground type for this node"""
        return self.ground

    def set_ground(self, ground):
        """Set a new ground type for this node"""
        self.ground = ground


def search_node_by_coord_in_list(list_node, coord):
    """
    Search if a node exist in list with the coordinate passed in arguments.
    """
    for node in list_node:
        if node.get_position() == coord:
            return node
    return None


def search_unit_by_coord_in_list(units, coord):
    """docstring for search_unit_by_coord_in_list"""
    for unit in units:
        if unit.get_position() == coord:
            return unit
    return None


def generate_grid(height, width):
    """docstring for generate_grid"""
    liste = []
    base = 0
    for i in range(width):
        for j in range(base, height):
            liste.append(Node((i, j)))
        if i != 0 and i % 2 == 1:
            height += 1
        else:
            base += 1
    return liste


def search_node_in_map(event, hexa):
    """docstring for searchNode"""
    neighbors = [
        (+1, +1), (+1, 0), (0, -1),
        (-1, -1), (-1, 0), (0, +1),
        (0, 0)
    ]
    pos = (-1, -1)
    old_dist = -1
    coord = (-1, -1)
    # search element in diagonal (search column)
    for i in range(9):
        y_i = MARGIN + i * hexa.get_apothem() * 2 - \
            i * hexa.get_apothem()
        x_i = MARGIN + i * hexa.get_radius() * 1.5
        dist = math.fabs(event.position.x - x_i)
        if pos == (-1, -1) or dist < old_dist:
            coord = (i, i)
            pos = (x_i, y_i)
            old_dist = dist
    # create a list of element on same column
    if event.position.y > pos[1]:
        liste = range(coord[0] - 1, 15)
    else:
        liste = range(0, coord[0] + 1)
    old_dist = -1
    # search the row
    for i in liste:
        y_pos = (MARGIN + i * hexa.get_apothem() * 2 - coord[0] *
                 hexa.get_apothem())
        dist = math.fabs(event.position.y - y_pos)
        if old_dist == -1 or dist < old_dist:
            coord = (coord[0], i)
            pos = (pos[0], y_pos)
            old_dist = dist
    old_dist = -1
    # improve the position of element selected with their neighbors
    for i in neighbors:
        act_coord = tuple(map(operator.add, coord, i))
        y_i = MARGIN + act_coord[1] * hexa.get_apothem() * 2 - \
            act_coord[0] * hexa.get_apothem()
        x_i = MARGIN + act_coord[0] * hexa.get_radius() * 1.5
        dist = math.sqrt((event.position.x - x_i)**2 +
                         (event.position.y - y_i)**2)
        if old_dist == -1 or dist < old_dist:
            pos = (x_i, y_i)
            final_coord = act_coord
            old_dist = dist
    coord = final_coord
    return pos, coord


def event_key_dispatcher(event, window, last_node, units):
    """docstring for event_key_dispatcher"""
    if event.pressed and event.code is sf.Keyboard.ESCAPE:
        window.close()
    if event.pressed and event.code is sf.Keyboard.C and last_node is not None:
        cavalry = Cavalry()
        cavalry.set_position(last_node.get_position())
        units.append(cavalry)
    if event.pressed and event.code is sf.Keyboard.A and last_node is not None:
        last_node.set_ground(Ground.water)
    if event.pressed and event.code is sf.Keyboard.Z and last_node is not None:
        last_node.set_ground(Ground.forest)
    if event.pressed and event.code is sf.Keyboard.E and last_node is not None:
        last_node.set_ground(Ground.mountain)
    if event.pressed and event.code is sf.Keyboard.R and last_node is not None:
        last_node.set_ground(Ground.plain)


def event_dispatcher(event, window, last_node, units, survol, survol_on, grid):
    """docstring for event_dispatcher"""
    hexa = Hexagon((100, 100), SIZE, GRAY_127, BORDER)
    if type(event) is sf.CloseEvent:
        window.close()
    if type(event) is sf.ResizeEvent:
        window.view = sf.View(sf.Rectangle((0, 0), window.size))
    if type(event) is sf.KeyEvent:
        event_key_dispatcher(event, window, last_node, units)
    if type(event) is sf.window.MouseMoveEvent:
        pos, coord = search_node_in_map(event, hexa)
        survol.position = pos
        node = search_node_by_coord_in_list(grid, coord)
        if node is not None:
            last_node = node
            survol_on = True
        else:
            last_node = None
            survol_on = False
    if type(event) is sf.window.FocusEvent:
        survol_on = False
    if type(event) is sf.window.MouseButtonEvent and event.pressed:
        if last_node is not None and \
            search_node_by_coord_in_list(
                grid, last_node.get_position()) is not None:
            unit = search_unit_by_coord_in_list(units,
                                                last_node.get_position())
            if unit is not None:
                unit.set_selected(not unit.get_selected())
    return survol_on, last_node


def main():
    """fonction principale du soft"""
    width, height = sf.Vector2(800, 600)
    settings = sf.window.ContextSettings()
    settings.antialiasing_level = 8
    window = sf.RenderWindow(sf.VideoMode(width, height), "PySFML test",
                             sf.window.Style.DEFAULT, settings)
    # window.framerate_limit = 60

    grid = generate_grid(6, 10)
    survol_on = False
    last_node = None
    survol = Hexagon((100, 100), SIZE, OVERLOAD, sf.Color.BLACK)
    fpstimer = time.time()
    fpscounter = 0
    units = []
    text = ''
    render = Renderer(window, SIZE)

    # On démarre la boucle de jeu
    while window.is_open:
        render.display_background()
        render.display_grid(grid)
        render.display_units(units, GRAY_127)
        for event in window.events:
            survol_on, last_node = event_dispatcher(event, window, last_node,
                                                    units, survol, survol_on,
                                                    grid)
        if time.time() - fpstimer >= 1:
            fpstimer = time.time()
            text = str(fpscounter) + 'fps'
            fpscounter = 0
        if survol_on is True:
            window.draw(survol)
        render.display_fps(text)
        window.display()
        fpscounter += 1

if __name__ == '__main__':
    main()
