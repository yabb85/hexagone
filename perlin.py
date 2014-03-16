#!/usr/bin/python
# -*-coding:Utf-8 -*


import random
import math
import Image


def generate_table(seed):
    """docstring for generate_table"""
    random.seed(seed)
    table = []
    value = random.randint(0, 255)
    while len(table) < 256:
        if value not in table:
            table.append(value)
        value = random.randint(0, 255)
    return table


def duplicate_table(table):
    """docstring for duplicate_table"""
    result = []
    for i in range(0, len(table) * 2):
        result[i] = table[i % 255]
    return result


def check_table(table):
    """docstring for check_table"""
    dictionary = {}
    for i in range(0, 256):
        dictionary[i] = 0

    for i in range(0, 256):
        if i in table:
            dictionary[i] += 1

    result = {}
    for key, value in dictionary.iteritems():
        if value is not 1:
            result[key] = value

    return result


def perlin(table, x, y, res):
    """docstring for perlin"""
    unit = 1.0 / math.sqrt(2.0)
    gradient2 = [[unit, unit], [-unit, unit], [unit, -unit], [-unit, -unit],
                [1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]

    x /= float(res)
    y /= float(res)

    x0 = int(x)
    y0 = int(y)

    ii = x0 % 255
    jj = y0 % 255

    grad1 = table[ii + table[jj]] % 8
    grad2 = table[ii + 1 + table[jj]] % 8
    grad3 = table[ii + table[jj + 1]] % 8
    grad4 = table[ii + 1 + table[jj + 1]] % 8

    tempX = x - x0
    tempY = y - y0
    s = gradient2[grad1][0] * tempX + gradient2[grad1][1] * tempY

    tempX = x - (x0 + 1.0)
    tempY = y - y0
    t = gradient2[grad2][0] * tempX + gradient2[grad2][1] * tempY

    tempX = x - x0
    tempY = y - (y0 + 1.0)
    u = gradient2[grad3][0] * tempX + gradient2[grad3][1] * tempY

    tempX = x - (x0 + 1.0)
    tempY = y - (y0 + 1.0)
    v = gradient2[grad4][0] * tempX + gradient2[grad4][1] * tempY

    # Lissage
    tmp = x - x0
    Cx = 3.0 * tmp * tmp - 2.0 * tmp * tmp * tmp

    Li1 = s + Cx * (t - s)
    Li2 = u + Cx * (v - u)

    tmp = y - y0
    Cy = 3.0 * tmp * tmp - 2.0 * tmp * tmp * tmp

    return Li1 + Cy * (Li2 - Li1)


table = generate_table(1)
dictionary = check_table(table)


width = 1000
height = 1000
img = Image.new('L', (width, height))
for i in range(0, width):
    for j in range(0, height):
        img.putpixel((i, j), (perlin(table, i, j, 100) + 1) * 0.5 * 255)
img.save('test.pgm', 'PPM')
