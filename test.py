#!/usr/bin/python
# -*-coding:Utf-8 -*
"""
This is a test of wargame
"""

import math
import sfml as sf
from hexagon import Hexagon, HexagonLine
import time
from unit import Cavalry
import operator


MARGIN = 70
GRAY_127 = sf.Color(127, 127, 127)
EAU = sf.Color(150, 196, 217)
RED = sf.Color(232, 174, 173)
GREEN = sf.Color(188, 222, 186)
BORDER = sf.Color(127, 127, 127, 127)
OVERLOAD = sf.Color(127, 127, 127, 100)


class Ground(object):
    """Enumerator for ground type"""
    plain = 0
    forest = 1
    mountain = 2
    water = 3

    def get_plain(self):
        """docstring for get_plain"""
        return self.plain

    def get_forest(self):
        """docstring for get_forest"""
        return self.forest

    def get_mountain(self):
        """docstring for get_mountain"""
        return self.mountain

    def get_water(self):
        """docstring for get_water"""
        return self.water


class TextureManager(object):
    """Texture manager."""
    class InternTextureManager(object):
        """Intern singleton class for texture manager."""
        def __init__(self):
            """docstring for __init__"""
            self.ground_textures = {
                Ground.plain: None,
                Ground.forest: None,
                Ground.mountain: None,
                Ground.water: None
            }
            self.unit_textures = {
                "Infantry": None,
                "Cavalery": None
            }
            self.background = None
            self.load_all_texture()

        def load_all_texture(self):
            """load all texture used in game"""
            self.background = sf.Texture.from_file('data/bois.jpg')
            self.ground_textures[Ground.forest] = sf.Texture.from_file(
                'data/arbre.jpg')
            self.ground_textures[Ground.water] = sf.Texture.from_file(
                'data/eau.jpg')
            self.ground_textures[Ground.mountain] = sf.Texture.from_file(
                'data/montagne.jpg')
            self.ground_textures[Ground.plain] = sf.Texture.from_file(
                'data/paper.jpg')
            # self.unit_textures["Infantry"] = sf.Texture.from_file()
            self.unit_textures["Cavalry"] = sf.Texture.from_file(
                'data/cheval.png')

        def convert_ground_to_texture(self, ground):
            """Search the texture associate to ground type."""
            return self.ground_textures[ground]

        def convert_texture_to_ground(self, texture):
            """docstring for convert_texture_to_ground"""
            # TODO
            pass

        def get_unit_texture(self, unit):
            """Search the texture for each type of unit."""
            if unit is not None:
                return self.unit_textures[unit.get_name()]
            else:
                return None

        def get_background(self):
            """Return the texture of background"""
            return self.background

    __instance = None

    def __init__(self):
        """docstring for __init__"""
        if TextureManager.__instance is None:
            TextureManager.__instance = TextureManager.InternTextureManager()

    def __getattr__(self, name):
        """docstring for __getattr__"""
        return getattr(self.__instance, name)

    def __setattr__(self, name):
        """docstring for __setattr__"""
        return setattr(self.__instance, name)


class Node(object):
    """
    Représente une case sur le plateau
    """
    def __init__(self, pos=(0, 0), ground=Ground.plain, color=sf.Color.WHITE):
        """docstring for __init__"""
        self.color = color
        self.position = pos
        self.ground = ground

    def get_position(self):
        """docstring for get_position"""
        return self.position

    def get_color(self):
        """docstring for get_color"""
        return self.color

    def set_color(self, color):
        """docstring for set_color"""
        self.color = color

    def get_ground(self):
        """docstring for get_ground"""
        return self.ground

    def set_ground(self, ground):
        """docstring for set_ground"""
        self.ground = ground


def convert_pixel_to_coord(position):
    """docstring for convert_pixel_to_coord"""
    hexa = Hexagon((0, 0), 60, RED, BORDER)
    x_coord = (position[0] - MARGIN) / (hexa.get_radius() * 1.5)
    y_coord = (position[1] - MARGIN + x_coord + hexa.get_apothem()) / \
        (hexa.get_radius() * 2)
    return (x_coord, y_coord)


def convert_coord_to_pixel(coord):
    """docstring for convert_coord_to_pixel"""
    hexa = Hexagon((0, 0), 60, RED, BORDER)
    y_pos = MARGIN + coord[1] * hexa.get_apothem() * 2 - coord[0] * \
        hexa.get_apothem()
    x_pos = MARGIN + coord[0] * hexa.get_radius() * 1.5
    return (x_pos, y_pos)


def display_units(window, units):
    """
    Display all unit on the map
    :param window:window used to display
    :param units:list of all units
    """
    hexa = Hexagon((100, 100), 60, GRAY_127, BORDER)
    texture_mgr = TextureManager()
    for unit in units:
        hexa.set_texture(texture_mgr.get_unit_texture(unit))
        hexa.position = convert_coord_to_pixel(unit.get_position())
        window.draw(hexa)
        if unit.get_selected():
            hexa.set_texture(None)
            hexa.set_color(sf.Color(250, 50, 250, 50))
            window.draw(hexa)
            neighbors = unit.get_neighbors()
            for i in range(len(neighbors)):
                pos = unit.get_position()
                neighbor = (neighbors[i][0] + pos[0], neighbors[i][1] + pos[1])
                hexa.position = convert_coord_to_pixel(neighbor)
                hexa.set_color(sf.Color(0, 0, 250, 50))
                window.draw(hexa)


def display_grid(window, graph):
    """
    Display all elements contains in graph (grid on map)
    :param window:window used to display
    :param graph:list of all elements to displaying
    """
    hexa = HexagonLine((100, 100), 60, BORDER)
    for node in graph:
        pos = node.get_position()
        y_pos = MARGIN + pos[1] * hexa.get_apothem() * 2 - \
            pos[0] * hexa.get_apothem()
        x_pos = MARGIN + pos[0] * hexa.get_radius() * 1.5
        hexa.position = (x_pos, y_pos)
        hexa.set_color(node.get_color())
        window.draw(hexa)


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


MAP = [Node((0, 0)), Node((0, 1)), Node((0, 2)), Node((0, 3)), Node((0, 4)),
       Node((1, 1)), Node((1, 2)), Node((1, 3)), Node((1, 4)),
       Node((2, 1)), Node((2, 2)), Node((2, 3)), Node((2, 4)), Node((2, 5)),
       Node((3, 2)), Node((3, 3)), Node((3, 4)), Node((3, 5)),
       Node((4, 2)), Node((4, 3)), Node((4, 4)), Node((4, 5)), Node((4, 6)),
       Node((5, 3)), Node((5, 4)), Node((5, 5)), Node((5, 6)),
       Node((6, 3)), Node((6, 4)), Node((6, 5)), Node((6, 6)), Node((6, 7)),
       Node((7, 4)), Node((7, 5)), Node((7, 6)), Node((7, 7))]


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
        dist_x = math.fabs(event.position.x - x_i)
        if pos == (-1, -1) or dist_x < old_dist:
            coord = (i, i)
            pos = (x_i, y_i)
            old_dist = dist_x
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
        dist_y = math.fabs(event.position.y - y_pos)
        if old_dist == -1 or dist_y < old_dist:
            coord = (coord[0], i)
            pos = (pos[0], y_pos)
            old_dist = dist_y
    old_dist = -1
    # improve the position of element selected with their neighbors
    for neighbor in neighbors:
        act_coord = tuple(map(operator.add, coord, neighbor))
        y_pos = MARGIN + act_coord[1] * hexa.get_apothem() * 2 - \
            act_coord[0] * hexa.get_apothem()
        x_pos = MARGIN + act_coord[0] * hexa.get_radius() * 1.5
        dist = math.sqrt((event.position.x - x_pos)**2 +
                         (event.position.y - y_pos)**2)
        if old_dist == -1 or dist < old_dist:
            pos = (x_pos, y_pos)
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


def event_dispatcher(event, window, last_node, units, survol, survol_on):
    """docstring for event_dispatcher"""
    hexa = Hexagon((100, 100), 60, GRAY_127, BORDER)
    if type(event) is sf.CloseEvent:
        window.close()
    if type(event) is sf.ResizeEvent:
        window.view = sf.View(sf.Rectangle((0, 0), window.size))
    if type(event) is sf.KeyEvent:
        event_key_dispatcher(event, window, last_node, units)
    if type(event) is sf.window.MouseMoveEvent:
        pos, coord = search_node_in_map(event, hexa)
        survol.position = pos
        node = search_node_by_coord_in_list(MAP, coord)
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
                MAP, last_node.get_position()) is not None:
            unit = search_unit_by_coord_in_list(units,
                                                last_node.get_position())
            if unit is not None:
                unit.set_selected(not unit.get_selected())
    return survol_on, last_node


def main():
    """docstring for main"""
    width, height = sf.Vector2(800, 600)
    settings = sf.window.ContextSettings()
    settings.antialiasing_level = 8
    window = sf.RenderWindow(sf.VideoMode(width, height), "PySFML test",
                             sf.window.Style.DEFAULT, settings)

    survol_on = False
    last_node = None
    texture_mgr = TextureManager()
    survol = Hexagon((100, 100), 60, OVERLOAD, sf.Color.BLACK)
    sprite = sf.Sprite(texture_mgr.get_background())
    font = sf.Font.from_file('data/Ubuntu-L.ttf')
    text = sf.Text('test', font, 30)
    text.color = sf.Color.RED
    text.position = (30, 0)
    fpstimer = time.time()
    fpscounter = 0
    units = []

    # On démarre la boucle de jeu
    while window.is_open:
        window.clear(sf.Color(50, 200, 50))
        window.draw(sprite)
        display_grid(window, MAP)
        display_units(window, units)
        for event in window.events:
            survol_on, last_node = event_dispatcher(event, window, last_node,
                                                    units, survol, survol_on)
        if time.time() - fpstimer >= 1:
            text.string = str(fpscounter) + 'fps'
            fpstimer = time.time()
            fpscounter = 0
        if survol_on is True:
            window.draw(survol)
        window.draw(text)
        window.display()
        fpscounter += 1

main()
