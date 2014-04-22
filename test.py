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
        self.unit = None

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

    def get_unit(self):
        """docstring for get_unit"""
        return self.unit

    def set_unit(self, unit):
        """docstring for set_unit"""
        self.unit = unit


def display_unit(hexa, window, graph, unit):
    """docstring for display_unit"""
    texture_mgr = TextureManager()
    hexa.set_texture(texture_mgr.get_unit_texture(unit))
    window.draw(hexa)
    if unit.get_selected():
        hexa.set_texture(None)
        hexa.set_color(sf.Color(250, 50, 250, 50))
        window.draw(hexa)


def display_graph(hexa, window, graph):
    """
    Display all elements contains in graph
    :param hexa:the geometrical form used to display
    :param window:window used to display
    :param graph:list of all elements to displaying
    """
    texture_mgr = TextureManager()
    for node in graph:
        pos = node.get_position()
        y_pos = MARGIN + pos[1] * hexa.get_apothem() * 2 - \
            pos[0] * hexa.get_apothem()
        x_pos = MARGIN + pos[0] * hexa.get_radius() * 1.5
        hexa.position = (x_pos, y_pos)
        hexa.set_color(node.get_color())
        hexa.set_texture(texture_mgr.convert_ground_to_texture(
            node.get_ground()))
        window.draw(hexa)
        if node.get_unit() is not None:
            display_unit(hexa, window, graph, node.get_unit())


def search_node_by_coord_in_list(list_node, coord):
    """
    Search if a nade exist in list with the coordinate passed in arguments.
    """
    for node in list_node:
        if node.get_position() == coord:
            return node
    return None


TEST = [Node((0, 0)), Node((0, 1)), Node((0, 2)), Node((0, 3)), Node((0, 4)),
        Node((1, 1)), Node((1, 2)), Node((1, 3)), Node((1, 4)),
        Node((2, 1)), Node((2, 2)), Node((2, 3)), Node((2, 4)), Node((2, 5)),
        Node((3, 2)), Node((3, 3)), Node((3, 4)), Node((3, 5)),
        Node((4, 2)), Node((4, 3)), Node((4, 4)), Node((4, 5)), Node((4, 6)),
        Node((5, 3)), Node((5, 4)), Node((5, 5)), Node((5, 6)),
        Node((6, 3)), Node((6, 4)), Node((6, 5)), Node((6, 6)), Node((6, 7)),
        Node((7, 4)), Node((7, 5)), Node((7, 6)), Node((7, 7))]


def search_node_in_map(event, hexa):
    """docstring for searchNode"""
    pos = (-1, -1)
    old_dist = (-1, -1)
    coord = (-1, -1)
    # search element in diagonal
    for i in range(9):
        y_i = MARGIN + i * hexa.get_apothem() * 2 - \
            i * hexa.get_apothem()
        x_i = MARGIN + i * hexa.get_radius() * 1.5
        dist = (math.fabs(event.position.x - x_i),
                math.fabs(event.position.y - y_i))
        if pos == (-1, -1) or dist < old_dist:
            coord = (i, i)
            pos = (x_i, y_i)
            old_dist = dist
    if event.position.y > pos[1]:
        liste = range(coord[0], 15)
    else:
        liste = range(0, coord[0])
    for i in liste:
        y_pos = (MARGIN + i * hexa.get_apothem() * 2 - coord[0] *
                 hexa.get_apothem())
        dist = (math.fabs(event.position.x - pos[0]),
                math.fabs(event.position.y - y_pos))
        if dist < old_dist:
            coord = (coord[0], i)
            pos = (pos[0], y_pos)
            old_dist = dist
    return pos, coord


def main():
    """docstring for main"""
    width, height = sf.Vector2(800, 600)
    settings = sf.window.ContextSettings()
    settings.antialiasing_level = 8
    window = sf.RenderWindow(sf.VideoMode(width, height), "PySFML test",
                             sf.window.Style.DEFAULT, settings)

    hexa = Hexagon((100, 100), 60, GRAY_127, BORDER)
    survol = Hexagon((100, 100), 60, OVERLOAD, sf.Color.BLACK)
    survol_on = False
    last_node = None
    texture_mgr = TextureManager()
    hexa.set_texture(texture_mgr.convert_ground_to_texture(Ground.forest))
    sprite = sf.Sprite(texture_mgr.get_background())
    font = sf.Font.from_file('data/Ubuntu-L.ttf')
    text = sf.Text('test', font, 30)
    text.color = sf.Color.RED
    text.position = (30, 0)
    fpstimer = time.time()
    fpscounter = 0

    # On démarre la boucle de jeu
    while window.is_open:
        window.clear(sf.Color(50, 200, 50))
        window.draw(sprite)
        display_graph(hexa, window, TEST)
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            if type(event) is sf.ResizeEvent:
                window.view = sf.View(sf.Rectangle((0, 0), window.size))
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.ESCAPE:
                window.close()
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.C and last_node is not None:
                cavalry = Cavalry()
                cavalry.set_position(last_node.get_position())
                last_node.set_unit(cavalry)
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.A and last_node is not None:
                last_node.set_ground(Ground.water)
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.Z and last_node is not None:
                last_node.set_ground(Ground.forest)
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.E and last_node is not None:
                last_node.set_ground(Ground.mountain)
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.R and last_node is not None:
                last_node.set_ground(Ground.plain)
            if type(event) is sf.window.MouseMoveEvent:
                pos, coord = search_node_in_map(event, hexa)
                survol.position = pos
                node = search_node_by_coord_in_list(TEST, coord)
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
                       TEST, last_node.get_position()) is not None:
                    if last_node.get_unit() is not None:
                        select = last_node.get_unit().get_selected()
                        last_node.get_unit().set_selected(not select)
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
