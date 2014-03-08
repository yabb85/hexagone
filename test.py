#!/usr/bin/python
# -*-coding:Utf-8 -*

import math
import sfml as sf

# On crée la fenêtre principale


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


def main():
    """docstring for main"""
    game_size = sf.Vector2(800, 600)
    w, h = game_size
    settings = sf.window.ContextSettings()
    settings.antialiasing_level = 8
    window = sf.RenderWindow(sf.VideoMode(w, h), "PySFML test")

    hexa = initialize_hexagone((100, 100), sf.Color.WHITE, 1, sf.Color.BLACK,
                               60, 30)
    initialize_board(hexa, window)

    # On démarre la boucle de jeu
    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.ESCAPE:
                window.close()
        window.display()

main()
