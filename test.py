#!/usr/bin/python
# -*-coding:Utf-8 -*

import math
import sfml as sf

# On crée la fenêtre principale


class Node():
    def __init__(self, pos=(0, 0), color=sf.Color.WHITE):
        """docstring for __init__"""
        self.color = color
        self.position = pos


class Hexagone(sf.ConvexShape):
    def __init__(self):
        """docstring for __init__"""
        self.point_count = 6
        self.radius = 100
        x = self.radius * math.sqrt(3) / 2
        y = self.radius / 2
        self.set_point(0, sf.Vector2(x, y))
        x = 0
        y = self.radius
        self.set_point(1, sf.Vector2(x, y))
        x = -self.radius * math.sqrt(3) / 2
        y = self.radius / 2
        self.set_point(2, sf.Vector2(x, y))
        x = -self.radius * math.sqrt(3) / 2
        y = -self.radius / 2
        self.set_point(3, sf.Vector2(x, y))
        x = 0
        y = -self.radius
        self.set_point(4, sf.Vector2(x, y))
        x = self.radius * math.sqrt(3) / 2
        y = -self.radius / 2
        self.set_point(5, sf.Vector2(x, y))

    def set_radius(self, radius):
        """docstring for set_radius"""
        self.radius = radius
        x = self.radius * math.sqrt(3) / 2
        y = self.radius / 2
        self.set_point(0, sf.Vector2(x, y))
        x = 0
        y = self.radius
        self.set_point(1, sf.Vector2(x, y))
        x = -self.radius * math.sqrt(3) / 2
        y = self.radius / 2
        self.set_point(2, sf.Vector2(x, y))
        x = -self.radius * math.sqrt(3) / 2
        y = -self.radius / 2
        self.set_point(3, sf.Vector2(x, y))
        x = 0
        y = -self.radius
        self.set_point(4, sf.Vector2(x, y))
        x = self.radius * math.sqrt(3) / 2
        y = -self.radius / 2
        self.set_point(5, sf.Vector2(x, y))

    def get_radius(self):
        """docstring for get_radius"""
        return self.radius

    def get_apothem(self):
        """docstring for get_apothem"""
        return self.radius * math.sqrt(3) / 2


def initialize_hexagone(initial_pos, color, outline_thick, outline_color,
                        radius, rotate):
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


def display_graph(hexa, window, graph):
    """docstring for display_graph"""
    window.clear(sf.Color(50, 200, 50))
    for e in graph:
        y = 70 + e[1] * hexa.get_apothem() * 2 + -e[0] * hexa.get_apothem()
        x = 70 + e[0] * hexa.get_radius() * 1.5
        hexa.position = (x, y)
        window.draw(hexa)


test = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3), (3, 4), (3, 5),
        (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (5, 3), (5, 4), (5, 5), (5, 6),
        (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (7, 4), (7, 5), (7, 6), (7, 7)]


def main():
    """docstring for main"""
    game_size = sf.Vector2(800, 600)
    w, h = game_size
    settings = sf.window.ContextSettings()
    settings.antialiasing_level = 8
    window = sf.RenderWindow(sf.VideoMode(w, h), "PySFML test")

    hexa = initialize_hexagone((100, 100), sf.Color.WHITE, 1, sf.Color.BLACK,
                               60, 30)
    survol = initialize_hexagone((100, 100), sf.Color.CYAN, 1, sf.Color.BLACK,
                                 60, 30)
    survol_on = False

    # On démarre la boucle de jeu
    while window.is_open:
        display_graph(hexa, window, test)
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.ESCAPE:
                window.close()
            if type(event) is sf.window.MouseMoveEvent:
                pos = (-1, -1)
                old_dist = (-1, -1)
                element = (-1, -1)
                for i in range(8):
                    y = (70 + i * hexa.get_apothem() * 2 + -i *
                         hexa.get_apothem())
                    x = 70 + i * hexa.get_radius() * 1.5
                    dist = (math.fabs(event.position.x - x),
                            math.fabs(event.position.y - y))
                    if pos == (-1, -1) or dist < old_dist:
                        element = (i, i)
                        pos = (x, y)
                        old_dist = dist
                if event.position.y > pos[1]:
                    liste = range(element[0], 15)
                else:
                    liste = range(0, element[0])
                for i in liste:
                    y = (70 + i * hexa.get_apothem() * 2 + -element[0] *
                         hexa.get_apothem())
                    dist = (math.fabs(event.position.x - pos[0]),
                            math.fabs(event.position.y - y))
                    if dist < old_dist:
                        element = (element[0], i)
                        pos = (pos[0], y)
                        old_dist = dist
                survol.position = pos
                if element in test:
                    survol_on = True
                else:
                    survol_on = False
            if type(event) is sf.window.FocusEvent:
                survol_on = False

        if survol_on is True:
            window.draw(survol)
        window.display()

main()
