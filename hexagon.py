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
        self.color = color
        self.texture = None

        for i in range(7):
            angle = 2 * math.pi / 6 * i
            x_i = self.origin[0] + self.radius * math.cos(angle)
            y_i = self.origin[1] + self.radius * math.sin(angle)
            self.points[i].position = sf.Vector2(x_i, y_i)
            self.points[i].color = outline_color

        shift = -1
        for i in range(18):
            if i % 3 == 0:
                self.vertices[i].position = self.origin
                shift += 2
            else:
                self.vertices[i].position = self.points[i - shift].position
            self.vertices[i].color = color

    def draw(self, target, states):
        """Draw the hexagon."""
        states.transform = self.transform
        states.texture = self.texture
        target.draw(self.vertices, states)
        target.draw(self.points, states)

    def set_color(self, color):
        """Apply a new color at hexagon."""
        for i in range(18):
            self.vertices[i].color = color

    def set_outline_color(self, color):
        """Apply a new outline color."""
        for i in range(7):
            self.points[i].color = color

    def set_texture(self, texture):
        """Apply a new texture at hexagon."""
        self.texture = texture
        if texture is None:
            return

        size = texture.size
        coef = float(size[0]) / (self.radius * 2)
        x_center = size[0] / 2
        y_center = size[1] / 2
        for i in range(6):
            angle = 2 * math.pi / 6 * i
            x_i = x_center + self.radius * math.cos(angle) * coef
            y_i = y_center + self.radius * math.sin(angle) * coef
            self.points[i].tex_coords = sf.Vector2(x_i, y_i)
        self.points[6].tex_coords = sf.Vector2(
            self.radius * coef, self.radius * coef)

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
    outline_color = sf.Color.BLACK
    hexa = Hexagon(position, radius, color, outline_color)

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
