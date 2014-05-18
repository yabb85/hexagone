#!/usr/bin/python
# -*-coding:Utf-8 -*
"""
Unit present in game
"""


class Unit(object):
    """Abstract class for implementation of unit."""
    def __init__(self):
        """docstring for __init__"""
        self.name = ""
        self.move = 1
        self.texture = None
        self.selected = False
        self.position = (0, 0)
        self.neighbors = [
            [+1, +1], [+1, 0], [0, -1],
            [-1, -1], [-1, 0], [0, +1]
        ]

    def get_name(self):
        """docstring for get_name"""
        return self.name

    def get_selected(self):
        """docstring for get_selected"""
        return self.selected

    def set_selected(self, select):
        """docstring for set_selected"""
        self.selected = select

    def get_position(self):
        """docstring for get_position"""
        return self.position

    def set_position(self, pos):
        """docstring for set_position"""
        self.position = pos

    def get_move(self):
        """docstring for get_move"""
        return self.move

    def get_neighbors(self):
        """docstring for get_neighbors"""
        return self.neighbors


class Infantry(Unit):
    """Infantry unit"""
    def __init__(self):
        """docstring for __init__"""
        Unit.__init__(self)
        self.name = "Infantry"


class Cavalry(Unit):
    """Cavalry unit"""
    def __init__(self):
        """docstring for __init__"""
        Unit.__init__(self)
        self.name = "Cavalry"
        self.move = 1
