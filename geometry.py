#!/usr/bin/python
# -*-coding:Utf-8 -*
"""
This is a package with all geometrical object
"""

import math


class Hexagon(object):
    """
    Hexagonal geometrical form
    """
    def __init__(self, position, radius):
        """Initialise the hexagon object with good values"""
        self.radius = radius
        self.position = position

    def get_radius(self):
        """Return the radius value of hexagon"""
        return self.radius

    def get_apothem(self):
        """return the apothem value of hexagon"""
        return self.radius * math.sqrt(3) / 2
