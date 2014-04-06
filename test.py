#!/usr/bin/python
# -*-coding:Utf-8 -*

import math
import sfml as sf
from hexagon import Hexagon
import time


MARGIN = 70
GRAY_127 = sf.Color(127, 127, 127)
EAU = sf.Color(150, 196, 217)
RED = sf.Color(232, 174, 173)
GREEN = sf.Color(188, 222, 186)
BORDER = sf.Color(127, 127, 127, 127)
OVERLOAD = sf.Color(127, 127, 127, 100)


class Ground:
    plain = 0
    forest = 1
    mountain = 2
    water = 3


class TextureManager:
    class __TextureManager:
        def __init__(self):
            """docstring for __init__"""
            self.textures = {
                Ground.plain: None,
                Ground.forest: None,
                Ground.mountain: None,
                Ground.water: None
            }
            self.background = None
            self.load_all_texture()

        def load_all_texture(self):
            """load all texture used in game"""
            self.background = sf.Texture.from_file('data/bois.jpg')
            self.textures[Ground.forest] = sf.Texture.from_file(
                'data/arbre.jpg')
            self.textures[Ground.water] = sf.Texture.from_file('data/eau.jpg')
            self.textures[Ground.mountain] = sf.Texture.from_file(
                'data/montagne.jpg')
            self.textures[Ground.plain] = sf.Texture.from_file(
                'data/paper.jpg')

        def convertGroundToTexture(self, ground):
            """serach the texture associate to ground type"""
            return self.textures[ground]

        def convertTextureToGround(self, texture):
            """docstring for convertTextureToGround"""
            pass

        def get_background(self):
            """docstring for get_background"""
            return self.background

    __instance = None

    def __init__(self):
        """docstring for __init__"""
        if TextureManager.__instance is None:
            TextureManager.__instance = TextureManager.__TextureManager()

    def __getattr__(self, name):
        """docstring for __getattr__"""
        return getattr(self.__instance, name)

    def __setattr__(self, name):
        """docstring for __setattr__"""
        return setattr(self.__instance, name)


class Node():
    """
    Représente un case sur le plateau
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
        y = MARGIN + pos[1] * hexa.get_apothem() * 2 - \
            pos[0] * hexa.get_apothem()
        x = MARGIN + pos[0] * hexa.get_radius() * 1.5
        hexa.position = (x, y)
        hexa.set_color(node.get_color())
        hexa.set_texture(texture_mgr.convertGroundToTexture(node.get_ground()))
        window.draw(hexa)


def searchNodeByCoordInList(list_node, coord):
    """
    Search if a nade exist in list with the coordinate passed in arguments.
    """
    for node in list_node:
        if node.get_position() == coord:
            return node
    return None


test = [Node((0, 0)), Node((0, 1)), Node((0, 2)), Node((0, 3)), Node((0, 4)),
        Node((1, 1)), Node((1, 2)), Node((1, 3)), Node((1, 4)),
        Node((2, 1)), Node((2, 2)), Node((2, 3)), Node((2, 4)), Node((2, 5)),
        Node((3, 2)), Node((3, 3)), Node((3, 4)), Node((3, 5)),
        Node((4, 2)), Node((4, 3)), Node((4, 4)), Node((4, 5)), Node((4, 6)),
        Node((5, 3)), Node((5, 4)), Node((5, 5)), Node((5, 6)),
        Node((6, 3)), Node((6, 4)), Node((6, 5)), Node((6, 6)), Node((6, 7)),
        Node((7, 4)), Node((7, 5)), Node((7, 6)), Node((7, 7))]


def searchNodeInMap(event, hexa):
    """docstring for searchNode"""
    pos = (-1, -1)
    old_dist = (-1, -1)
    coord = (-1, -1)
    """search element in diagonal"""
    for i in range(9):
        y = MARGIN + i * hexa.get_apothem() * 2 - \
            i * hexa.get_apothem()
        x = MARGIN + i * hexa.get_radius() * 1.5
        dist = (math.fabs(event.position.x - x),
                math.fabs(event.position.y - y))
        if pos == (-1, -1) or dist < old_dist:
            coord = (i, i)
            pos = (x, y)
            old_dist = dist
    if event.position.y > pos[1]:
        liste = range(coord[0], 15)
    else:
        liste = range(0, coord[0])
    for i in liste:
        y = (MARGIN + i * hexa.get_apothem() * 2 - coord[0] *
             hexa.get_apothem())
        dist = (math.fabs(event.position.x - pos[0]),
                math.fabs(event.position.y - y))
        if dist < old_dist:
            coord = (coord[0], i)
            pos = (pos[0], y)
            old_dist = dist
    return pos, coord


def main():
    """docstring for main"""
    game_size = sf.Vector2(800, 600)
    w, h = game_size
    settings = sf.window.ContextSettings()
    settings.antialiasing_level = 8
    window = sf.RenderWindow(sf.VideoMode(w, h), "PySFML test",
                             sf.window.Style.DEFAULT, settings)

    hexa = Hexagon((100, 100), 60, GRAY_127, 1, BORDER)
    survol = Hexagon((100, 100), 60, OVERLOAD, 1, sf.Color.BLACK)
    survol_on = False
    last_node = None
    texture_mgr = TextureManager()
    hexa.set_texture(texture_mgr.convertGroundToTexture(Ground.forest))
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
        display_graph(hexa, window, test)
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            if type(event) is sf.ResizeEvent:
                window.view = sf.View(sf.Rectangle((0, 0), window.size))
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.ESCAPE:
                window.close()
            if type(event) is sf.window.MouseMoveEvent:
                pos, coord = searchNodeInMap(event, hexa)
                survol.position = pos
                node = searchNodeByCoordInList(test, coord)
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
                   searchNodeByCoordInList(test, last_node.get_position()) \
                   is not None:
                    if last_node.get_color() == sf.Color.WHITE:
                        last_node.set_color(EAU)
                        last_node.set_ground(Ground.water)
                    elif last_node.get_color() == EAU:
                        last_node.set_color(RED)
                        last_node.set_ground(Ground.mountain)
                    elif last_node.get_color() == RED:
                        last_node.set_color(GREEN)
                        last_node.set_ground(Ground.forest)
                    else:
                        last_node.set_color(sf.Color.WHITE)
                        last_node.set_ground(Ground.plain)

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
