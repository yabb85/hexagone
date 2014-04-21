#!/usr/bin/python
# -*-coding:Utf-8 -*
"""
Draw an hexagon
"""

import math
import sfml as sf


class Hexagon(sf.TransformableDrawable):
    """
    Hexagoanl geometrical form
    """
    def __init__(self, position, radius, color, outline_color):
        """docstring for __init__"""
        sf.TransformableDrawable.__init__(self)
        self.vertices = sf.VertexArray(sf.PrimitiveType.TRIANGLES, 18)
        self.points = sf.VertexArray(sf.PrimitiveType.LINES_STRIP, 7)
        self.position = position
        self.radius = radius
        self.outline_color = outline_color
        self.origin = sf.Vector2(0, 0)
        self.color = color
        self.texture = None

        x = self.radius / 2
        y = self.radius * math.sqrt(3) / 2

        self.points[0].position = sf.Vector2(-x, y)
        self.points[0].color = outline_color
        self.points[1].position = sf.Vector2(x, y)
        self.points[1].color = outline_color
        self.points[2].position = sf.Vector2(self.radius, 0)
        self.points[2].color = outline_color
        self.points[3].position = sf.Vector2(x, -y)
        self.points[3].color = outline_color
        self.points[4].position = sf.Vector2(-x, -y)
        self.points[4].color = outline_color
        self.points[5].position = sf.Vector2(-self.radius, 0)
        self.points[5].color = outline_color
        self.points[6].position = sf.Vector2(-x, y)
        self.points[6].color = outline_color

        self.vertices[0].position = self.origin
        self.vertices[0].color = color
        self.vertices[1].position = self.points[0].position
        self.vertices[1].color = color
        self.vertices[2].position = self.points[1].position
        self.vertices[2].color = color
        self.vertices[3].position = self.origin
        self.vertices[3].color = color
        self.vertices[4].position = self.points[1].position
        self.vertices[4].color = color
        self.vertices[5].position = self.points[2].position
        self.vertices[5].color = color
        self.vertices[6].position = self.origin
        self.vertices[6].color = color
        self.vertices[7].position = self.points[2].position
        self.vertices[7].color = color
        self.vertices[8].position = self.points[3].position
        self.vertices[8].color = color
        self.vertices[9].position = self.origin
        self.vertices[9].color = color
        self.vertices[10].position = self.points[3].position
        self.vertices[10].color = color
        self.vertices[11].position = self.points[4].position
        self.vertices[11].color = color
        self.vertices[12].position = self.origin
        self.vertices[12].color = color
        self.vertices[13].position = self.points[4].position
        self.vertices[13].color = color
        self.vertices[14].position = self.points[5].position
        self.vertices[14].color = color
        self.vertices[15].position = self.origin
        self.vertices[15].color = color
        self.vertices[16].position = self.points[5].position
        self.vertices[16].color = color
        self.vertices[17].position = self.points[0].position
        self.vertices[17].color = color

    def draw(self, target, states):
        """docstring for draw"""
        states.transform = self.transform
        states.texture = self.texture
        target.draw(self.vertices, states)
        target.draw(self.points, states)

    def set_color(self, color):
        """docstring for set_color"""
        self.vertices[0].color = color
        self.vertices[1].color = color
        self.vertices[2].color = color
        self.vertices[3].color = color
        self.vertices[4].color = color
        self.vertices[5].color = color
        self.vertices[6].color = color
        self.vertices[7].color = color
        self.vertices[8].color = color
        self.vertices[9].color = color
        self.vertices[10].color = color
        self.vertices[11].color = color
        self.vertices[12].color = color
        self.vertices[13].color = color
        self.vertices[14].color = color
        self.vertices[15].color = color
        self.vertices[16].color = color
        self.vertices[17].color = color

    def set_outline_color(self, color):
        """docstring for set_fill_color"""
        self.points[0].color = color
        self.points[1].color = color
        self.points[2].color = color
        self.points[3].color = color
        self.points[4].color = color
        self.points[5].color = color
        self.points[6].color = color

    def set_texture(self, texture):
        """docstring for set_texture"""

        self.texture = texture

        if texture is None:
            return

        size = texture.size

        x = self.radius / 2
        y = self.radius * math.sqrt(3) / 2
        rad = self.radius
        coef = float(size[0]) / (self.radius * 2)

        self.points[0].tex_coords = sf.Vector2(
            (rad - x) * coef, (rad + y) * coef)
        self.points[1].tex_coords = sf.Vector2(
            (rad + x) * coef, (rad + y) * coef)
        self.points[2].tex_coords = sf.Vector2(
            (rad * 2) * coef, rad * coef)
        self.points[3].tex_coords = sf.Vector2(
            (rad + x) * coef, (rad - y) * coef)
        self.points[4].tex_coords = sf.Vector2(
            (rad - x) * coef, (rad - y) * coef)
        self.points[5].tex_coords = sf.Vector2(0, rad * coef)
        self.points[6].tex_coords = sf.Vector2(rad * coef, rad * coef)

        self.vertices[0].tex_coords = self.points[6].tex_coords
        self.vertices[1].tex_coords = self.points[0].tex_coords
        self.vertices[2].tex_coords = self.points[1].tex_coords
        self.vertices[3].tex_coords = self.points[6].tex_coords
        self.vertices[4].tex_coords = self.points[1].tex_coords
        self.vertices[5].tex_coords = self.points[2].tex_coords
        self.vertices[6].tex_coords = self.points[6].tex_coords
        self.vertices[7].tex_coords = self.points[2].tex_coords
        self.vertices[8].tex_coords = self.points[3].tex_coords
        self.vertices[9].tex_coords = self.points[6].tex_coords
        self.vertices[10].tex_coords = self.points[3].tex_coords
        self.vertices[11].tex_coords = self.points[4].tex_coords
        self.vertices[12].tex_coords = self.points[6].tex_coords
        self.vertices[13].tex_coords = self.points[4].tex_coords
        self.vertices[14].tex_coords = self.points[5].tex_coords
        self.vertices[15].tex_coords = self.points[6].tex_coords
        self.vertices[16].tex_coords = self.points[5].tex_coords
        self.vertices[17].tex_coords = self.points[0].tex_coords

    def get_radius(self):
        """docstring for get_radius"""
        return self.radius

    def get_apothem(self):
        """docstring for get_apothem"""
        return self.radius * math.sqrt(3) / 2


def main():
    """docstring for main"""
    position = (70, 70)
    radius = 60
    color = sf.Color(127, 127, 127)
    thickness = 1
    outline_color = sf.Color.BLACK
    hexa = Hexagon(position, radius, color, thickness, outline_color)

    montagne = sf.Texture.from_file('data/montagne.jpg')
    eau = sf.Texture.from_file('data/eau.jpg')
    hexa.set_texture(montagne)

    w_size, h_size = sf.Vector2(800, 600)
    settings = sf.window.ContextSettings()
    settings.antialiasing_level = 8
    window = sf.RenderWindow(sf.VideoMode(w_size, h_size), "PySFML test",
                             sf.window.Style.DEFAULT, settings)

    while window.is_open:
        window.clear(sf.Color(50, 200, 50))
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            if type(event) is sf.ResizeEvent:
                window.view = sf.View(sf.Rectangle((0, 0), window.size))
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.ESCAPE:
                window.close()
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.A:
                hexa.set_color(sf.Color(250, 50, 250))
                hexa.set_outline_color(sf.Color(0, 0, 250))
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.B:
                hexa.set_color(sf.Color(250, 50, 250, 50))
                hexa.set_outline_color(sf.Color.BLACK)
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.C:
                hexa.set_texture(eau)
            if type(event) is sf.KeyEvent and event.pressed and \
               event.code is sf.Keyboard.D:
                hexa.set_texture(montagne)
        window.draw(hexa)
        window.display()


if __name__ == '__main__':
    main()
