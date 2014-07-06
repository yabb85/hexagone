#!/usr/bin/python
# -*-coding:Utf-8 -*
"""
Renderer module
"""

import sfml as sf
from hexagon import HexagonLine, Hexagon


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
        # self.background = sf.Texture.from_file('data/bois.jpg')
        self.background = sf.Texture.from_file('final.png')
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
        """Search ground type associate to texture."""
        for key, value in self.ground_textures:
            if value == texture:
                return key
        return None

    def get_unit_texture(self, unit):
        """Search the texture for each type of unit."""
        if unit is not None:
            return self.unit_textures[unit.get_name()]
        else:
            return None

    def get_background(self):
        """Return the texture of background"""
        return self.background


class Renderer(object):
    """
    rendering of game
    """
    def __init__(self, window, size):
        """docstring for __init__"""
        self.size = size
        self.grid_color = sf.Color(127, 127, 127)
        self.overload_color = sf.Color(127, 127, 127, 100)
        self.margin = 70
        self.window = window
        self.hexa_grid = HexagonLine((100, 100), self.size, self.grid_color)
        self.font = sf.Font.from_file('data/Ubuntu-L.ttf')
        self.text = sf.Text('test', self.font, 30)
        self.text.color = sf.Color.RED
        self.text.position = (30, 0)
        self.texture_mgr = TextureManager()
        self.sprite = sf.Sprite(self.texture_mgr.get_background())

    def display_grid(self, graph):
        """
        Display all elements contains in graph (grid on map)
        :param graph:list of all elements to displaying
        """
        for node in graph:
            pos = node.get_position()
            y_pos = self.margin + pos[1] * self.hexa_grid.get_apothem() * 2 - \
                pos[0] * self.hexa_grid.get_apothem()
            x_pos = self.margin + pos[0] * self.hexa_grid.get_radius() * 1.5
            self.hexa_grid.position = (x_pos, y_pos)
            self.hexa_grid.set_color(node.get_color())
            self.window.draw(self.hexa_grid)

    def display_units(self, units, color):
        """
        Display all unit on the map
        :param units:list of all units
        :param color:color of unit
        """
        hexa = Hexagon((100, 100), self.size, color, self.grid_color)
        for unit in units:
            hexa.set_texture(self.texture_mgr.get_unit_texture(unit))
            hexa.position = convert_coord_to_pixel(unit.get_position(),
                                                   self.size,
                                                   color,
                                                   self.grid_color,
                                                   self.margin)
            self.window.draw(hexa)
            if unit.get_selected():
                hexa.set_texture(None)
                hexa.set_color(sf.Color(250, 50, 250, 50))
                self.window.draw(hexa)
                neighbors = unit.get_neighbors()
                for i in range(len(neighbors)):
                    pos = unit.get_position()
                    neighbor = (neighbors[i][0] + pos[0],
                                neighbors[i][1] + pos[1])
                    hexa.position = convert_coord_to_pixel(neighbor,
                                                           self.size,
                                                           color,
                                                           self.grid_color,
                                                           self.margin)
                    hexa.set_color(sf.Color(0, 0, 250, 50))
                    self.window.draw(hexa)

    def display_fps(self, fps):
        """display a number of fps in corner of screen"""
        self.text.string = fps
        self.window.draw(self.text)

    def display_background(self):
        """display the background of game"""
        self.window.clear(sf.Color(0, 0, 0))
        self.window.draw(self.sprite)


def convert_coord_to_pixel(coord, size, color, border, margin):
    """Convert a coordinate in grid to coordinate on screen"""
    hexa = Hexagon((0, 0), size, color, border)
    y_pos = margin + coord[1] * hexa.get_apothem() * 2 - coord[0] * \
        hexa.get_apothem()
    x_pos = margin + coord[0] * hexa.get_radius() * 1.5
    return (x_pos, y_pos)


def convert_pixel_to_coord(position, size, color, border, margin):
    """convert a coordinate on screen to coordinate in grid"""
    hexa = Hexagon((0, 0), size, color, border)
    x_coord = (position[0] - margin) / (hexa.get_radius() * 1.5)
    y_coord = (position[1] - margin + x_coord + hexa.get_apothem()) / \
        (hexa.get_radius() * 2)
    return (x_coord, y_coord)
