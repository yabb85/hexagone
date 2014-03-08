#!/usr/bin/python
# -*-coding:Utf-8 -*

import math
import sfml as sf

# On crée la fenêtre principale
game_size = sf.Vector2(800, 600)
w, h = game_size
settings = sf.window.ContextSettings()
settings.antialiasing_level = 8
window = sf.RenderWindow(sf.VideoMode(w, h), "PySFML test")


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


hexa = Hexagone()

hexa.position = (100, 100)
hexa.outline_thickness = 1
hexa.outline_color = sf.Color.BLACK
hexa.set_radius(60)
nb_col = game_size.x / (hexa.get_radius() * 2)
nb_row = game_size.y / (hexa.get_apothem() * 2)
hexa.rotate(30)


# On démarre la boucle de jeu
while window.is_open:
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()
        if type(event) is sf.KeyEvent and event.pressed and \
           event.code is sf.Keyboard.ESCAPE:
            window.close()

    hexa.position = (hexa.get_radius(), hexa.get_apothem())
    last_position = hexa.position
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

    window.display()
