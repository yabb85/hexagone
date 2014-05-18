#!/usr/bin/python
# -*-coding:Utf-8 -*


import random
import math
import Image


def generate_table(seed):
    """Generate a new perlin table with random value"""
    random.seed(seed)
    table = []
    value = random.randint(0, 255)
    while len(table) < 256:
        if value not in table:
            table.append(value)
        value = random.randint(0, 255)
    return table


def duplicate_table(table):
    """Duplicate a perlin table."""
    result = []
    for i in range(0, len(table) * 2):
        result[i] = table[i % 255]
    return result


def check_table(table):
    """
    Return a vlau with error in perlin table
    Value with error is a value not present in table or
    a value present everal times
    """
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

    index1 = (ii + table[jj]) % 256
    index2 = (ii + 1 + table[jj]) % 256
    index3 = (ii + table[jj + 1]) % 256
    index4 = (ii + 1 + table[jj + 1]) % 256
    grad1 = table[index1] % 8
    grad2 = table[index2] % 8
    grad3 = table[index3] % 8
    grad4 = table[index4] % 8

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


def heightmap(table, width, height, harmonique, base):
    """docstring for heightmap"""
    lst = []
    factors = []
    for i in range(0, width * height):
        lst.append(0)

    for harm in range(0, harmonique):
        freq = base * 2 ** harm
        img = Image.new('L', (width, height))
        #factor = 2 ** (harmonique - harm - 1)
        factor = 2 ** math.sqrt(harmonique - harm - 1)
        factors.append(1.0 / factor)
        for i in range(0, width):
            for j in range(0, height):
                value = (perlin(table, i, j, freq) + 1) * 0.5 * 255
                lst[j + i * height] += value / factor
                img.putpixel((i, j), value)
        #img.save('freq' + str(freq) + '.pgm')

    for f in factors:
        print f
    sum_factor = sum(factors)
    print sum_factor
    result = Image.new('L', (width, height))
    for i in range(0, width):
        for j in range(0, height):
            result.putpixel((i, j), lst[j + i * height] / sum_factor)

    return result


def generate_palette(path):
    """docstring for generate_palette"""
    palette = []
    img = Image.open('data/ramp.png')
    shift = img.size[0] / 256
    for i in range(0, 256):
        pixel = img.getpixel((i * shift, 0))
        palette.append(pixel[0])
        palette.append(pixel[1])
        palette.append(pixel[2])

    assert len(palette) == 768

    return palette


def convertToHexa(image, liste):
    """docstring for convertToHexa"""
    pass


def main():
    """docstring for main"""
    width = 800
    height = 600
    harmonique = 6
    base = 5

    table = generate_table(1)
    dictionary = check_table(table)
    print dictionary

    result = heightmap(table, width, height, harmonique, base)

    palette = generate_palette('data/ramp.png')

    result.save('result.pgm')

    final = result.copy()
    final.putpalette(palette)
    final.show()
    final.save('final.png')

if __name__ == '__main__':
    main()
