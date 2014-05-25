#!/usr/bin/python
# -*-coding:Utf-8 -*
"""
Test of hexagon module
"""

import unittest
import sfml as sf
from hexagon import Hexagon
from hexagon import HexagonLine


class TestHexagonLine(unittest.TestCase):
    """
    Test HexagonLine class
    """
    def setUp(self):
        """intialize the environment for all tests"""
        self.hexagon = HexagonLine((0, 0), 60, sf.Color(127, 127, 127))

    def test_radius(self):
        """test the radius value of hexagon"""
        radius = self.hexagon.get_radius()
        self.assertEqual(radius, 60)

    def test_apothem(self):
        """test the apothem value of hexagon"""
        apothem = self.hexagon.get_apothem()
        self.assertAlmostEqual(apothem, 51.961524227)


class TestHexagon(unittest.TestCase):
    """
    Test Hexagon class
    """
    def setUp(self):
        """intialize the environment for all tests"""
        self.hexagon = Hexagon((0, 0), 50, sf.Color(127, 127, 127),
                               sf.Color(127, 127, 127))

    def test_radius(self):
        """test the radius value of hexagon"""
        radius = self.hexagon.get_radius()
        self.assertEqual(radius, 50)

    def test_apothem(self):
        """test the apothem value of hexagon"""
        apothem = self.hexagon.get_apothem()
        self.assertAlmostEqual(apothem, 43.301270189)


if __name__ == '__main__':
    unittest.main()
