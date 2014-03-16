#!/usr/bin/python
# -*-coding:Utf-8 -*

import math
import sfml as sf


MARGIN = 70
GRAY_127 = sf.Color(127, 127, 127)
EAU = sf.Color(150, 196, 217)
RED = sf.Color(232, 174, 173)
GREEN = sf.Color(188, 222, 186)
BORDER = sf.Color(127, 127, 127, 127)
OVERLOAD = sf.Color(127, 127, 127, 100)

T_BOIS = None
T_EAU = None
T_MONTAGNE = None
T_ARBRE = None
T_VIDE = None


class Ground:
    plain = 0
    forest = 1
    mountain = 2
    water = 3


class TextureManager:
    def laod_all_texture(self):
        """docstring for laod_all_texture"""
        pass

    def convertGroundToTexture(self, ground):
        """docstring for convertGroundToTexture"""
        pass

    def convertTextureToGround(self, texture):
        """docstring for convertTextureToGround"""
        pass


class Node():
    def __init__(self, pos=(0, 0), ground=Ground.plain, color=sf.Color.WHITE):
        """docstring for __init__"""
        self.color = color
        self.position = pos
        self.texture = sf.Texture.from_file('data/paper.jpg')
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

    def set_texture(self, texture):
        """docstring for set_texture"""
        self.texture = texture


class Hexagone(sf.ConvexShape):
    def __init__(self):
        """docstring for __init__"""
        self.point_count = 6
        self.radius = 100
        x = -self.radius / 2
        y = self.radius * math.sqrt(3) / 2
        self.set_point(0, sf.Vector2(x, y))
        x = self.radius / 2
        y = self.radius * math.sqrt(3) / 2
        self.set_point(1, sf.Vector2(x, y))
        x = self.radius
        y = 0
        self.set_point(2, sf.Vector2(x, y))
        x = self.radius / 2
        y = -self.radius * math.sqrt(3) / 2
        self.set_point(3, sf.Vector2(x, y))
        x = -self.radius / 2
        y = -self.radius * math.sqrt(3) / 2
        self.set_point(4, sf.Vector2(x, y))
        x = -self.radius
        y = 0
        self.set_point(5, sf.Vector2(x, y))

    def set_radius(self, radius):
        """docstring for set_radius"""
        self.radius = radius
        x = -self.radius / 2
        y = self.radius * math.sqrt(3) / 2
        self.set_point(0, sf.Vector2(x, y))
        x = self.radius / 2
        y = self.radius * math.sqrt(3) / 2
        self.set_point(1, sf.Vector2(x, y))
        x = self.radius
        y = 0
        self.set_point(2, sf.Vector2(x, y))
        x = self.radius / 2
        y = -self.radius * math.sqrt(3) / 2
        self.set_point(3, sf.Vector2(x, y))
        x = -self.radius / 2
        y = -self.radius * math.sqrt(3) / 2
        self.set_point(4, sf.Vector2(x, y))
        x = -self.radius
        y = 0
        self.set_point(5, sf.Vector2(x, y))

    def get_radius(self):
        """docstring for get_radius"""
        return self.radius

    def get_apothem(self):
        """docstring for get_apothem"""
        return self.radius * math.sqrt(3) / 2

    def set_texture(self, texture):
        """docstring for set_texture"""
        self.texture = texture


def initialize_hexagone(initial_pos, color, outline_thick, outline_color,
                        radius, rotate=0):
    """docstring for initialize_hexagone"""
    hexa = Hexagone()
    hexa.fill_color = color
    hexa.position = initial_pos
    hexa.outline_thickness = outline_thick
    hexa.outline_color = outline_color
    hexa.set_radius(radius)
    hexa.rotate(rotate)
    return hexa


def initialize_board(hexa, window):
    hexa.position = (hexa.get_radius(), hexa.get_apothem())
    window.clear(sf.Color(50, 200, 50))
    for j in range(0, 5):
        for i in range(0, 8):
            window.draw(hexa)
            radius = hexa.get_radius()
            if i % 2 == 0:
                hexa.move((radius * 1.5, hexa.get_apothem()))
            else:
                hexa.move((radius * 1.5, -hexa.get_apothem()))
        hexa.position = (hexa.get_radius(),
                         hexa.position.y + 2 * hexa.get_apothem())


def load_texture():
    """docstring for load_texture"""
    global T_ARBRE
    global T_BOIS
    global T_EAU
    global T_MONTAGNE
    global T_VIDE
    T_ARBRE = sf.Texture.from_file('data/arbre.jpg')
    T_BOIS = sf.Texture.from_file('data/bois.jpg')
    T_EAU = sf.Texture.from_file('data/eau.jpg')
    T_MONTAGNE = sf.Texture.from_file('data/montagne.jpg')
    T_VIDE = sf.Texture.from_file('data/paper.jpg')


def display_graph(hexa, window, graph):
    """docstring for display_graph"""
    for node in graph:
        pos = node.get_position()
        y = MARGIN + pos[1] * hexa.get_apothem() * 2 - \
            pos[0] * hexa.get_apothem()
        x = MARGIN + pos[0] * hexa.get_radius() * 1.5
        hexa.position = (x, y)
        hexa.fill_color = node.get_color()
        hexa.set_texture(node.texture)
        window.draw(hexa)


def searchNodeByCoordInList(list_node, coord):
    """docstring for searchNodeByCoordInList"""
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
    pass
    pos = (-1, -1)
    old_dist = (-1, -1)
    coord = (-1, -1)
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
    global T_BOIS
    global T_ARBRE
    global T_EAU
    global T_MONTAGNE
    global T_VIDE
    game_size = sf.Vector2(800, 600)
    w, h = game_size
    settings = sf.window.ContextSettings()
    settings.antialiasing_level = 8
    window = sf.RenderWindow(sf.VideoMode(w, h), "PySFML test",
                             sf.window.Style.DEFAULT, settings)

    hexa = initialize_hexagone((100, 100), GRAY_127, 1, BORDER, 60)
    survol = sf.CircleShape(60, 6)
    survol
    #survol = initialize_hexagone((100, 100), OVERLOAD, 1, sf.Color.BLACK,
                                #60)
    survol_on = False
    last_node = None
    load_texture()
    hexa.set_texture(T_VIDE)
    survol.rotate(30)
    survol.texture = T_ARBRE
    survol.outline_thickness = 1
    survol.outline_color = sf.Color.BLACK
    sprite = sf.Sprite(T_BOIS)

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
                        last_node.set_texture(T_EAU)
                    elif last_node.get_color() == EAU:
                        last_node.set_color(RED)
                        last_node.set_texture(T_MONTAGNE)
                    elif last_node.get_color() == RED:
                        last_node.set_color(GREEN)
                        last_node.set_texture(T_ARBRE)
                    else:
                        last_node.set_texture(T_VIDE)
                        last_node.set_color(sf.Color.WHITE)

        if survol_on is True:
            window.draw(survol)
        window.display()

main()
